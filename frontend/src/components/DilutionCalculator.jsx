import React, { useState } from 'react';
import '../styles/components.css';

const DilutionCalculator = ({ capTable }) => {
  const [newShares, setNewShares] = useState(1000);
  const [dilutionResult, setDilutionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async () => {
    if (newShares <= 0) return;
    
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/dilution-calculator?new_shares=${newShares}`,
        { method: 'GET' }
      );
      const result = await response.json();
      setDilutionResult(result);
    } catch (error) {
      console.error('Failed to calculate dilution:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!capTable) {
    return <div className="empty-container">Load a cap table to use dilution calculator</div>;
  }

  return (
    <div className="dilution-container">
      <h2>📉 Dilution Calculator</h2>

      <div className="calculator-form">
        <label>New Shares to Issue:</label>
        <div className="input-group">
          <input
            type="number"
            min="1"
            value={newShares}
            onChange={(e) => setNewShares(Math.max(0, parseInt(e.target.value) || 0))}
            placeholder="Number of shares"
            className="input-number"
          />
          <button onClick={handleCalculate} disabled={loading} className="btn btn-primary">
            {loading ? '⏳ Calculating...' : '🔢 Calculate'}
          </button>
        </div>
      </div>

      {dilutionResult && (
        <div className="dilution-results">
          <h4>Dilution Impact</h4>
          <div className="results-table">
            <table>
              <thead>
                <tr>
                  <th>Shareholder</th>
                  <th>Before %</th>
                  <th>After %</th>
                  <th>Dilution</th>
                </tr>
              </thead>
              <tbody>
                {(dilutionResult.dilution_impact || []).map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.shareholder}</td>
                    <td><span className="before">{item.original_percentage.toFixed(2)}%</span></td>
                    <td><span className="after">{item.new_percentage.toFixed(2)}%</span></td>
                    <td>
                      <span className={`dilution ${item.dilution_percentage > 0 ? 'negative' : 'neutral'}`}>
                        {item.dilution_percentage > 0 ? '-' : ''}{item.dilution_percentage.toFixed(2)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default DilutionCalculator;
