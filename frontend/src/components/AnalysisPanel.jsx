import React, { useState, useEffect } from 'react';
import '../styles/components.css';

const AnalysisPanel = ({ capTable, triggerReload }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (capTable) {
      fetchAnalysis();
    }
  }, [capTable, triggerReload]);

  const fetchAnalysis = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
      });
      const result = await response.json();
      setAnalysis(result);
    } catch (error) {
      console.error('Failed to fetch analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!capTable || !analysis) {
    return <div className="empty-container">Load a cap table to see analysis</div>;
  }

  return (
    <div className="analysis-container">
      <h2>🔍 Quick Analysis</h2>

      {/* Largest Shareholder */}
      {analysis.largest_shareholder && (
        <div className="analysis-card">
          <h4>👑 Largest Shareholder</h4>
          <div className="card-content">
            <p className="highlight">{analysis.largest_shareholder.name}</p>
            <p>{analysis.largest_shareholder.shares.toLocaleString()} shares ({analysis.largest_shareholder.percentage.toFixed(2)}%)</p>
          </div>
        </div>
      )}

      {/* Top 3 Shareholders */}
      {analysis.ownership && (
        <div className="analysis-card">
          <h4>🏆 Top Shareholders</h4>
          <div className="card-content">
            {analysis.ownership.slice(0, 3).map((owner, idx) => (
              <div key={idx} className="ownership-item">
                <span className="rank">#{owner.rank}</span>
                <span className="name">{owner.shareholder}</span>
                <span className="percentage">{owner.percentage.toFixed(2)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ESOP Summary */}
      {analysis.esop_summary && (
        <div className="analysis-card">
          <h4>🏢 ESOP Status</h4>
          <div className="card-content">
            <p>Total ESOP Shares: <strong>{analysis.esop_summary.total_esop_shares}</strong></p>
            <p>ESOP Percentage: <strong>{analysis.esop_summary.esop_percentage.toFixed(2)}%</strong></p>
            <p>Allocated: <strong>{analysis.esop_summary.allocated_shares}</strong></p>
            <p>Available: <strong>{analysis.esop_summary.available_shares}</strong></p>
          </div>
        </div>
      )}

      {loading && <div className="loading">⏳ Analyzing...</div>}
    </div>
  );
};

export default AnalysisPanel;
