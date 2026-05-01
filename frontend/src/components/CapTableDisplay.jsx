import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';
import '../styles/components.css';

const COLORS = ['#8b5cf6', '#ec4899', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

const CapTableDisplay = ({ capTable }) => {
  if (!capTable) {
    return <div className="empty-container">No cap table loaded</div>;
  }

  const chartData = useMemo(() => {
    return (capTable.shareholders || []).map(sh => ({
      name: sh.name,
      value: sh.percentage || 0
    }));
  }, [capTable.shareholders]);

  return (
    <div className="cap-table-container">
      <h2>📈 Cap Table Overview</h2>
      <div className="company-info">
        <h3>{capTable.company_name || 'Company'}</h3>
        <p>Total Shareholders: {capTable.shareholders?.length || 0}</p>
      </div>

      <div className="chart-section">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value.toFixed(2)}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="shareholders-table">
        <h4>Shareholders Breakdown</h4>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Shares</th>
              <th>Percentage</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {(capTable.shareholders || []).map((sh, idx) => (
              <tr key={idx}>
                <td>{sh.name}</td>
                <td>{sh.shares.toLocaleString()}</td>
                <td>{(sh.percentage || 0).toFixed(2)}%</td>
                <td>{sh.share_type || 'Common'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CapTableDisplay;
