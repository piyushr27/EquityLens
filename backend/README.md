# 🔙 Backend - AI Equity Assistant

> FastAPI + LangChain backend for natural language equity queries

## 📋 Overview

Production-grade Python backend providing:
- **FastAPI**: High-performance async REST API
- **LangChain**: AI agent for natural language understanding
- **MongoDB**: Persistent storage for cap tables and queries
- **MCP Tools**: Structured functions for equity calculations

## 🏗️ Architecture

```
User Request
    ↓
FastAPI Endpoint
    ↓
LangChain Agent
    ↓
MCP-style Tools (tools.py)
    ↓
CapTableTools (Calculations)
    ↓
Response
```

## 📁 File Structure

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app, endpoints, lifecycle |
| `config.py` | Configuration and settings |
| `models.py` | Pydantic data models |
| `database.py` | MongoDB connection and queries |
| `agent.py` | LangChain agent setup |
| `tools.py` | MCP-style equity tools |
| `requirements.txt` | Python dependencies |

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with OpenAI API key

# Start MongoDB
docker-compose up -d

# Run
python main.py
```

API available at: **http://localhost:8000**

## 🔌 Endpoints

### Cap Table Management

#### POST `/upload-cap-table-json`
Upload cap table data.

**Request:**
```json
{
  "company_name": "TechStartup Inc.",
  "shareholders": [
    {"name": "Founder Alice", "shares": 5000, "share_type": "Common"}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Cap table uploaded successfully",
  "table_id": "507f1f77bcf86cd799439011",
  "shareholders_count": 1
}
```

#### GET `/cap-table`
Get current cap table.

#### POST `/load-sample-data`
Load sample data for demo.

### Queries & Analysis

#### POST `/query`
**Natural language query using LangChain agent.**

**Request:**
```json
{"question": "Who owns the most equity?"}
```

**Response:**
```json
{
  "question": "Who owns the most equity?",
  "answer": "Based on the cap table, Founder Alice owns the most equity with 5000 shares...",
  "success": true
}
```

#### POST `/analyze`
Get quick analysis of cap table.

**Response:**
```json
{
  "company_name": "TechStartup Inc.",
  "ownership": [
    {"shareholder": "Founder Alice", "shares": 5000, "percentage": 35.71, "rank": 1}
  ],
  "largest_shareholder": {...},
  "esop_summary": {...}
}
```

#### GET `/dilution-calculator?new_shares=1000`
Calculate dilution impact.

#### GET `/history?limit=10`
Get query history.

## 🤖 LangChain Agent

The agent uses OpenAI's function calling to select and invoke tools:

```python
agent = create_openai_functions_agent(
    llm,           # ChatOpenAI model
    tools,         # List of MCP tools
    prompt         # System prompt
)
```

### Tools Available

```python
Tools = {
    "get_cap_table": "Retrieve full cap table",
    "get_largest_shareholder": "Find top stakeholder",
    "calculate_ownership": "Rank shareholders by %",
    "calculate_dilution": "Simulate new investment",
    "get_esop_summary": "ESOP pool details",
    "shareholder_summary": "Individual data"
}
```

## 📊 Models

### CapTable
```python
class CapTable(BaseModel):
    company_name: str
    shareholders: List[Shareholder]
    total_shares: Optional[int]
    created_at: datetime
```

### Shareholder
```python
class Shareholder(BaseModel):
    name: str
    shares: int
    share_type: str  # Common, Preferred, Options
    percentage: Optional[float]
```

### QueryResponse
```python
class QueryResponse(BaseModel):
    query: str
    answer: str
    data: Optional[Dict]
    timestamp: datetime
```

## 🗄️ Database Schema

### Collections

#### `cap_tables`
```javascript
{
  _id: ObjectId,
  company_name: String,
  shareholders: Array,
  total_shares: Number,
  created_at: Date,
  uploaded_at: Date
}
```

#### `queries`
```javascript
{
  _id: ObjectId,
  question: String,
  answer: String,
  company: String,
  timestamp: Date
}
```

## ⚙️ Configuration

### Environment Variables
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_equity_assistant
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
API_PORT=8000
```

## 🛡️ Error Handling

All endpoints include:
- Input validation (Pydantic)
- Try-catch for database errors
- HTTP status codes
- Descriptive error messages

```python
@app.post("/query")
async def query_equity(data: Dict[str, Any]):
    if not current_agent:
        raise HTTPException(status_code=404, detail="No cap table loaded")
    try:
        # Process query
    except Exception as e:
        return {"error": str(e)}
```

## 🔄 Lifecycle

### Startup
```python
@app.on_event("startup")
async def startup_event():
    db_connection.connect()
    print("✓ Connected to MongoDB")
```

### Shutdown
```python
@app.on_event("shutdown")
async def shutdown_event():
    db_connection.disconnect()
```

## 📦 Dependencies

### Core
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation
- `pymongo`: MongoDB driver

### AI/ML
- `langchain`: Agent framework
- `langchain-openai`: OpenAI integration
- `python-dotenv`: Config management

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### On Heroku
```bash
heroku create ai-equity-assistant
git push heroku main
```

## 🔍 Monitoring

### Health Check
```bash
GET /health
```

### API Documentation
Auto-generated at: **http://localhost:8000/docs**

### Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🧪 Testing

### Test Cap Table Upload
```bash
curl -X POST http://localhost:8000/upload-cap-table-json \
  -H "Content-Type: application/json" \
  -d @data/sample-cap-table-1.json
```

### Test Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Who owns the most equity?"}'
```

### Test Dilution
```bash
curl http://localhost:8000/dilution-calculator?new_shares=1000
```

## 🛠️ Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
mongosh "mongodb://localhost:27017"

# Or start via Docker
docker-compose up -d
```

### OpenAI API Error
```bash
# Verify API key
echo $OPENAI_API_KEY

# Check rate limits
# https://platform.openai.com/account/rate-limits
```

### Port Already in Use
```bash
# Change port in config.py or .env
API_PORT=8001

# Or kill process
lsof -i :8000
kill -9 <PID>
```

## 📚 References

- FastAPI: https://fastapi.tiangolo.com/
- LangChain: https://python.langchain.com/
- MongoDB: https://docs.mongodb.com/
- OpenAI: https://platform.openai.com/docs/

---

**Built for Qapita** ❤️
