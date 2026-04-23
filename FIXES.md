# FIXES.md — Bug Report

## Fix 1 — api/.env committed with real credentials
**File:** api/.env  
**Problem:** Real Redis password committed to GitHub  
**Fix:** Deleted api/.env, added to .gitignore, created .env.example

## Fix 2 — api/.env syntax error
**File:** api/.env line 2  
**Problem:** APP_ENV=production had no newline, causing syntax error  
**Fix:** Removed the file entirely

## Fix 3 — api/main.py Redis hardcoded to localhost
**File:** api/main.py line 8  
**Problem:** redis.Redis(host="localhost") fails inside Docker containers  
**Fix:** Changed to use REDIS_HOST environment variable

## Fix 4 — api/main.py Redis password ignored
**File:** api/main.py line 8  
**Problem:** REDIS_PASSWORD env var existed but was never used  
**Fix:** Added password=REDIS_PASSWORD to Redis client

## Fix 5 — api/main.py wrong HTTP status for missing jobs
**File:** api/main.py line 17  
**Problem:** Returns HTTP 200 instead of 404 when job not found  
**Fix:** Changed to raise HTTPException(status_code=404)

## Fix 6 — worker/worker.py Redis hardcoded to localhost
**File:** worker/worker.py line 6  
**Problem:** redis.Redis(host="localhost") fails inside Docker  
**Fix:** Changed to use REDIS_HOST environment variable

## Fix 7 — worker/worker.py Redis password ignored
**File:** worker/worker.py line 6  
**Problem:** REDIS_PASSWORD never passed to Redis client  
**Fix:** Added password=REDIS_PASSWORD to Redis client

## Fix 8 — worker/worker.py no graceful shutdown
**File:** worker/worker.py  
**Problem:** No SIGTERM handler, worker killed mid-job on container stop  
**Fix:** Added signal handlers to exit cleanly

## Fix 9 — worker/worker.py wrong queue name
**File:** worker/worker.py line 12  
**Problem:** Queue named "job" was ambiguous  
**Fix:** Renamed to "job_queue" in both api and worker

## Fix 10 — frontend/app.js API URL hardcoded to localhost
**File:** frontend/app.js line 6  
**Problem:** http://localhost:8000 fails inside Docker containers  
**Fix:** Changed to use API_URL environment variable

## Fix 11 — Unpinned dependency versions
**File:** api/requirements.txt, worker/requirements.txt  
**Problem:** No version pins cause non-reproducible builds  
**Fix:** Pinned all versions explicitly

## Fix 12 — frontend/package.json missing engines field
**File:** frontend/package.json  
**Problem:** No Node.js version specified  
**Fix:** Added engines field requiring Node >= 20

## Fix 13 — No healthcheck endpoints
**File:** api/main.py, frontend/app.js  
**Problem:** No /healthz endpoints for Docker health checks  
**Fix:** Added GET /healthz to both services
