# ⚡ Quick Reference

> Fast lookup for commands and URLs

## 🚀 Quick Start Commands

```bash
# One-liner to start everything (Linux/Mac)
docker-compose up -d && cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py &
cd ../frontend && npm install && npm run dev

# Windows (separate terminals):
# Terminal 1: Backend
cd backend && pip install -r requirements.txt && python main.py

# Terminal 2: Frontend  
cd frontend && npm install && npm run dev

# Terminal 3: MongoDB
docker-compose up -d
```

---

## 🌐 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | React app |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| Alt API Docs | http://localhost:8000/redoc | ReDoc format |
| OpenAPI Schema | http://localhost:8000/openapi.json | API schema |
| MongoDB | localhost:27017 | Database |

---

## 🔌 API Endpoints

### Cap Table
```
POST   /upload-cap-table-json      Upload cap table
GET    /cap-table                  Get current table
POST   /load-sample-data           Load demo data
```

### Queries & Analysis
```
POST   /query                      Ask question (AI)
POST   /analyze                    Quick analysis
GET    /dilution-calculator?new_shares=N    Calculate dilution
GET    /history?limit=10           Query history
GET    /tools                      Available tools
```

### System
```
GET    /                           Health/info
GET    /health                     Health check
```

---

## 💻 Common Commands

### Backend

```bash
# Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate.bat
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env with OpenAI key

# Run
python main.py

# Test
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Frontend

```bash
# Setup
cd frontend
npm install

# Run
npm run dev

# Build
npm run build

# Preview build
npm run preview
```

### MongoDB

```bash
# Docker
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs

# Direct
mongosh "mongodb://localhost:27017"
# Then in mongo shell:
show dbs
use ai_equity_assistant
show collections
db.cap_tables.find().pretty()
```

---

## 📝 Sample Queries

**Try these in the chat:**

```
1. "Who owns the most equity?"
2. "Show ownership breakdown"
3. "What happens with 1000 new shares?"
4. "Tell me about ESOP"
5. "Rank shareholders by percentage"
6. "Get details about Founder Alice"
7. "Calculate 500 share dilution"
8. "Show largest investor"
```

---

## 🧪 Quick API Tests

### cURL Commands

```bash
# Health check
curl http://localhost:8000/health

# Load sample data
curl -X POST http://localhost:8000/load-sample-data

# Query (AI)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Who owns the most?"}'

# Get analysis
curl -X POST http://localhost:8000/analyze

# Dilution calculator
curl http://localhost:8000/dilution-calculator?new_shares=1000
```

### Upload Custom Cap Table

```bash
curl -X POST http://localhost:8000/upload-cap-table-json \
  -H "Content-Type: application/json" \
  -d @data/sample-cap-table-1.json
```

---

## 🔐 Environment Variables

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_equity_assistant

# API
API_TITLE=AI Equity Assistant API
API_VERSION=1.0.0
API_PORT=8000

# OpenAI (Required!)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

---

## 📁 Important Directories

```
backend/
  - main.py          → FastAPI app
  - agent.py         → LangChain agent
  - tools.py         → MCP tools
  - .env            → Configuration (create from .env.example)
  - venv/           → Virtual environment (git ignored)

frontend/
  - src/App.jsx      → Main component
  - src/components/  → React components
  - src/services/    → API client
  - src/styles/      → CSS files
  - node_modules/    → Dependencies (git ignored)

data/
  - sample-*.json    → Sample cap tables
```

---

## 🐛 Troubleshooting Quick Fixes

```bash
# Port in use?
lsof -i :8000 && kill -9 <PID>

# MongoDB not working?
docker-compose up -d
mongosh "mongodb://localhost:27017"

# Backend won't start?
pip install -r requirements.txt
echo $OPENAI_API_KEY  # Check API key is set

# Frontend can't connect?
curl http://localhost:8000/health  # Check backend
cat frontend/src/services/api.js    # Check URL

# npm issues?
rm -rf node_modules package-lock.json
npm install

# Python venv issues?
rm -rf venv
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Key Files at a Glance

| File | Purpose | Lines |
|------|---------|-------|
| backend/main.py | API endpoints | 270+ |
| backend/agent.py | LangChain setup | 180+ |
| backend/tools.py | MCP tools | 250+ |
| frontend/src/App.jsx | Main component | - |
| frontend/src/components/*.jsx | 5 components | - |
| README.md | Main docs | 500+ |
| ARCHITECTURE.md | System design | 300+ |
| GETTING_STARTED.md | Setup guide | 400+ |

---

## 🎯 Testing Checklist

- [ ] Backend starts (Python process)
- [ ] Frontend starts (Vite dev server)
- [ ] MongoDB running (Docker)
- [ ] http://localhost:8000/health returns OK
- [ ] http://localhost:5173 loads
- [ ] Load sample data works
- [ ] Chat returns responses
- [ ] Dilution calculator works

---

## 📦 Dependencies Quick View

### Backend (Python)
```
fastapi          Web framework
langchain        AI agent
langchain-openai LLM integration
pymongo          Database
pydantic         Validation
uvicorn          Server
```

### Frontend (Node)
```
react            UI library
vite             Build tool
recharts         Charts
axios            HTTP client
react-icons      Icon set
```

---

## 🚀 Production Deployment Checklist

- [ ] Update CORS origins
- [ ] Set strong MongoDB credentials
- [ ] Enable HTTPS/SSL
- [ ] Add authentication
- [ ] Setup monitoring
- [ ] Configure backups
- [ ] Add logging service
- [ ] Rate limiting
- [ ] CDN for static assets
- [ ] Environment variables secured

---

## 📚 Documentation Map

```
Start Here:
├── README.md               ← Main documentation
├── PROJECT_SUMMARY.md      ← This project overview
├── GETTING_STARTED.md      ← Setup guide
│
Then Read:
├── ARCHITECTURE.md         ← System design
├── backend/README.md       ← API documentation
└── frontend/README.md      ← Component documentation

Reference:
└── QUICK_REFERENCE.md      ← This file!
```

---

## 🎉 First 5 Minutes

```
1. Start MongoDB: docker-compose up -d
2. Start Backend: cd backend && python main.py
3. Start Frontend: cd frontend && npm run dev
4. Open: http://localhost:5173
5. Click: "Load Sample Data"
6. Chat: "Who owns the most?"
7. Explore: Try dilution calculator
8. Done! 🎊
```

---

**Built for Qapita** ❤️
