import React, { useEffect, useState } from "react";
import { getOverview } from "../api";

function Overview() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getOverview()
      .then(setData)
      .catch(() => setError("Unable to load dataset overview"));
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!data) return <p>Loading dataset overview...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Dataset Overview</h2>

      <p><strong>Total Records:</strong> {data.num_rows}</p>
      <p><strong>Total Attributes:</strong> {data.num_columns}</p>

      <h3>Attributes</h3>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Attribute Name</th>
            <th>Data Type</th>
          </tr>
        </thead>
        <tbody>
          {data.columns.map((col, index) => (
            <tr key={index}>
              <td>{col.name}</td>
              <td>{col.dtype}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Sample Data (First 5 Records)</h3>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            {Object.keys(data.sample_data[0]).map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.sample_data.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Overview;
