#!/usr/bin/env python3
"""Topic themes (Nolan 10/26: "every topic should have different music and voices to go with the theme").

A script picks a theme with spec "theme" (whole script) or hook beat "theme" (one Short in a pack). The theme sets
the narrator voice (voice, rate, pitch, tempo) and the music bed, overriding the spec's own values. Meatball's
lines, persona and jokes stay the same: all lines are Meatball's, the theme only changes how he sounds.

Voices were picked by numbers on the same Northwoods lines (episodes/weird-pilot/voice-sampler.mp4,
research/48 §10): median pitch from librosa pyin, and faster-whisper (small.en) word accuracy, which must be at
least the current voice's (Andrew +10%: 127 Hz, 0.94). Kokoro onyx was the deepest (90 Hz) but misheard more
(0.91), so no theme uses it. Music sits at about -27 LUFS under a -16 LUFS voice (spec "music_lufs").
"""

THEMES = {
    # dark pulsing synth + deep documentary voice
    "conspiracy": dict(voice="en-US-ChristopherNeural", rate="+26%", pitch="+0Hz", music="gen:conspiracy"),
    # tense ticking strings + clipped, serious deep voice (Northwoods, MKUltra, Gulf of Tonkin)
    "cold-war": dict(voice="en-US-EricNeural", rate="+22%", pitch="-2Hz", music="gen:cold-war"),
    # eerie theremin and pads + hushed deep voice (Roswell, Area 51)
    "ufo": dict(voice="en-US-ChristopherNeural", rate="+26%", pitch="-6Hz", music="gen:ufo"),
    # low drones and sonar pings + deep voice (Bermuda Triangle, sea mysteries)
    "ocean-mystery": dict(voice="en-US-AndrewMultilingualNeural", rate="+12%", pitch="-8Hz", music="gen:ocean"),
    # mischievous pizzicato march + playful, energetic voice (Emu War, Great Molasses Flood, Tarrare)
    "absurd-history": dict(voice="en-US-BrianMultilingualNeural", rate="+16%", pitch="+0Hz", music="gen:absurd"),
    # eerie music-box waltz + warm storyteller voice (Dancing Plague, strange old Europe)
    "strange-history": dict(voice="en-US-BrianMultilingualNeural", rate="+12%", pitch="-4Hz", music="gen:waltz"),
    # electric and bright + crisp, quick voice (lightning, body and science myths)
    "science-myth": dict(voice="en-US-SteffanNeural", rate="+20%", pitch="+0Hz", music="gen:science"),
    # the current animal Shorts: quiz bed + Andrew at +10% (rate +0% then atempo 1.10)
    "animals": dict(voice="en-US-AndrewMultilingualNeural", rate="+0%", pitch="+0Hz", tempo=1.1,
                    music="music/quiz-bed.m4a", music_lufs=None),
}
DEFAULTS = dict(tempo=1.12, music_lufs=-27)   # a touch faster on top of the edge rate (Nolan 10/26)


def apply(spec, theme=None):
    """The spec with the theme's voice and music written into it (rate also becomes the Shorts rate)."""
    name = theme or spec.get("theme")
    if not name:
        return spec
    if name not in THEMES:
        raise SystemExit(f"unknown theme {name!r}; pick one of {', '.join(THEMES)}")
    t = dict(DEFAULTS, **THEMES[name])
    out = dict(spec, theme=name, voice=t["voice"], rate=t["rate"], short_rate=t["rate"], pitch=t["pitch"],
               tempo=t["tempo"], music=t["music"])
    if t.get("music_lufs") is not None:
        out["music_lufs"] = t["music_lufs"]
    else:
        out.pop("music_lufs", None)
    return out
