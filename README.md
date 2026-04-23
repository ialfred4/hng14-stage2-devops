# Job Processing System

A containerised job processing system with four services:
- **frontend** — Node.js/Express UI (port 3000)
- **api** — Python/FastAPI service (port 8000)
- **worker** — Python background processor
- **redis** — Message queue (internal only)

## Prerequisites
- Docker 24.x
- Docker Compose v2
- Git

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ialfred4/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Create your .env file
```bash
cp .env.example .env
```
Edit .env and set your Redis password.

### 3. Start the stack
```bash
docker compose up --build -d
```

### 4. Verify everything is running
```bash
docker compose ps
```
All services should show healthy.

### 5. Open the app
Go to http://localhost:3000 in your browser.
Click Submit New Job and watch it complete!

## Stopping
```bash
docker compose down
```

## Running Tests
```bash
cd api
python3 -m pytest tests/ -v
```

## Bug Fixes
See FIXES.md for all 13 bugs found and fixed.
