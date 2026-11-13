#!/bin/bash
cd "$(dirname "$0")"
if ! command -v node >/dev/null; then echo "Node.js is not installed. Get the LTS version from https://nodejs.org then run this again."; read -r; exit 1; fi
[ -d node_modules ] || { echo "First run: installing..."; npm install; }
[ -f .env ] || cp .env.example .env
(sleep 2; open http://localhost:3000) &
npm start
