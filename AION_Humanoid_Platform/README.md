# AION — Humanoid Robotics & AI Automation Platform

A starter monorepo combining:
- React + Vite dashboard
- Spring Boot REST API (robot projects, commands, health)
- MySQL persistence
- Python FastAPI AI gateway (speech-to-text hook, browser automation, command routing)
- Viser 3D visualization service
- Selenium + `webbrowser` automation
- Nginx reverse proxy
- Docker Compose development stack

> **Capacity note:** This is a development starter, not a validated 200,000-concurrent-user deployment. The architecture is split into independently scalable services. To serve 200k users, deploy behind a load balancer, run multiple stateless API replicas, use managed/high-availability MySQL, Redis/queueing, object storage, observability, and perform load/security tests before making capacity claims.

## Architecture

```text
Browser / React dashboard
          |
       Nginx :80
       /   |    \
   /api  /ai   /viz
    |     |      |
 Spring  FastAPI Viser
 Boot    AI svc  3D scene
    |
 MySQL
```

- React: `http://localhost`
- Spring Boot API: proxied under `/api`
- Python AI service: proxied under `/ai`
- Viser: `http://localhost:8082` (direct link; websocket proxy can vary by deployment)
- MySQL: internal Docker network only

## Start with Docker

Requirements: Docker Desktop / Docker Engine + Compose.

```bash
docker compose up --build
```

Then open `http://localhost`.

If the Java container fails on first run, run `docker compose build --no-cache api` and retry. The first Maven build needs internet access to download dependencies.

## Run services separately (development)

### Backend
Install Java 21 and Maven, then:
```bash
cd backend
mvn spring-boot:run
```
Set DB variables or use Docker Compose for MySQL.

### AI / robotics services
Python 3.11 recommended:
```bash
cd ai-service
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Viser scene is a separate process:
```bash
python -m app.viser_scene
```

Speech recognition:
- The `/ai/voice/transcribe` endpoint accepts an audio upload and uses SpeechRecognition with Google's online recognizer; it requires microphone/audio input supplied by the client and internet access.
- `SpeechRecognition` may require PyAudio for direct microphone capture. This starter deliberately keeps server-side microphone access optional.
- Never expose a server microphone to users without explicit consent.

## API examples

```bash
curl http://localhost/api/health
curl http://localhost/api/robots
curl -X POST http://localhost/ai/command \
  -H "Content-Type: application/json" \
  -d '{"text":"show robot status"}'
```

Create a robot project:
```bash
curl -X POST http://localhost/api/robots \
  -H "Content-Type: application/json" \
  -d '{"name":"Humanoid Alpha","category":"humanoid","description":"Research prototype"}'
```

## Robot visualization categories

The dashboard includes category filters for:
- Humanoid
- Manipulation / grippers
- Locomotion
- Perception / cameras / LiDAR
- Simulation / digital twin
- ROS 2 integration
- Speech / interaction
- AI planning
- Safety / diagnostics

These are starter metadata categories; actual physics simulation, URDF import, ROS 2 control, motion planning, and sensor streams need integration with your chosen simulator and robot hardware.

## Browser automation safety

The Selenium and `webbrowser` tools are restricted to an allowlist (`example.com`, `localhost` by default). Add trusted domains to `AUTOMATION_ALLOWED_HOSTS`. Do not use this service to bypass login, CAPTCHA, access controls, or site terms. Avoid storing credentials in code.

## Production path for 200,000 users

1. Keep Spring Boot and FastAPI stateless; store state in MySQL/Redis/object storage.
2. Put Nginx or a cloud load balancer in front; run multiple API replicas.
3. Use connection pooling and MySQL primary/replica or managed HA database.
4. Use Redis for rate limits, sessions/cache, and a queue (Kafka/RabbitMQ) for long robot/AI jobs.
5. Run Viser visualization separately from the core API; stream scene updates using a dedicated channel.
6. Add OAuth2/OIDC, RBAC, audit logs, secrets management, TLS, rate limiting, WAF, backups.
7. Load test realistic flows (k6/Gatling/JMeter), monitor p95 latency/error rate/DB saturation.
8. For robot safety, require operator confirmation for physical actuation; start with simulation-only commands.

## Important safety note

This starter can display metadata and route demo commands. It does **not** directly actuate a physical humanoid robot. Physical control should go through a separately authenticated ROS 2 gateway with emergency stop, limits, watchdogs, and simulation/hardware interlocks.
