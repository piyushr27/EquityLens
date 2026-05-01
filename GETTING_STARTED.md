# 🚀 Getting Started - AI Equity Assistant

> Complete step-by-step guide to run the AI Equity Assistant

## 📋 Prerequisites

Before you start, ensure you have:

### Required
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **MongoDB 5+** - [Local Installation](https://www.mongodb.com/try/download/community)
- **Google API Key** - [Get one](https://ai.google.dev/tutorials/python_quickstart)

### Recommended
- **Git** - For version control
- **VS Code** - Code editor
- **Postman** - API testing (optional)

---

## ⚡ Quick Start (5 minutes)

### Step 1: Clone & Navigate
```bash
cd c:\Users\piyus\Desktop\ai-equity-assistant
```

### Step 2: Start MongoDB
```bash
# Make sure MongoDB is running locally
# If you have MongoDB installed:
mongod

# For MongoDB installed via package manager (Windows):
net start MongoDB
```

### Step 3: Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your-key-here

# Run backend
python main.py
```

**Backend Ready**: http://localhost:8000 ✓

### Step 4: Setup Frontend
```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Frontend Ready**: http://localhost:5173 ✓

### Step 5: Load Sample Data
1. Open http://localhost:5173 in browser
2. Click **📋 Load Sample Data**
3. Ask questions! 🎉

---

## 🔧 Detailed Setup Guide

### Backend Setup (Detailed)

#### 1. Create Virtual Environment
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:**
```bash
# Should show (venv) in terminal
which python  # Should show venv path
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
pip list | grep langchain
```

#### 3. Configure Environment
```bash
# Copy template
copy .env.example .env

# Edit .env file
# Find and update:
# GOOGLE_API_KEY=your-actual-key-here
```

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and paste into .env

#### 4. Verify MongoDB Connection
```bash
# Test MongoDB is accessible
mongosh "mongodb://localhost:27017"

# Should show: test>
# Exit with: exit()
```

#### 5. Start Backend Server
```bash
python main.py

# Should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# ✓ Connected to MongoDB
```

#### 6. Test Backend
```bash
# In another terminal:
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

---

### Frontend Setup (Detailed)

#### 1. Install Node Modules
```bash
cd frontend

npm install

# Or with yarn
yarn install

# Verify
node --version
npm --version
```

#### 2. Configure API URL
**Check `src/services/api.js`:**
```javascript
const API_URL = 'http://localhost:8000';  // Already set
```

#### 3. Start Dev Server
```bash
npm run dev

# Should show:
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

#### 4. Open in Browser
Open http://localhost:5173 - should see the app!

---

## 📊 First Time Usage

### 1. Load Sample Data
Click **📋 Load Sample Data** button
- TechStartup Inc. sample will load
- Pie chart will appear
- Analysis panel will populate

### 2. View Cap Table
- See shareholder breakdown
- Check percentages
- Review pie chart visualization

### 3. Ask Questions
Try these in the chat:
```
"Who owns the most equity?"
"Show ownership breakdown"
"What's the dilution for 1000 new shares?"
"Tell me about ESOP"
"Rank shareholders"
```

### 4. Use Dilution Calculator
- Enter number of new shares
- Click Calculate
- See impact on each shareholder

---

## 📤 Upload Custom Cap Table

### Method 1: Upload JSON File
1. Click **📁 Upload JSON** button
2. Select a JSON file from `data/` folder
3. File uploads and displays

### Method 2: Create Custom Cap Table
Create a JSON file with this structure:
```json
{
  "company_name": "Your Company",
  "shareholders": [
    {
      "name": "Founder",
      "shares": 5000,
      "share_type": "Common"
    },
    {
      "name": "Investor",
      "shares": 2500,
      "share_type": "Preferred"
    }
  ]
}
```

Then upload via UI.

---

## 🔌 API Testing

### Using cURL

#### 1. Load Sample Data
```bash
curl -X POST http://localhost:8000/load-sample-data
```

#### 2. Upload Cap Table
```bash
curl -X POST http://localhost:8000/upload-cap-table-json \
  -H "Content-Type: application/json" \
  -d @data/sample-cap-table-1.json
```

#### 3. Query with AI
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Who owns the most equity?"}'
```

#### 4. Get Analysis
```bash
curl -X POST http://localhost:8000/analyze
```

#### 5. Calculate Dilution
```bash
curl http://localhost:8000/dilution-calculator?new_shares=1000
```

### Using Postman
1. Import `backend/openapi.json` (auto-generated at http://localhost:8000/openapi.json)
2. Or create requests manually:
   - POST: http://localhost:8000/query
   - Body: `{"question": "..."}`

### Auto-Generated Docs
Visit: **http://localhost:8000/docs**

---

## ️ Troubleshooting

### ❌ Backend won't start

**Error: "Address already in use"**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port in .env
API_PORT=8001
```

**Error: "MongoDB connection refused"**
```bash
# Check MongoDB status
docker ps | grep mongodb

# Start MongoDB
docker-compose up -d

# Or test connection
mongosh "mongodb://localhost:27017"
```

**Error: "GOOGLE_API_KEY not found"**
```bash
# Verify .env exists
ls backend/.env

# Check contents
cat backend/.env | grep GOOGLE

# Update with real key
echo "GOOGLE_API_KEY=your-key" >> backend/.env
```

### ❌ Frontend won't start

**Error: "npm not found"**
```bash
# Install Node.js from https://nodejs.org/
node --version  # Should show v16+
npm --version   # Should show 8+
```

**Error: "Port 5173 in use"**
```bash
# Use different port
npm run dev -- --port 3000
```

**Error: "Cannot find API"**
- Check backend is running: `curl http://localhost:8000/health`
- Check `src/services/api.js` API_URL is correct
- Check browser console for CORS errors

### ❌ Queries return errors

**Error: "No cap table loaded"**
```bash
# Load sample data first
curl -X POST http://localhost:8000/load-sample-data
```

**Error: "LangChain error"**
```bash
# Check Google API key is valid
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"

# Test LLM directly
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print(ChatGoogleGenerativeAI().invoke('test'))"
```

**Error: "MongoDB error"**
```bash
# Check MongoDB is running
mongosh "mongodb://localhost:27017"

# Check database exists
db.adminCommand('ping')
```

---

## 📝 Configuration

### Backend (.env)

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_equity_assistant

# API Server
API_TITLE=AI Equity Assistant API
API_VERSION=1.0.0
API_PORT=8000

# Google Gemini (Required for LLM)
GOOGLE_API_KEY=your-api-key-here
GOOGLE_MODEL=gemini-pro
```

### Frontend (vite.config.js)

```javascript
export default defineConfig({
  server: {
    port: 5173,
    open: true,  // Auto-open browser
  },
})
```

### API Configuration (src/services/api.js)

```javascript
const API_URL = 'http://localhost:8000';  // Change if needed
```

---

## 📚 Project Structure

```
ai-equity-assistant/
├── backend/               # Python FastAPI
│   ├── main.py           # Server entry point
│   ├── agent.py          # LangChain agent
│   ├── tools.py          # MCP tools
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/             # React app
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── services/
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   ├── sample-cap-table-1.json
│   └── sample-cap-table-2.json
│
├── docker-compose.yml
├── README.md
└── ARCHITECTURE.md
```

---

## 🚀 Next Steps

After getting started:

1. **Explore the Code**
   - Read [ARCHITECTURE.md](ARCHITECTURE.md) for design details
   - Check [backend/README.md](backend/README.md) for API docs
   - Check [frontend/README.md](frontend/README.md) for component docs

2. **Try Advanced Features**
   - Upload custom cap table
   - Write complex queries
   - Explore dilution scenarios
   - Check MongoDB queries

3. **Customize**
   - Add more MCP tools
   - Enhance LLM prompts
   - Modify UI components
   - Add authentication

4. **Deploy**
   - Docker containers
   - Cloud platforms (Heroku, Railway, Vercel)
   - Production setup with reverse proxy

---

## 🆘 Getting Help

### Check Documentation
- Main README: [README.md](README.md)
- Backend docs: [backend/README.md](backend/README.md)
- Frontend docs: [frontend/README.md](frontend/README.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

### Verify Setup
```bash
# Backend health
curl http://localhost:8000/health

# Frontend check
curl http://localhost:5173

# Database check
mongosh "mongodb://localhost:27017"
```

### Review Logs
```bash
# Backend logs (where you ran python main.py)
# Watch for errors and startup messages

# Frontend logs
# Open http://localhost:5173 and check browser console (F12)
```

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] MongoDB running
- [ ] Google API key obtained
- [ ] Backend virtual environment created
- [ ] `pip install -r requirements.txt` successful
- [ ] `.env` file configured with API key
- [ ] Backend running on http://localhost:8000
- [ ] Frontend dependencies installed
- [ ] Frontend running on http://localhost:5173
- [ ] Sample data loads successfully
- [ ] Can ask questions and get responses
- [ ] MongoDB contains cap_tables collection
