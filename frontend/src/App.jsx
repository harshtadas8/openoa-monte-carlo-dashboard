import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const BASE_URL =
  import.meta.env.VITE_API_URL ||
  "https://openoa-monte-carlo-dashboard.onrender.com";

function App() {
  const [data, setData] = useState(null);
  const [numSim, setNumSim] = useState(100);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
  setLoading(true);

  try {
    const res = await fetch(`${BASE_URL}/analysis/aep`);

    if (!res.ok) {
      throw new Error("Backend error");
    }

    const result = await res.json();
    setData(result);

  } catch (err) {
    console.error("Fetch error:", err);

    // 🔥 IMPORTANT: Stop spinner even on error
    setData(null);

  } finally {
    setLoading(false);
  }
};
  useEffect(() => {
    fetchData();
  }, []);

  const handleRunClick = () => {
    fetchData();
  };

  if (loading) {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <h2>Loading Monte Carlo Results...</h2>
    </div>
  );
}

if (!data) {
  return (
    <div className="loading-container">
      <h2>Unable to load data. Please refresh.</h2>
    </div>
  );
}

  const bins = 12;
  const min = Math.min(...data.distribution);
  const max = Math.max(...data.distribution);
  const step = (max - min) / bins;

  const histogram = Array.from({ length: bins }, (_, i) => {
    const lower = min + i * step;
    const upper = lower + step;
    const count = data.distribution.filter(
      (v) => v >= lower && v < upper
    ).length;

    return {
      range: `${lower.toFixed(2)} - ${upper.toFixed(2)}`,
      count,
    };
  });

  return (
    <div className="page">
      <div className="content">
        <h1 className="title">Monte Carlo AEP Risk Dashboard</h1>

        <div className="control-wrapper">
          <div className="control-box">
            <label>Simulations</label>
            <select
              value={numSim}
              onChange={(e) => setNumSim(parseInt(e.target.value))}
            >
              <option value={100}>100</option>
              <option value={300}>300</option>
              <option value={500}>500</option>
              <option value={1000}>1000</option>
            </select>

            <button onClick={handleRunClick}>
              Run Simulation
            </button>
          </div>
        </div>

        <div className="card-grid">
          <MetricCard title="Mean AEP (GWh)" value={data.mean_aep_GWh.toFixed(2)} />
          <MetricCard title="P50 (GWh)" value={data.p50_GWh.toFixed(2)} />
          <MetricCard title="P90 (GWh)" value={data.p90_GWh.toFixed(2)} />
          <MetricCard title="Std Dev" value={data.std_dev.toFixed(2)} />
        </div>

        <div className={`risk-panel ${data.risk.color}`}>
          <h2>Risk Assessment</h2>
          <p><strong>Level:</strong> {data.risk.level}</p>
          <p><strong>P50 - P90 Spread:</strong> {data.risk.spread} GWh</p>
          <p>{data.risk.description}</p>
        </div>

        <h2 className="section-title">AEP Distribution</h2>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height={420}>
            <BarChart data={histogram}>
              <XAxis dataKey="range" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{ backgroundColor: "#1e293b", border: "none" }}
                labelStyle={{ color: "#fff" }}
              />
              <Bar dataKey="count" fill="#38bdf8" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

export default App;