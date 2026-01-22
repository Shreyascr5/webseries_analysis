import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [overview, setOverview] = useState(null);
  const [stats, setStats] = useState(null);
  const [showStats, setShowStats] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/overview")
      .then(res => res.json())
      .then(setOverview);

    fetch("http://127.0.0.1:5000/stats")
      .then(res => res.json())
      .then(setStats);
  }, []);

  return (
    <div className="container">
      <h1 className="title">Web Series Dataset – Statistical Analysis</h1>

      {/* OVERVIEW */}
      <div className="card">
        <h2>Dataset Overview</h2>

        {!overview ? (
          <p>Loading overview...</p>
        ) : (
          <>
            <p><strong>Total Records:</strong> {overview.rows}</p>

            <h4>Attributes</h4>
            <ul>
              {overview.columns.map(col => (
                <li key={col}>{col}</li>
              ))}
            </ul>
          </>
        )}
      </div>

      {/* TOGGLE BUTTON */}
      <button onClick={() => setShowStats(!showStats)}>
        {showStats ? "Hide Statistics" : "Show Statistics"}
      </button>

      {/* STATS */}
      {showStats && stats && (
        <div className="card stat-card">
          <h2>Descriptive Statistics</h2>

          {Object.keys(stats).map(col => (
            <div key={col} style={{ marginBottom: "20px" }}>
              <h4>{col}</h4>
              <table>
                <tbody>
                  <tr><td>Mean</td><td>{stats[col].mean?.toFixed(2)}</td></tr>
                  <tr><td>Std Dev</td><td>{stats[col].std?.toFixed(2)}</td></tr>
                  <tr><td>Min</td><td>{stats[col].min}</td></tr>
                  <tr><td>Max</td><td>{stats[col].max}</td></tr>
                </tbody>
              </table>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
