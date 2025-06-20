# Friend Finder Web Application

**Friend Finder** is a full-stack social web application where users can connect, chat, and discover new friends by searching based on username, topic, or pincode.

## 🚀 Tech Stack

- **Frontend**: [SvelteKit](https://kit.svelte.dev/) + [Tailwind CSS](https://tailwindcss.com/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLite
- **Authentication**: Session tokens stored in cookies
- **Deployment**: Docker
- **Maps**: [Leaflet.js](https://leafletjs.com/) for displaying user locations on a street map

## 🌟 Features

- 🧑‍🤝‍🧑 User registration and login
- 🔐 Secure session-based authentication
- 💬 Real-time chat functionality
- 🕵️‍♂️ Search friends by username, topic, or pincode
- 🗺️ User map integration
- 🗺️ Map integration using Leaflet.js** to show nearby or connected users on a street-level map
- 📦 Easy to deploy with Docker

## 🧭 Interactive Map with Leaflet.js

Friend Finder uses **Leaflet.js** to embed a real-time street map (StreetFit style) where users can:

- View their own location on the map
- See other users' locations
- Explore and interact with user markers

The map is lightweight, mobile-friendly, and integrated with the Geolocation API to fetch current coordinates securely.

## 🧑‍💻 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (for containerized deployment)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/friend-finder.git
cd friend-finder



** Set up the backend (FastAPI)

- cd backend
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn main:app --reload


** Set up the frontend (SvelteKit)

- cd frontend
- npm install
- npm run dev

** Run with Docker

- docker-compose up --build

📁 Project Structure

friend-finder/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── ...
├── frontend/
│   ├── src/
│   ├── routes/
│   └── ...
├── docker-compose.yml
└── README.md

🔒 Authentication

Session-based authentication using secure HTTP-only cookies. Tokens are set upon successful login and are used to authorize subsequent requests.


📌 Future Improvements

    Notifications system

    Friend request mechanism

    File/image sharing in chat

    UI enhancements

    PostgreSQL support