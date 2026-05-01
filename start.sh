#!/bin/bash
set -e

echo "🚀 AI Equity Assistant - Startup Script"
echo "======================================="

# Check if .env exists
if [ ! -f backend/.env ]; then
  echo "📝 Creating .env file from template..."
  cp backend/.env.example backend/.env
  echo "✓ .env created. Please update with your credentials (especially GOOGLE_API_KEY)"
fi

# Ensure MongoDB is running
echo "📦 Checking MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
  echo "⚠️  MongoDB doesn't appear to be running."
  echo "Please start MongoDB locally before continuing."
  exit 1
fi
echo "✓ MongoDB is running"

echo ""
echo "🔙 Starting Backend (FastAPI)..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1 || pip3 install -r requirements.txt
python main.py &
BACKEND_PID=$!
echo "✓ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"

echo ""
echo "⏳ Waiting for backend to start..."
sleep 3

# Test backend health
echo "🏥 Testing backend health..."
curl -s http://localhost:8000/health || echo "⚠️  Backend health check failed"

cd ..

echo ""
echo "🎨 Starting Frontend (React)..."
cd frontend
npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
echo "✓ Frontend running on http://localhost:5173"

echo ""
echo "✨ All services started!"
echo "======================================="
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Run 'kill $BACKEND_PID $FRONTEND_PID' to stop all services"
