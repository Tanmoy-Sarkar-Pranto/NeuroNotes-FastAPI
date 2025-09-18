@echo off
REM NeuroNotes Development Startup Script for Windows
REM This script starts both backend and frontend development servers

echo 🚀 Starting NeuroNotes Development Servers...
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found!
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo ❌ Frontend directory not found!
    pause
    exit /b 1
)

REM Check if backend virtual environment exists
if not exist "backend\.venv" (
    echo ❌ Backend virtual environment not found!
    echo 💡 Run 'cd backend && python -m venv .venv && .venv\Scripts\activate && uv sync' first
    pause
    exit /b 1
)

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo ❌ Frontend dependencies not found!
    echo 💡 Run 'cd frontend && npm install' first
    pause
    exit /b 1
)

echo 🔧 Starting backend server...
start "Backend Server" cmd /k "cd backend && .venv\Scripts\activate && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo 🎨 Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Development servers started!
echo 📊 Backend API: http://localhost:8000
echo 🌐 Frontend App: http://localhost:5173
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close the command windows to stop the servers.
pause