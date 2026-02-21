# K-9

Web controller for the mythical K-9 robot (Flask + Socket.IO) with optional GPIO access (Raspberry Pi) and a `--debug` mode to run without hardware.

## Requirements

- Python 3.x
- (Optional, Raspberry Pi) GPIO support via `RPi.GPIO`

## Installation

Clone the repository, then create and activate a virtual environment:

```bash
python3 -m venv venv
source ./venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables

The app reads environment variables from a `.env` file (loaded via `python-dotenv`).

At minimum, set a Flask secret key:

1. Create a `.env` file at the project root:
   ```bash
   cp env.local .env
   ```

2. Edit `.env` if needed:
   - `SECRET_KEY`: used by Flask as `app.config["SECRET_KEY"]`

Example (`.env`):
```env
SECRET_KEY='secret'
```

## Run / Execute

Start the web server:

```bash
python3 web_robot.py
```

To run without hardware (mock GPIO), use debug mode:

```bash
python3 web_robot.py --debug
```

The server logs indicate it starts on:

- `http://0.0.0.0:5000` (binds on all interfaces)

Open in a browser (typical):
- On the same machine: `http://localhost:5000`
- From another device on the network: `http://<raspberry-pi-ip>:5000`

Stop with `Ctrl+C`.

## Notes

- `--debug` enables a “no hardware” mode (useful for development/testing on non-Pi machines).
- GPIO control and the distance sensor are handled by `motors.py` and `ultrasonic.py`.
