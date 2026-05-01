# 🎨 Frontend - AI Equity Assistant

> React + Vite frontend for interactive equity analytics

## 📋 Overview

Modern React frontend providing:
- **Responsive UI**: Works on desktop and tablet
- **Real-time Charts**: Pie charts with Recharts
- **Chat Interface**: Natural language interaction
- **Live Analysis**: Quick insights and calculations
- **File Upload**: Support for JSON cap tables

## 🏗️ Architecture

```
App.jsx (Main)
    ├── CapTableUpload.jsx (Load data)
    ├── CapTableDisplay.jsx (Visualization)
    ├── ChatInterface.jsx (AI queries)
    ├── AnalysisPanel.jsx (Quick insights)
    └── DilutionCalculator.jsx (Simulation)
```

## 📁 File Structure

```
src/
├── main.jsx              # React entry point
├── App.jsx               # Main component
├── components/
│   ├── CapTableUpload.jsx      # Upload component
│   ├── CapTableDisplay.jsx     # Chart & table
│   ├── ChatInterface.jsx       # Chat UI
│   ├── AnalysisPanel.jsx       # Quick insights
│   └── DilutionCalculator.jsx  # Dilution simulator
├── services/
│   └── api.js            # Axios API client
└── styles/
    ├── index.css         # Global styles
    ├── App.css           # App layout
    └── components.css    # Component styles
```

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm build
```

Frontend available at: **http://localhost:5173**

## 🎯 Components

### 1. CapTableUpload
**Responsibilities:**
- Load sample data
- Upload JSON files
- Error handling

**Props:**
```javascript
<CapTableUpload onUploadSuccess={handleUploadSuccess} />
```

**Methods:**
- `handleLoadSample()` - Load demo data
- `handleJsonUpload(e)` - Upload custom file

### 2. CapTableDisplay
**Responsibilities:**
- Display pie chart
- Show shareholder table
- Calculate percentages

**Props:**
```javascript
<CapTableDisplay capTable={capTable} />
```

**Features:**
- Interactive Recharts pie chart
- Shareholder breakdown table
- Real-time percentage calculation

### 3. ChatInterface
**Responsibilities:**
- Chat message UI
- Send queries to backend
- Display AI responses

**Props:**
```javascript
<ChatInterface onQuery={handleQuery} />
```

**Features:**
- Message history
- Auto-scroll to latest
- Loading states
- Error handling

### 4. AnalysisPanel
**Responsibilities:**
- Show quick insights
- Top shareholders
- ESOP summary

**Props:**
```javascript
<AnalysisPanel capTable={capTable} triggerReload={reloadTrigger} />
```

**Features:**
- Top 3 shareholders
- Largest stakeholder card
- ESOP status summary

### 5. DilutionCalculator
**Responsibilities:**
- Calculate dilution impact
- Show before/after percentages

**Props:**
```javascript
<DilutionCalculator capTable={capTable} />
```

**Features:**
- Input new shares
- Calculate button
- Impact table

## 🔌 API Integration

### API Service (`services/api.js`)

```javascript
export const capTableAPI = {
  loadSampleData: () => api.post('/load-sample-data'),
  uploadCapTable: (data) => api.post('/upload-cap-table-json', data),
  getCapTable: () => api.get('/cap-table'),
  query: (question) => api.post('/query', { question }),
  analyze: () => api.post('/analyze'),
  calculateDilution: (newShares) => api.get(`/dilution-calculator?new_shares=${newShares}`),
};
```

### Usage Example
```javascript
const handleQuery = async (question) => {
  const response = await capTableAPI.query(question);
  setMessages([...messages, {
    type: 'assistant',
    text: response.data.answer
  }]);
};
```

## 🎨 Styling

### CSS Architecture

#### Global (`index.css`)
- Reset styles
- Font setup
- Base colors

#### Layout (`App.css`)
- Grid layout (3 columns)
- Header & footer
- Responsive breakpoints

#### Components (`components.css`)
- Button styles
- Card styles
- Chat styles
- Table styles

### Color Scheme
```css
Primary: #667eea (Purple)
Secondary: #764ba2 (Dark Purple)
Success: #10b981 (Green)
Danger: #ef4444 (Red)
Warning: #f59e0b (Orange)
```

### Responsive Design
```css
Desktop: 3-column grid
Tablet: 1-column stack
Mobile: Full-width (via media queries)
```

## 📊 Data Flow

```
1. User uploads cap table
   ↓
2. CapTableUpload sends to backend
   ↓
3. Backend stores in MongoDB
   ↓
4. Frontend receives cap table data
   ↓
5. CapTableDisplay renders chart
   ↓
6. AnalysisPanel fetches analysis
   ↓
7. User can now query via ChatInterface
```

## 🚀 Build & Deploy

### Production Build
```bash
npm run build
# Creates dist/ folder

npm run preview
# Preview production build locally
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

### Deploy to Netlify
```bash
npm run build
# Drag & drop dist/ to Netlify
```

### Docker Build
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 5173
CMD ["npm", "run", "dev"]
```

## 🔄 State Management

### Local State
- `capTable`: Current cap table data
- `messages`: Chat messages
- `loading`: Loading states
- `analysis`: Analysis results

### Lifting State
App.jsx manages global state:
```javascript
const [capTable, setCapTable] = useState(null);
const [reloadTrigger, setReloadTrigger] = useState(0);
```

### Props Drilling
Components receive callbacks:
```javascript
<CapTableUpload onUploadSuccess={handleUploadSuccess} />
```

## 🛣️ Routing (Future)
Currently single-page app. For multi-page:
```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<App />} />
    <Route path="/history" element={<History />} />
  </Routes>
</BrowserRouter>
```

## 🎯 UX Features

### Loading States
- Skeleton screens
- Spinner animations
- Disabled buttons during requests

### Error Handling
- User-friendly error messages
- Retry buttons
- Error boundaries (future)

### Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation

## 🧪 Testing (Future)

### Setup
```bash
npm install --save-dev vitest @testing-library/react
```

### Example Test
```javascript
import { render, screen } from '@testing-library/react';
import ChatInterface from './components/ChatInterface';

test('renders chat input', () => {
  render(<ChatInterface onQuery={() => {}} />);
  const input = screen.getByPlaceholderText(/Ask about/i);
  expect(input).toBeInTheDocument();
});
```

## 📱 Browser Support

| Browser | Minimum |
|---------|---------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

## 🔒 Security

- No hardcoded secrets
- API calls via env variables
- Input validation
- XSS protection (React sanitizes by default)

## 📚 Dependencies

### Core
- `react@18.2.0` - UI framework
- `react-dom@18.2.0` - DOM renderer
- `vite@5.0.0` - Build tool

### UI/Charts
- `recharts@2.10.0` - Chart library
- `react-icons@4.12.0` - Icon set

### API
- `axios@1.6.0` - HTTP client

## 🚀 Performance

### Optimizations
- Lazy loading (Future: React.lazy)
- Code splitting (Vite auto)
- Image optimization
- CSS minification (Vite)

### Bundle Size
- Main: ~150KB
- Recharts: ~300KB
- Axios: ~50KB
- Total: ~500KB (gzipped ~150KB)

## 🔍 Debugging

### React DevTools
```bash
# Chrome extension for React inspection
https://chrome.google.com/webstore/detail/react-developer-tools/
```

### Console Logs
```javascript
console.log('Debug data:', capTable);
console.error('Error occurred:', error);
```

### Vite Debug
```bash
npm run dev -- --debug
```

## 📚 Resources

- React: https://react.dev/
- Vite: https://vitejs.dev/
- Recharts: https://recharts.org/
- Axios: https://axios-http.com/

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Change port in vite.config.js
export default defineConfig({
  server: { port: 3000 }
})
```

### API Connection Failed
```bash
# Check backend is running
curl http://localhost:8000/health

# Update API_URL in services/api.js
```

### npm install Issues
```bash
npm cache clean --force
rm package-lock.json
npm install
```

---

**Built for Qapita** ❤️
