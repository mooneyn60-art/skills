import io
import json
import os
import tempfile
import unittest

from tars import coach, guard, improve, ledger, registry, rules_sim


def opt_row(day, hhmm, pnl, qty=2, kind="call"):
    return {"id": f"{day}-SPY-C770-{hhmm}-USER", "type": "close", "symbol": "SPY",
            "instrument": f"option_{kind}", "qty": qty, "entry": 1.0, "exit": 1.0,
            "realized_pnl": pnl, "closed": f"{day}T{hhmm[:2]}:{hhmm[2:]}:00Z"}


class Tmp(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self._old = (registry.PATH, improve.PROPOSALS)
        registry.PATH = os.path.join(self.d, "rules.json")
        improve.PROPOSALS = os.path.join(self.d, "proposals")

    def tearDown(self):
        registry.PATH, improve.PROPOSALS = self._old


class TestSim(unittest.TestCase):
    def day(self, pnls, qty=2):
        return [{"pnl": p, "qty": qty} for p in pnls]

    def test_daily_stop_counts_crossing_trade(self):
        self.assertEqual(rules_sim.apply(self.day([-200, -150, 500]), daily_stop=300), (-350, 2))

    def test_losses_in_row(self):
        self.assertEqual(rules_sim.apply(self.day([-1, -1, -1, 9]), max_losses_in_row=3), (-3, 3))

    def test_streak_resets_on_win(self):
        self.assertEqual(rules_sim.apply(self.day([-1, -1, 5, -1, -1, 9]), max_losses_in_row=3)[0], 10)

    def test_qty_scaling(self):
        self.assertEqual(rules_sim.apply(self.day([100], qty=10), max_qty=5), (50.0, 1))


class TestGuard(Tmp):
    def test_stale_state_denies(self):
        v = guard.check_option_open({"date": "2026-01-01"}, {"daily_stop": 300}, today="2026-10-15")
        self.assertTrue(v and "missing" in v[0])

    def test_limits(self):
        st = {"date": "2026-10-15", "options_pnl": -310, "losses_in_row": 3, "round_trips": 4}
        v = guard.check_option_open(st, {"daily_stop": 300, "max_losses_in_row": 3, "max_qty": 3},
                                    today="2026-10-15", qty=5)
        self.assertEqual(len(v), 3)
        self.assertEqual(guard.check_option_open(
            {"date": "2026-10-15", "options_pnl": -100}, {"daily_stop": 300}, today="2026-10-15"), [])

    def test_hook_inert_without_adopted_rules(self):
        out = io.StringIO()
        ev = {"tool_name": "mcp__Robinhood__place_option_order",
              "tool_input": {"legs": [{"position_effect": "open"}], "quantity": "5"}}
        guard.hook_main(io.StringIO(json.dumps(ev)), out)
        self.assertEqual(out.getvalue(), "")

    def test_hook_denies_when_adopted_and_state_stale(self):
        registry.propose("opt-ds300", {"daily_stop": 300}, {})
        registry.set_status("opt-ds300", "adopted", "test")
        old = guard.STATE
        guard.STATE = os.path.join(self.d, "missing.json")
        try:
            out = io.StringIO()
            ev = {"tool_name": "mcp__Robinhood__place_option_order",
                  "tool_input": {"legs": [{"position_effect": "open"}], "quantity": "1"}}
            guard.hook_main(io.StringIO(json.dumps(ev)), out)
        finally:
            guard.STATE = old
        self.assertEqual(json.loads(out.getvalue())["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_closing_orders_never_blocked(self):
        self.assertFalse(guard.is_option_open("mcp__Robinhood__place_option_order",
                                              {"legs": [{"position_effect": "close"}]}))
        self.assertFalse(guard.is_option_open("mcp__Robinhood__place_equity_order", {"side": "buy"}))

    def test_unprotected(self):
        pos = [{"symbol": "NVDA", "quantity": "1", "shares_available_for_sells": "1"},
               {"symbol": "SN", "quantity": "1", "shares_available_for_sells": "0"},
               {"symbol": "VLO", "quantity": "0.45", "shares_available_for_sells": "0.45"}]
        self.assertEqual([p["symbol"] for p in guard.unprotected(pos)], ["NVDA"])


class TestRegistry(Tmp):
    def test_only_adopted_count_and_tightest_wins(self):
        registry.propose("a", {"daily_stop": 300}, {})
        registry.propose("b", {"daily_stop": 200, "max_qty": 3}, {})
        self.assertEqual(registry.adopted_limits(), {})
        registry.set_status("a", "adopted", "Nolan")
        registry.set_status("b", "adopted", "Nolan")
        self.assertEqual(registry.adopted_limits(), {"daily_stop": 200, "max_qty": 3})


class TestImprove(Tmp):
    def test_proposes_rule_that_generalises(self):
        rows = []
        # every day: two wins, then a long losing tail -> a loss-streak stop helps on all days
        for i in range(10):
            day = f"2026-09-{i+1:02d}"
            seq = [50, 40] + [-30] * 8
            rows += [opt_row(day, f"14{j:02d}", p) for j, p in enumerate(seq)]
        text, res = improve.run(rows, write=True, today="2026-10-15")
        self.assertIn("PROPOSED", text)
        self.assertTrue(registry.load()["rules"])
        self.assertTrue(all(r["status"] == "proposed" for r in registry.load()["rules"]))

    def test_rejects_when_unseen_days_disagree(self):
        rows = []
        for i in range(10):
            day = f"2026-09-{i+1:02d}"
            seq = [-30] * 4 + ([-30] * 4 if i < 6 else [400])  # later days: comeback after losses
            rows += [opt_row(day, f"14{j:02d}", p) for j, p in enumerate(seq)]
        text, _ = improve.run(rows, write=False, today="2026-10-15")
        self.assertNotIn("PROPOSED", text)


class TestCoach(unittest.TestCase):
    def test_flags(self):
        w = coach.check("put", 6, 0.1, day_pnl=-200, last_side="call", minutes_since_last=4)
        self.assertEqual(len(w), 5)
        self.assertEqual(coach.check("call", 2, 0.8, has_stop=True), [])


class TestLedger(unittest.TestCase):
    def test_real_ledger_loads(self):
        if not os.path.exists(ledger.ledger_path()):
            self.skipTest("desk ledger not present")
        t = ledger.owner_option_trades(ledger.load())
        self.assertTrue(t and all(a["closed"] <= b["closed"] for a, b in zip(t, t[1:])))


if __name__ == "__main__":
    unittest.main()
