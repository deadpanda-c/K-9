# Robot Web API Documentation

## **Overview**

K-9 uses **Flask + Flask-SocketIO** for **real-time bidirectional communication** between web browser and Raspberry Pi. No traditional REST endpoints - everything flows through **WebSockets**.

## **Protocol: Socket.IO Events**

## **WebSocket Connection**

```text
Client ↔ Server: ws://<pi-ip>:5000/socket.io/
```

## **1. Client → Server (Control Commands)**

| Event           | Data                      | Action               |
| --------------- | ------------------------- | -------------------- |
| `motor_command` | `{"command": "forward"}`  | Both motors forward  |
|                 | `{"command": "backward"}` | Both motors backward |
|                 | `{"command": "stop"}`     | All motors stop      |

**Example (JavaScript):**

```javascript
socket.emit('motor_command', 'forward');
```

## **2. Server → Client (Status Updates)**

**Event:** `status_update` (pushed every 500ms)

**Data format:**

```json
{
  "motors": "forward|backward|stopped",
  "distance": 42.5,     // cm (real or 42.0 in debug)
  "debug": false,       // true = mock mode
  "connected": true
}
```

**Example (JavaScript):**

```javascript
socket.on('status_update', (data) => {
    console.log(`Distance: ${data.distance}cm, Motors: ${data.motors}`);
});
```

## **3. Connection Events** (automatic)

| Event        | Direction       | Purpose                |
| ------------ | --------------- | ---------------------- |
| `connect`    | Server → Client | Connection established |
| `disconnect` | Server → Client | Connection lost        |

## **HTTP Endpoints** (minimal)

| Method | URL                 | Purpose                      |
| ------ | ------------------- | ---------------------------- |
| `GET`  | `/`                 | Serve `templates/index.html` |
| `GET`  | `/static/style.css` | Serve CSS                    |

## **Full JavaScript Client Example**

```javascript
// Connect
const socket = io('http://192.168.1.100:5000');

// Listen for updates
socket.on('status_update', (data) => {
    document.getElementById('distance').textContent = data.distance + 'cm';
    document.getElementById('status').textContent = data.motors;
});

// Send commands
function forward() { socket.emit('motor_command', 'forward'); }
function stop()    { socket.emit('motor_command', 'stop'); }
function backward(){ socket.emit('motor_command', 'backward'); }

// Connection status
socket.on('connect', () => console.log('Connected!'));
socket.on('disconnect', () => console.log('Disconnected'));
```

## **Python Server Events** (`web_robot.py`)

```python
# Incoming from web
@socketio.on('motor_command')
def handle_motor(cmd):
    if cmd == 'forward':    motors.forward()
    elif cmd == 'backward': motors.backward() 
    elif cmd == 'stop':     motors.stop()
    emit('status_update', status)

# Outgoing to web (auto every 500ms)
socketio.emit('status_update', status)
```

## **Message Flow Diagram**

```text
Browser ──────► Pi: motor_command('forward')
                    │
                    ▼ (500ms loop)
Pi ────────► Browser: status_update({motors:'forward', distance:42.5})
```

## **Debug Mode**

Pass `--debug` flag:

- Motors: Print `[MOTORS] forward()` instead of GPIO
- Ultrasonic: Always returns `42.0cm`
- Web shows **"DEBUG"** mode indicator

## **Testing with curl** (basic connectivity)

```bash
curl http://<pi-ip>:5000  # Should return HTML
```

## **Network Access**

- **Local:** `http://192.168.x.x:5000`
- **Remote:** Port forward 5000 or use ngrok
- **Mobile:** Same WiFi network as Pi

## **Error Handling**

- Connection drops → UI shows red ✗
- Invalid commands → Ignored (no crash)
- GPIO errors → Graceful mock fallback

