# LATS — Location-Aware Tracking System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-1.0-lightgrey?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-IoT-660066?logo=eclipse-mosquitto&logoColor=white)

A GPS-based emergency response system that bridges IoT hardware with a real-time web platform to dispatch help to whoever is closest. Registered users share their live GPS coordinates through the browser; when an IoT hardware device triggers an alert, the system applies the Haversine formula across all active sessions to identify the nearest responder instantly and broadcasts that responder's identity and position to every connected client over WebSockets. Published in the International Journal of Computer Science and Engineering (IJCSE).

---

## Features

- Real-time GPS coordinate collection from browser clients
- Haversine-based nearest-responder calculation against a hardware device's fixed coordinates
- Instant WebSocket broadcast (Socket.IO) to all connected clients when the nearest user is identified
- MQTT integration for IoT hardware communication
- User registration, login, and session management with a custom `@login_required` decorator
- Interactive map view (Google Maps) showing the hardware alert origin and nearest responder
- PostgreSQL-backed persistent user store via Flask-SQLAlchemy

## Tech Stack

- **Language:** Python, HTML, JavaScript
- **Web framework:** Flask 1.0
- **Real-time transport:** Flask-SocketIO / python-socketio (WebSockets + eventlet)
- **IoT messaging:** Flask-MQTT / paho-mqtt
- **Database:** PostgreSQL via Flask-SQLAlchemy / psycopg2
- **Session storage:** Flask-Session (filesystem)
- **Front-end:** Bootstrap 4, Google Maps JavaScript API, Socket.IO client
- **Geospatial math:** Haversine formula (Python standard library)

---

## Getting Started

### Prerequisites

- Python 3.6+
- A PostgreSQL database (connection string required)
- A Google Maps API key (for the map view)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/katkhedepushpak/LATS.git
cd LATS

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Before running, set the following values in `application.py`:

| Setting | Location in code | Description |
|---|---|---|
| `SQLALCHEMY_DATABASE_URI` | `app.config[...]` | PostgreSQL connection string |
| `hardware` dict | `hardware = {...}` | Latitude/longitude of the IoT device |
| `app.secret_key` | `app.secret_key = ...` | Flask session secret (change in production) |

### Running the App

```bash
python application.py
```

The server starts on `http://localhost:5000` by default (via eventlet + Socket.IO).

---

## Usage

1. **Register** at `/register` — provide a username, password, and email.
2. **Log in** at `/login`.
3. The dashboard at `/` collects your browser's GPS coordinates and updates the database in real time.
4. When a hardware device connects (or the Socket.IO `connect` event fires), the server computes the nearest registered user and broadcasts their ID along with the hardware device's coordinates to all clients.
5. The map panel renders the alert origin and nearest responder visually.
6. **Log out** at `/logout` — your coordinates are cleared from the active pool.

---

## API / Socket Events

| Event | Direction | Payload | Description |
|---|---|---|---|
| `connect` | Client → Server | — | Triggers nearest-user calculation |
| `nearest` | Server → All clients | `{ id, latitude, longitude }` | Broadcasts nearest responder and hardware location |

---

## Screenshots

> _Screenshots of the dashboard and map view can be added here._

---

## Publication

This system was published in the **International Journal of Computer Science and Engineering (IJCSE)** as a GPS-based emergency response solution combining IoT and machine learning.

---

## Author

Built by [Pushpak Vijay Katkhede](https://katkhedepushpak.github.io)
