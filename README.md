# Aerostats - SAE Brasil Aerodesign Competition Tracker

Live competition data system for SAE Brasil Aerodesign events.

## Tech Stack

### Backend
- Python with FastAPI
- SQLModel for ORM
- SQLite (local) / Supabase Postgres (production)
- Alembic for migrations
- JWT authentication
- uv for dependency management

### Frontend
- Vue 3 + TypeScript
- Pinia for state management
- Vue Router
- TailwindCSS v4
- Axios for API calls
- Mobile-friendly responsive design

## Quick Start

### Option 1: Use the startup script (Recommended)

```bash
./start_dev.sh
```

This script will:
- Kill any existing backend/frontend processes
- Start the backend on port 8000
- Start the frontend on port 5173
- Show you the URLs to access
- Press Ctrl+C to stop both servers

### Option 2: Manual setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies (uv will create a virtual environment automatically):
```bash
uv sync
```

3. Run database migrations:
```bash
uv run alembic upgrade head
```

4. Seed the database with sample data:
```bash
uv run python seed.py
```

This creates:
- Admin user: `admin@aerostats.com` / `admin123`
- Sample teams
- Initial system state

5. Start the development server:
```bash
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

4. Build for production:
```bash
npm run build
```

## Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=sqlite:///./aerostats.db
JWT_SECRET=your-secret-key-here
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

For production with Supabase:
```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-production-secret
ALLOWED_ORIGINS=["https://your-frontend-domain.com"]
```

## API Endpoints

### Public Endpoints (No Auth Required)

- `GET /team_battery_status` - Get all teams and their current status
- `GET /current_flight_status` - Get current flight information
- `GET /current_battery_round` - Get current active round per class
- `GET /last_released_battery_round` - Get last released round per class
- `GET /data_released_batteries` - Get all released results

### Admin Endpoints (Auth Required)

- `POST /auth/login` - Login with email/password
- `PATCH /admin/current_flight` - Update current flight status
- `PATCH /admin/team/{team_id}/battery_status` - Update team battery status
- `PATCH /admin/current_battery_round` - Update active round
- `POST /admin/battery_placing_upload` - Upload results CSV

## Features

### Public Features
- Live team status tracking
- Current flight status display
- Released competition results
- Real-time updates via polling

### Admin Features
- Secure login
- Update current flight (team + status)
- Manage team battery statuses
- Control active rounds per class
- Upload results via CSV
- All mutations are logged with user, timestamp, and changes

## Data Model

- **Team**: Competition teams with status tracking
- **Battery (Round)**: Competition rounds per class
- **Flight**: Individual flight attempts
- **BatteryPlacing**: Results and scores per round
- **User**: Admin users for authentication
- **AuditLog**: Complete mutation history
- **SystemState**: Global competition state

## Status Enums

### Team Battery Status
- not_classified
- waiting_for_inspection_call
- called_for_inspection
- in_inspection
- in_flight_queue
- flying
- post_flight_inspection
- flown

### Flight Status
- competition_paused
- ready_to_takeoff
- flying
- failed_takeoff
- in_flight_fail
- landing_fail
- successful_flight

## CSV Upload Format

For uploading results, use a CSV file with these columns:
```csv
team_id,placing,score
uuid-here,1,123.45
uuid-here,2,95.30
```

## Development

- Backend runs on port 8000
- Frontend runs on port 5173
- CORS is configured for local development
- Hot reload enabled for both backend and frontend
