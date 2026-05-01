# 🏗️ Architecture Overview

> AI Equity Assistant - Complete System Design

## 🎯 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Web Browser                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  React Frontend (http://localhost:5173)              │  │
│  │  ├─ CapTableUpload                                   │  │
│  │  ├─ CapTableDisplay (Recharts)                       │  │
│  │  ├─ ChatInterface                                    │  │
│  │  ├─ AnalysisPanel                                    │  │
│  │  └─ DilutionCalculator                               │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬──────────────────────────────────────┘
                         │
                    HTTP/REST
                    (Axios)
                         │
┌────────────────────────▼──────────────────────────────────────┐
│  FastAPI Backend (http://localhost:8000)                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ API Layer (main.py)                                   │  │
│  │ ├─ POST /upload-cap-table-json                        │  │
│  │ ├─ POST /query                                        │  │
│  │ ├─ GET /cap-table                                     │  │
│  │ ├─ POST /analyze                                      │  │
│  │ └─ GET /dilution-calculator                           │  │
│  └─────────────────────────────────────────────────────────┘  │
│              ↓                          ↓                      │
│  ┌────────────────────┐      ┌──────────────────────┐          │
│  │ LangChain Agent    │      │ CapTableTools        │          │
│  │ (agent.py)         │      │ (tools.py)           │          │
│  │                    │      │                      │          │
│  │ • Function Agent   │      │ MCP-Style Tools:     │          │
│  │ • Google Gemini LLM  │      │ • get_cap_table      │          │
│  │ • Tool Router      │      │ • calculate_dilution │          │
│  │ • Prompt Hub       │      │ • get_esop_summary   │          │
│  │                    │      │ • shareholder_summary│          │
│  └────────────────────┘      └──────────────────────┘          │
│              │                        │                        │
└──────────────┼────────────────────────┼────────────────────────┘
               │                        │
          ┌────▼───────────────────────▼──┐
          │   MongoDB (localhost:27017)   │
          │                               │
          │  Collections:                 │
          │  • cap_tables                 │
          │  • queries                    │
          │  • embeddings (optional)      │
          └───────────────────────────────┘
```

## 🔄 Data Flow: User Query

```
1. User enters question in ChatInterface
   ↓
2. React sends POST /query to FastAPI
   ↓
3. FastAPI passes question to LangChain Agent
   ↓
4. Agent analyzes question and picks appropriate tool
   ↓
5. Tool (from CapTableTools) executes calculation
   ↓
6. Tool returns structured result
   ↓
7. Agent formats response using LLM
   ↓
8. FastAPI returns answer to React
   ↓
9. ChatInterface displays answer
   ↓
10. Query saved to MongoDB
```

## 🏗️ Detailed Component Architecture

### Frontend Layer
```
App.jsx (State Management)
├── State
│   ├── capTable: CapTable | null
│   ├── reloadTrigger: number
│   └── callbacks
│
├── Layout Grid (3-column)
│   ├── Left Panel
│   │   ├── CapTableUpload
│   │   └── AnalysisPanel
│   ├── Center Panel
│   │   └── CapTableDisplay
│   └── Right Panel
│       ├── ChatInterface
│       └── DilutionCalculator
```

### Backend API Layer
```
FastAPI App
├── Lifecycle Events
│   ├── @startup → db_connection.connect()
│   └── @shutdown → db_connection.disconnect()
│
├── Core Endpoints
│   ├── POST /upload-cap-table-json
│   │   └── Saves to MongoDB & creates agent
│   ├── POST /query
│   │   └── Routes to LangChain agent
│   ├── POST /analyze
│   │   └── Quick calculations
│   └── GET /dilution-calculator
│       └── Simulates dilution
│
├── Middleware
│   └── CORS (for React frontend)
```

### AI/LLM Layer
```
LangChain Agent
├── LLM: ChatGoogleGenerativeAI (gemini-pro)
├── Tools: 6 MCP-style functions
├── Prompt: Hub template
└── Executor: Function-calling agent

Tools:
1. get_cap_table() → Full cap table
2. get_largest_shareholder() → Top stakeholder
3. calculate_ownership() → Ranked breakdown
4. calculate_dilution(shares) → Impact simulation
5. get_esop_summary() → Pool details
6. shareholder_summary(name) → Individual data
```

### Data Layer
```
MongoDB
├── Database: ai_equity_assistant
├── Collections
│   ├── cap_tables
│   │   ├── _id: ObjectId
│   │   ├── company_name: String
│   │   ├── shareholders: Array
│   │   └── timestamps
│   │
│   ├── queries
│   │   ├── _id: ObjectId
│   │   ├── question: String
│   │   ├── answer: String
│   │   └── timestamp
│   │
│   └── embeddings (future)
│       └── Vector embeddings for semantic search
```

## 📊 Technology Stack Rationale

### Why FastAPI?
✅ **Performance**: Async/await support, ~10x faster than Flask
✅ **Developer Experience**: Auto OpenAPI docs, type hints
✅ **Scalability**: Built on ASGI, production-ready
✅ **Pydantic**: Automatic validation and serialization

### Why LangChain?
✅ **Function Calling**: Native OpenAI functions support
✅ **Tool Abstractions**: Unified tool invocation pattern
✅ **Agent Framework**: Complex reasoning with tools
✅ **Ecosystem**: Easy OpenAI, vector DB, memory integration

### Why React + Vite?
✅ **Vite**: Lightning-fast HMR, minimal config
✅ **React Ecosystem**: Massive component library
✅ **Developer Experience**: Fast iteration, great tooling
✅ **Performance**: Small bundle, code splitting

### Why MongoDB?
✅ **Flexible Schema**: Cap tables vary by company
✅ **JSON Native**: Matches our data model perfectly
✅ **Scalable**: Sharding support for millions of queries
✅ **Queries**: Aggregation pipeline for complex analysis

## 🔐 Security Layers

```
┌────────────────────────────────────────┐
│      CORS (Origin validation)          │
├────────────────────────────────────────┤
│   Input Validation (Pydantic)          │
├────────────────────────────────────────┤
│   Rate Limiting (Future)                │
├────────────────────────────────────────┤
│   Authentication (JWT - Future)         │
├────────────────────────────────────────┤
│   MongoDB Auth (Env variables)          │
├────────────────────────────────────────┤
│   Google API Key (Env variables)        │
└────────────────────────────────────────┘
```

## 📈 Scalability Design

### Horizontal Scaling
```
Load Balancer
├── FastAPI Instance 1
├── FastAPI Instance 2
├── FastAPI Instance 3
└── FastAPI Instance N

All connecting to:
└── MongoDB Cluster (Sharded)
```

### Vertical Scaling
- **Backend**: Async operations, worker threads
- **Frontend**: Code splitting, lazy loading
- **Database**: Indexing, aggregation optimization

### Caching Strategy (Future)
```
Request
  ↓
Redis Cache
  ├─ Hit → Return cached response
  └─ Miss → Query → Cache → Return
```

## 🔄 Deployment Architectures

### Local Development
```
Developer Machine
├── Backend: python main.py (8000)
├── Frontend: npm run dev (5173)
└── MongoDB: Local instance (27017)
```

### Local MongoDB Setup
```
Docker Host
├── mongodb service (27017)
├── backend service (8000)
└── frontend service (5173)
```

### Production (Cloud)
```
Cloud Platform (AWS/GCP/Azure)
├── Frontend: CDN + Static Hosting
├── Backend: Containerized (K8s/ECS)
├── Database: Managed Service
└── Cache: Redis/Memcached
```

## 🧪 Testing Strategy

### Backend Testing
```
Unit Tests (pytest)
├── Test models.py
├── Test tools.py calculations
└── Test database.py operations

Integration Tests
├── Test endpoints (FastAPI TestClient)
├── Test LangChain agent
└── Test MongoDB persistence
```

### Frontend Testing
```
Component Tests (Vitest)
├── Test each component render
├── Test prop handling
└── Test event handlers

E2E Tests (Playwright)
├── Test upload flow
├── Test chat interaction
└── Test analysis display
```

## 📊 Monitoring & Observability

```
Logging
├── Application logs → stdout
├── Access logs → FastAPI
└── Error traces → Sentry (future)

Metrics
├── API response time
├── LLM latency
├── Database query time
└── Frontend performance (Core Web Vitals)

Alerting
├── High error rates
├── Slow queries
└── API downtime
```

## 🔄 CI/CD Pipeline (Future)

```
GitHub Push
    ↓
Lint & Format (pre-commit)
    ↓
Run Tests (pytest + vitest)
    ↓
Build Docker Images
    ↓
Push to Registry (Docker Hub/ECR)
    ↓
Deploy to Staging
    ↓
Smoke Tests
    ↓
Deploy to Production
```

## 📈 Performance Optimization

### Frontend Optimization
- Code splitting by component
- Tree shaking (Vite)
- Image optimization
- CSS minification
- Lazy loading routes (future)

### Backend Optimization
- Database indexing (MongoDB)
- Query result caching (Redis future)
- Async/await for I/O
- Connection pooling
- Batch operations

### Network Optimization
- Gzip compression
- CDN for static assets
- Keep-alive connections
- Minimal payload sizes

## 🔐 Data Privacy

```
User Data Handling
├── Cap table: Stored in MongoDB
├── Queries: Stored for history
├── LLM calls: Sent to Google Gemini API
│   └── Configure data retention policy
└── No personal data beyond shareholders
```

## 🎯 Future Architecture Enhancements

### Short-term
- [ ] Add Redis caching layer
- [ ] Implement request logging
- [ ] Add authentication (JWT)
- [ ] Setup error tracking (Sentry)

### Medium-term
- [ ] Multi-tenancy support
- [ ] Real-time WebSocket updates
- [ ] Background job queue (Celery)
- [ ] Vector embeddings (LLM embeddings)

### Long-term
- [ ] GraphQL layer
- [ ] Microservices split
- [ ] Event-driven architecture
- [ ] Machine learning pipeline

