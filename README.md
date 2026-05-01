# 🚀 EquityLens : AI-Powered Cap Table & Equity Insights Assistant

> **Production-ready AI platform** showcasing modern equity analytics with natural language processing, built with **LangChain, FastAPI, React, and MongoDB**.

## 📋 Overview

This project demonstrates a **modern AI + equity platform** that combines:
- **AI Agents** (LangChain + MCP-style tools) for natural language queries
- **Backend API** (FastAPI + Python) with RAG capabilities
- **Real-time Frontend** (React) with charts and analysis
- **Structured Data** (MongoDB) for cap tables and query history

## 🎯 Core Features

### 1. **Cap Table Management**
- Upload cap table data (JSON format)
- View shareholder breakdown with percentages
- Interactive pie charts and tables
- Real-time calculations

### 2. **AI-Powered Insights (LangChain Agent)**
- Ask natural language questions about equity
- MCP-style tool calling for structured data access
- Example queries:
  - "Who owns the most equity?"
  - "What's the dilution after Series A?"
  - "Show ESOP allocation summary"
  - "Rank shareholders by percentage"

### 3. **Advanced Analytics**
- **Ownership Rankings**: Shareholders ranked by equity percentage
- **Dilution Calculator**: Simulate new investment impact
- **ESOP Management**: Track employee stock option pools
- **Query History**: MongoDB-backed query persistence

### 4. **Production-Grade Architecture**
- Async FastAPI backend with full CORS support
- MongoDB for persistent storage
- LangChain agent with error handling
- React frontend with responsive design
- Docker support for easy deployment

---

## 🏗️ Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI |
| AI Engine | LangChain + OpenAI |
| Database | MongoDB |
| Language | Python 3.9+ |
| Tools | MCP-style functions |

### Frontend
| Component | Technology |
|-----------|-----------|
| Framework | React 18 |
| Build Tool | Vite |
| Charts | Recharts |
| Styling | CSS3 |
| API Client | Axios |

### DevOps
| Component | Technology |
|-----------|-----------|
| Container | Docker |
| Orchestration | Docker Compose |
| Backend Server | Uvicorn |
| Frontend Server | Vite Dev Server |

---

## 📁 Project Structure

```
ai-equity-assistant/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic data models
│   ├── database.py          # MongoDB connection & queries
│   ├── agent.py             # LangChain agent setup
│   ├── tools.py             # MCP-style equity tools
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Environment template
│   └── README.md            # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx         # React entry point
│   │   ├── App.jsx          # Main app component
│   │   ├── components/
│   │   │   ├── CapTableUpload.jsx
│   │   │   ├── CapTableDisplay.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── AnalysisPanel.jsx
│   │   │   └── DilutionCalculator.jsx
│   │   ├── services/
│   │   │   └── api.js       # API client
│   │   └── styles/
│   │       ├── index.css
│   │       ├── App.css
│   │       └── components.css
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── README.md
│
├── data/
│   ├── sample-cap-table-1.json    # Sample: TechStartup Inc.
│   └── sample-cap-table-2.json    # Sample: FinTech Solutions
│
├── docker-compose.yml
├── start.sh
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** (for backend)
- **Node.js 16+** (for frontend)
- **MongoDB 5+** (via Docker or local)
- **OpenAI API Key** (for LLM)

### 1️⃣ Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your credentials
# OPENAI_API_KEY=your-key-here
# MONGODB_URL=mongodb://localhost:27017

# Start MongoDB (Docker)
docker-compose up -d

# Run backend
python main.py
```

Backend will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### 2️⃣ Setup Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### 3️⃣ Load Sample Data

1. Open **http://localhost:5173** in your browser
2. Click **"📋 Load Sample Data"** button
3. Start asking questions! 🎉

---

## 📚 API Documentation

### Core Endpoints

#### 1. **Upload Cap Table**
```bash
POST /upload-cap-table-json
Content-Type: application/json

{
  "company_name": "TechStartup Inc.",
  "shareholders": [
    {"name": "Founder Alice", "shares": 5000, "share_type": "Common"},
    {"name": "Investor", "shares": 2500, "share_type": "Preferred"}
  ]
}
```

#### 2. **Query with AI Agent**
```bash
POST /query
Content-Type: application/json

{"question": "Who owns the most equity?"}
```

Response:
```json
{
  "question": "Who owns the most equity?",
  "answer": "Founder Alice owns the most equity with 5000 shares...",
  "success": true
}
```

#### 3. **Get Cap Table**
```bash
GET /cap-table
```

#### 4. **Quick Analysis**
```bash
POST /analyze
```

Response includes:
- Ownership breakdown
- Largest shareholder
- ESOP summary

#### 5. **Calculate Dilution**
```bash
GET /dilution-calculator?new_shares=1000
```

Shows impact on each shareholder.

#### 6. **Query History**
```bash
GET /history?limit=10
```

---

## 🤖 AI Tools (MCP-Style)

The LangChain agent has access to these structured tools:

| Tool | Purpose | Input |
|------|---------|-------|
| `get_cap_table` | Retrieve full cap table | - |
| `get_largest_shareholder` | Find top stakeholder | - |
| `calculate_ownership` | Rank shareholders | - |
| `calculate_dilution` | Simulate new investment | New shares (int) |
| `get_esop_summary` | ESOP pool details | - |
| `shareholder_summary` | Individual shareholder data | Shareholder name (str) |

### Example LLM Interactions

```
User: "Who owns the largest stake?"
Agent: Calls get_largest_shareholder → Returns top owner with %

User: "What happens if we issue 1000 new shares?"
Agent: Calls calculate_dilution(1000) → Shows impact on all shareholders

User: "Show me the ESOP status"
Agent: Calls get_esop_summary → Returns pool details
```

---

## 🧪 Sample Data

Two sample cap tables included:

### Sample 1: TechStartup Inc. (Seed Stage)
```json
{
  "company_name": "TechStartup Inc.",
  "shareholders": [
    {"name": "Founder Alice", "shares": 5000},
    {"name": "Founder Bob", "shares": 3000},
    {"name": "Seed Investor A", "shares": 2500},
    {"name": "Seed Investor B", "shares": 2000},
    {"name": "ESOP Pool", "shares": 2000},
    {"name": "Angel Investor", "shares": 1500}
  ]
}
```

### Sample 2: FinTech Solutions (Series A)
```json
{
  "company_name": "FinTech Solutions Ltd.",
  "shareholders": [
    {"name": "CEO James", "shares": 8000},
    {"name": "CTO Sarah", "shares": 6000},
    {"name": "Series A - VC Fund X", "shares": 5000},
    {"name": "Series A - Family Office", "shares": 3000},
    {"name": "ESOP Pool", "shares": 3000}
  ]
}
```

---

## 🔧 Configuration

### Backend (.env)
```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_equity_assistant

# API
API_TITLE=AI Equity Assistant API
API_VERSION=1.0.0
API_PORT=8000

# LLM
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
```

### Frontend
Update `frontend/src/services/api.js`:
```javascript
const API_URL = 'http://localhost:8000';  // Change if needed
```

---

## 🐳 Docker Deployment

### Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# MongoDB will be available at localhost:27017
# Update backend .env with: MONGODB_URL=mongodb://mongodb:27017
```

### Manual Docker Build
```bash
# Backend
cd backend
docker build -t ai-equity-assistant-backend .
docker run -p 8000:8000 --env-file .env ai-equity-assistant-backend

# Frontend
cd frontend
docker build -t ai-equity-assistant-frontend .
docker run -p 5173:5173 ai-equity-assistant-frontend
```

---

## 📊 Frontend Features

### Components

1. **CapTableUpload**
   - Load sample data
   - Upload custom JSON files
   - Error handling

2. **CapTableDisplay**
   - Interactive pie chart
   - Shareholder table
   - Real-time percentage calculations

3. **ChatInterface**
   - Natural language queries
   - Message history
   - Loading states

4. **AnalysisPanel**
   - Quick insights
   - Top shareholders
   - ESOP summary

5. **DilutionCalculator**
   - Simulate new investment
   - Show impact on ownership %
   - Visual dilution breakdown

---

## 🎓 Architecture Highlights


✅ **RAG + Tool Calling**: LangChain agent uses structured tools to query data
✅ **Structured Finance Data**: Proper cap table models and calculations
✅ **Real-time Analytics**: Live charts and instant calculations
✅ **Production Ready**: Error handling, MongoDB persistence, CORS
✅ **AI + Equity Focus**: Natural language interface for finance professionals
✅ **Scalable Design**: Microservice-ready backend with clear separation

### Key Design Patterns

1. **MCP-Style Tools**
   ```python
   # Tools registry for consistent invocation
   Tools = {
       "get_cap_table": func(),
       "calculate_dilution": func(),
       "get_esop_summary": func()
   }
   ```

2. **Structured Data Models**
   ```python
   class CapTable(BaseModel):
       shareholders: List[Shareholder]
       total_shares: int
   ```

3. **Agent + Tools Pattern**
   ```python
   agent = create_openai_functions_agent(llm, tools, prompt)
   # Agent selects best tool for user query
   ```

---

## 🔐 Security Considerations

- **API Security**: CORS configured for localhost (update for production)
- **Secrets**: Environment variables for sensitive data
- **Database**: MongoDB auth enabled in docker-compose
- **Validation**: Pydantic models validate all inputs
- **Error Handling**: Graceful error responses without sensitive data leaks

### Production Checklist

- [ ] Update CORS origins to production domain
- [ ] Use strong MongoDB credentials
- [ ] Enable HTTPS/SSL
- [ ] Add authentication (JWT tokens)
- [ ] Rate limiting on API
- [ ] Audit logging
- [ ] Regular MongoDB backups

---

## 🚨 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check MongoDB connection
mongosh "mongodb://localhost:27017"

# Check port availability
netstat -an | grep 8000
```

### Frontend can't connect to backend
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check CORS configuration in main.py
# Update API_URL in frontend/src/services/api.js
```

### LangChain errors
```bash
# Verify OpenAI API key
echo $OPENAI_API_KEY

# Test LLM connection
python -c "from langchain_openai import ChatOpenAI; ChatOpenAI().invoke('test')"
```

### MongoDB issues
```bash
# Check MongoDB status
docker ps | grep mongodb

# View logs
docker logs <container_id>

# Restart MongoDB
docker restart <container_id>
```

---

## 📈 Next Steps / Enhancement Ideas

### Short-term
- [ ] Add more AI tools (tax implications, dilution projection)
- [ ] Implement user authentication
- [ ] Export cap table as PDF
- [ ] Real-time collab features

### Medium-term
- [ ] Multi-company support
- [ ] Historical dilution tracking
- [ ] Investment round simulation
- [ ] Vesting schedules

### Long-term
- [ ] Predictive modeling (valuation, cap table growth)
- [ ] Integration with legal templates
- [ ] API rate limiting and metrics
- [ ] Mobile app

---

## 📄 API Schema Reference

### CapTable Model
```python
{
  "company_name": str,
  "shareholders": [
    {
      "name": str,
      "shares": int,
      "share_type": str,  # Common, Preferred, Options
      "percentage": float  # Calculated
    }
  ]
}
```

### Query Response
```python
{
  "question": str,
  "answer": str,
  "success": bool
}
```

### Analysis Response
```python
{
  "company_name": str,
  "ownership": [OwnershipSummary],
  "largest_shareholder": dict,
  "esop_summary": dict
}
```


## 🎉 Quick Demo Queries

Try these questions in the chat:

```
"Who is the largest shareholder?"
"Show ownership breakdown"
"What happens if we issue 2000 new shares?"
"Tell me about the ESOP pool"
"Rank all shareholders by percentage"
"How many shares does Founder Alice have?"
"What's the total shareholding of investors?"
"Calculate dilution for 500 new shares"
```

