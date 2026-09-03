$ErrorActionPreference = "Stop"
$Project = "E:\smart campus one"
if (!(Test-Path $Project)) { throw "Project folder not found: $Project" }
Set-Location $Project

$dirs = @(
"assets","frontend\src\components","frontend\src\pages","frontend\src\layouts","frontend\src\hooks",
"frontend\src\services","frontend\src\utils","frontend\src\types","frontend\src\assets","frontend\public",
"backend\app\api\routes","backend\app\core","backend\app\models","backend\app\schemas","backend\app\services",
"backend\app\repositories","backend\app\middleware","backend\tests","database\migrations","database\seeds",
"modules\timetable","modules\attendance","modules\reports","modules\notifications","modules\integrations",
"storage","docs\architecture","docs\api","docs\database","docs\setup","docs\project-report",
"tests\integration","tests\e2e","deployment\docker","deployment\nginx","deployment\scripts")
$dirs | % { New-Item -ItemType Directory -Path $_ -Force | Out-Null }

function Put($p,$s) {
  $d=Split-Path $p -Parent
  if($d){New-Item -ItemType Directory -Path $d -Force | Out-Null}
  [IO.File]::WriteAllText($p,$s,[Text.UTF8Encoding]::new($false))
}

Put ".gitignore" @'
.env
.env.*
!.env.example
*.pem
*.key
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.venv/
venv/
node_modules/
frontend/dist/
frontend/.vite/
npm-debug.log*
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db
storage/*
!storage/.gitkeep
.coverage
htmlcov/
coverage/
*.log
'@

Put ".env.example" @'
APP_ENV=development
APP_NAME=SmartCampus One
APP_VERSION=0.1.0
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:5173
DATABASE_URL=postgresql+psycopg://smartcampus:smartcampus_dev@localhost:5432/smartcampus
SECRET_KEY=change-this-development-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
VITE_API_BASE_URL=http://localhost:8000/api
'@

Put "docker-compose.yml" @'
services:
  postgres:
    image: postgres:16-alpine
    container_name: smartcampus-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: smartcampus
      POSTGRES_USER: smartcampus
      POSTGRES_PASSWORD: smartcampus_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U smartcampus -d smartcampus"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    build: ./backend
    container_name: smartcampus-backend
    environment:
      APP_ENV: development
      DATABASE_URL: postgresql+psycopg://smartcampus:smartcampus_dev@postgres:5432/smartcampus
      SECRET_KEY: change-this-development-secret
      CORS_ORIGINS: http://localhost:5173
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
'@

Put "backend\requirements.txt" @'
fastapi>=0.115,<1
uvicorn[standard]>=0.30,<1
pydantic-settings>=2.6,<3
SQLAlchemy>=2.0,<3
psycopg[binary]>=3.2,<4
python-jose[cryptography]>=3.3,<4
passlib[bcrypt]>=1.7,<2
pytest>=8,<9
httpx>=0.27,<1
'@

Put "backend\Dockerfile" @'
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
'@

Put "backend\app\__init__.py" ""
Put "backend\app\api\__init__.py" ""
Put "backend\app\api\routes\__init__.py" ""
Put "backend\app\core\__init__.py" ""

Put "backend\app\core\config.py" @'
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SmartCampus One"
    app_version: str = "0.1.0"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://smartcampus:smartcampus_dev@localhost:5432/smartcampus"
    secret_key: str = "change-this-development-secret"
    access_token_expire_minutes: int = 30
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
'@

Put "backend\app\core\database.py" @'
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'@

Put "backend\app\api\routes\health.py" @'
from fastapi import APIRouter
router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {"status":"ok","service":"SmartCampus One API","version":"0.1.0"}
'@

Put "backend\app\main.py" @'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes.health import router as health_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router, prefix="/api")

@app.get("/")
def root():
    return {"name": settings.app_name, "version": settings.app_version, "status": "running"}
'@

Put "backend\tests\test_health.py" @'
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_root():
    r=client.get("/")
    assert r.status_code==200
    assert r.json()["name"]=="SmartCampus One"

def test_health():
    r=client.get("/api/health")
    assert r.status_code==200
    assert r.json()["status"]=="ok"
'@

Put "frontend\package.json" @'
{"name":"smartcampus-one-frontend","private":true,"version":"0.1.0","type":"module","scripts":{"dev":"vite","build":"tsc -b && vite build","preview":"vite preview"},"dependencies":{"react":"^18.3.1","react-dom":"^18.3.1"},"devDependencies":{"@types/react":"^18.3.12","@types/react-dom":"^18.3.1","@vitejs/plugin-react":"^4.3.4","typescript":"^5.7.2","vite":"^6.0.5"}}
'@

Put "frontend\tsconfig.json" @'
{"files":[],"references":[{"path":"./tsconfig.app.json"},{"path":"./tsconfig.node.json"}]}
'@
Put "frontend\tsconfig.app.json" @'
{"compilerOptions":{"target":"ES2022","lib":["ES2022","DOM","DOM.Iterable"],"skipLibCheck":true,"module":"ESNext","moduleResolution":"Bundler","allowImportingTsExtensions":true,"resolveJsonModule":true,"isolatedModules":true,"noEmit":true,"jsx":"react-jsx","strict":true},"include":["src"]}
'@
Put "frontend\tsconfig.node.json" @'
{"compilerOptions":{"target":"ES2023","lib":["ES2023"],"module":"ESNext","moduleResolution":"Bundler","skipLibCheck":true,"noEmit":true,"strict":true},"include":["vite.config.ts"]}
'@
Put "frontend\vite.config.ts" @'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({plugins:[react()],server:{port:5173,host:"localhost"}});
'@
Put "frontend\index.html" @'
<!doctype html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/><meta name="theme-color" content="#0f172a"/><title>SmartCampus One</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>
'@
Put "frontend\src\main.tsx" @'
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";
createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
'@
Put "frontend\src\App.tsx" @'
function App() {
  return <main className="shell"><section className="card"><div className="logo">🎓</div><p className="eyebrow">SMARTCAMPUS ONE</p><h1>One Smart Platform for Every Campus</h1><p>Multi-college smart timetable and attendance management platform.</p><div className="status">● Phase 1 foundation is running</div></section></main>;
}
export default App;
'@
Put "frontend\src\index.css" @'
:root{font-family:Inter,system-ui,sans-serif;color:#e5e7eb;background:#020617}*{box-sizing:border-box}body{margin:0;min-width:320px;min-height:100vh;background:radial-gradient(circle at 20% 10%,#2563eb3d,transparent 35%),radial-gradient(circle at 80% 90%,#7c3aed33,transparent 35%),#020617}.shell{min-height:100vh;display:grid;place-items:center;padding:24px}.card{width:min(900px,100%);padding:56px;border:1px solid #94a3b830;border-radius:28px;background:#0f172ac7;box-shadow:0 30px 80px #00000059}.logo{width:72px;height:72px;display:grid;place-items:center;border-radius:20px;background:linear-gradient(135deg,#2563eb,#7c3aed);font-size:34px}.eyebrow{margin:28px 0 8px;color:#60a5fa;font-size:13px;font-weight:800;letter-spacing:.18em}h1{margin:0;font-size:clamp(38px,7vw,68px);line-height:1.02;letter-spacing:-.04em}.card>p:not(.eyebrow){color:#94a3b8;font-size:18px;line-height:1.7}.status{display:inline-block;margin-top:18px;padding:10px 14px;border:1px solid #22c55e40;border-radius:999px;color:#bbf7d0;background:#22c55e14;font-size:14px}
'@

# Placeholder files to preserve module structure
$placeholders = @(
"storage\.gitkeep","database\migrations\.gitkeep","database\seeds\.gitkeep",
"modules\timetable\.gitkeep","modules\attendance\.gitkeep","modules\reports\.gitkeep",
"modules\notifications\.gitkeep","modules\integrations\.gitkeep","tests\integration\.gitkeep",
"tests\e2e\.gitkeep","deployment\docker\.gitkeep","deployment\nginx\.gitkeep","deployment\scripts\.gitkeep",
"docs\architecture\README.md","docs\api\README.md","docs\database\README.md","docs\setup\README.md","docs\project-report\README.md")
$placeholders | % { if(!(Test-Path $_)){Put $_ "# SmartCampus One`r`n`r`nPhase 1 documentation placeholder."} }

Write-Host "`nPhase 1 files created." -ForegroundColor Green
Write-Host "Now checking installed tools..." -ForegroundColor Cyan
foreach($tool in @("git","node","npm","python","docker")){
  if(Get-Command $tool -ErrorAction SilentlyContinue){Write-Host "$tool : OK" -ForegroundColor Green}
  else{Write-Host "$tool : NOT FOUND" -ForegroundColor Yellow}
}
Write-Host "`nIMPORTANT: This script does NOT push to GitHub and does NOT delete your existing README/assets." -ForegroundColor Yellow
Write-Host "Next: run the verification commands shown below."
