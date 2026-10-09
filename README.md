# AION — Humanoid Robotics Platform

**AION** is an AI-powered humanoid robotics platform that integrates web technologies, backend services, AI automation, speech recognition, and 3D visualization to support humanoid robot development and management.

## 🚀 Features

* **ReactJS:** Interactive frontend dashboard.
* **Spring Boot:** Java-based REST API and backend services.
* **Python FastAPI:** AI automation and speech-related services.
* **Viser:** 3D scene visualization for robotics.
* **SpeechRecognition:** Voice-input processing.
* **Selenium & Webbrowser:** Browser automation and URL opening.
* **MySQL:** Persistent data storage.
* **Nginx:** Reverse proxy and request routing.
* **Docker Compose:** Simplified multi-service deployment.

## 🛠️ Technologies Used

ReactJS, Vite, Java 21, Spring Boot, Python, FastAPI, MySQL, JPA, Viser, Selenium, SpeechRecognition, Nginx, and Docker.

## 📂 Project Structure

```text
AION/
├── frontend/       # ReactJS user interface
├── backend/        # Spring Boot REST API
├── ai-service/     # Python AI and automation services
├── nginx/          # Reverse proxy configuration
├── docker-compose.yml
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

* Docker and Docker Compose
* Git (optional)

### Run the Project

1. Download and extract the project ZIP.
2. Open a terminal in the project directory.
3. Start the services:

```bash
docker compose up --build
```

4. Open the frontend in your browser using the local address configured in the project.

Check the Docker Compose configuration and service logs for the exact ports and startup status.

## 🎯 Project Goal

To provide a unified platform for managing robotics projects, visualizing 3D scenes, and integrating AI-powered automation through a modular web architecture.

## 📈 Scalability

The architecture is designed as a starting point for future scaling. Supporting **200,000 concurrent users** would require production deployment, horizontal scaling, load balancing, database optimization, monitoring, security hardening, and comprehensive load testing.

## ⚠️ Important Note

This project is a software platform and starter implementation. It does not directly control physical humanoid robot hardware. Hardware integration requires suitable robot drivers, communication protocols, and safety mechanisms.

## 📄 License

Add an appropriate open-source or project-specific license before distributing this project.
