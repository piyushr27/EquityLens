import React, { useState } from 'react';
import CapTableUpload from './components/CapTableUpload';
import CapTableDisplay from './components/CapTableDisplay';
import ChatInterface from './components/ChatInterface';
import AnalysisPanel from './components/AnalysisPanel';
import DilutionCalculator from './components/DilutionCalculator';
import './styles/App.css';

function App() {
  const [capTable, setCapTable] = useState(null);
  const [reloadTrigger, setReloadTrigger] = useState(0);

  const handleUploadSuccess = (data) => {
    setCapTable(data);
    setReloadTrigger(prev => prev + 1);
  };

  const handleQuery = () => {
    setReloadTrigger(prev => prev + 1);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>🚀 AI-Powered Cap Table & Equity Insights</h1>
          <p>Qapita-Inspired Equity Analytics Platform</p>
        </div>
      </header>

      <div className="container">
        <div className="left-panel">
          <CapTableUpload onUploadSuccess={handleUploadSuccess} />
          <AnalysisPanel capTable={capTable} triggerReload={reloadTrigger} />
        </div>

        <div className="center-panel">
          <CapTableDisplay capTable={capTable} />
        </div>

        <div className="right-panel">
          <ChatInterface onQuery={handleQuery} />
          <DilutionCalculator capTable={capTable} />
        </div>
      </div>

      <footer className="footer">
        <p>Showcasing Qapita's AI + Equity Platform Stack | LangChain × FastAPI × React × MongoDB</p>
      </footer>
    </div>
  );
}

export default App;
