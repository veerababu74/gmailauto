# Render Deployment Configuration Recommendations

## Current Setup Analysis
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:10000
- Working Directory: backend/

## Recommended Optimizations

### 1. BUILD COMMAND (Recommended Changes)
Current: backend/ $ pip install -r requirements.txt
Recommended: backend/ $ pip install --no-cache-dir -r requirements_deploy.txt

Benefits:
- Uses deployment-specific requirements
- Avoids caching issues
- Faster builds with --no-cache-dir

### 2. PRE-DEPLOY COMMAND (Add This)
Current: backend/ $ (empty)
Recommended: backend/ $ alembic upgrade head

Benefits:
- Automatically runs database migrations
- Ensures DB schema is up-to-date
- Prevents deployment issues

### 3. START COMMAND (Current is Good)
Current: backend/ $ gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:10000
Status: ✅ OPTIMAL

This is perfect for Render's requirements:
- Uses gunicorn for production
- 4 workers for good performance
- UvicornWorker for FastAPI compatibility
- Binds to 0.0.0.0:10000 (Render's default port)

### 4. ENVIRONMENT VARIABLES TO SET
Add these in Render Dashboard > Environment:
- PYTHON_VERSION=3.12.9 (or use runtime.txt)
- RENDER_ENV=production
- DATABASE_URL=(if using external DB)

### 5. FILES TO ENSURE ARE PRESENT
✅ runtime.txt (already created)
✅ requirements_deploy.txt (already updated)
✅ requirements.txt (fallback)
✅ main.py (FastAPI app)

## Alternative Build Commands (if issues persist)

### Option A: Use requirements_no_rust.txt
backend/ $ pip install --no-cache-dir -r requirements_no_rust.txt

### Option B: Force binary packages only
backend/ $ pip install --no-cache-dir --only-binary=all -r requirements_deploy.txt

### Option C: Use emergency build script
backend/ $ ./emergency_build.sh

## Monitoring & Debugging Commands

### Check deployment status
curl https://your-app-name.onrender.com/

### View logs in Render Dashboard
- Go to Logs tab
- Monitor for errors during build/deploy

### Health check endpoint
curl https://your-app-name.onrender.com/docs
