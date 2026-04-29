# Real-Time Multiplayer Game

A two-to-eight player coin collecting game over WebSockets.

This is a small, independent Python portfolio project. The code favours ordinary functions and clear modules over complex architecture.

## Setup

Requires Python 3.12+ (desktop tools also require Tkinter, included with the standard Windows Python installer).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

Run commands from this repository's root. Web apps bind to localhost by default. Each app is independent, so stop one before starting another on the same port.

## Check it

```sh
python -m pytest -q
```

## Dates

The commit author dates have been deliberately arranged between October 2025 and October 2026 at the portfolio owner's request. They are presentation metadata, not a record of the actual development timeline. Repository creation and upload timestamps remain the real dates.

## Play locally

Open http://127.0.0.1:5000 in two browser tabs. Give each player a different name and join the same room. Move with arrow keys, WASD or the on-screen buttons. Gold coins award points; other players block a square. Rooms allow at most eight players. Positions and scores are controlled by Python, with a limit on accepted movement frequency. Reloading disconnects the player and resets that player's score.

This is a small in-memory Flask-Sock/WebSocket game, adapted from the Node.js/Socket.io idea. Each connection is cleaned up when it closes, and an empty room is removed. It uses one server process and a lock around game state; horizontal scaling and persistent accounts are outside this project's scope. The default listener is localhost. Sharing it over a network requires a deliberately configured host and network setup.

## Optional local container

```sh
docker build -t realtime-multiplayer-game .
docker run --rm -p 127.0.0.1:5000:5000 realtime-multiplayer-game
```

This runs a local demonstration server. Container storage is temporary unless you mount a volume for `instance/`. Docker commands were supplied but Docker is not installed in the development environment, so container execution was not verified here.
