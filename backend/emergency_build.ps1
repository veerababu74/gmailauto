# Emergency build script that bypasses all Rust compilation
$ErrorActionPreference = "Stop"

Write-Host "🚨 Emergency build mode - bypassing Rust compilation..." -ForegroundColor Yellow

# Use temporary requirements file
$tempRequirements = @"
fastapi==0.104.1
uvicorn==0.24.0
gunicorn==21.2.0
python-multipart==0.0.6
python-jose==3.3.0
passlib==1.7.4
python-decouple==3.8
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
pymysql==1.1.0
mysql-connector-python==8.2.0
aiomysql==0.2.0
aiosqlite==0.19.0
pydantic==1.10.13
email-validator==2.1.0
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
celery==5.3.4
redis==5.0.1
cryptography==3.4.8
typing-extensions==4.8.0
"@

Set-Content -Path "temp_requirements.txt" -Value $tempRequirements

Write-Host "📦 Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip

Write-Host "🚀 Installing packages with only pre-built wheels..." -ForegroundColor Green
python -m pip install --no-cache-dir --only-binary=all -r temp_requirements.txt

Write-Host "✅ Emergency build completed successfully!" -ForegroundColor Green
