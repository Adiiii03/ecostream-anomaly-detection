import { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { AlertTriangle, CheckCircle, Activity, Thermometer, Zap, Gauge } from 'lucide-react';
import './App.css';

export default function App() {
  const [data, setData] = useState([]);
  const [latest, setLatest] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/readings');
      const reversedData = [...response.data].reverse();
      setData(reversedData);
      
      if (response.data.length > 0) {
        setLatest(response.data[0]);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const isCritical = latest?.status === "CRITICAL";

  return (
    <div className={`dashboard ${isCritical ? 'critical-bg' : ''}`}>
      <div className="container">
        
        {/* Header */}
        <header className="header">
          <div className="logo-section">
            <Activity className="icon-blue" size={40} />
            <h1>EcoStream <span style={{fontWeight: 300, opacity: 0.7}}>Industrial AI</span></h1>
          </div>
          <div className={`status-badge ${isCritical ? 'status-critical' : 'status-normal'}`}>
            {isCritical ? <AlertTriangle size={24} /> : <CheckCircle size={24} />}
            <span>{latest?.status || "SYSTEM OFFLINE"}</span>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="stats-grid">
          {/* Temperature Card */}
          <div className={`card ${isCritical ? 'card-critical' : ''}`}>
            <div style={{display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '10px'}}>
              <Thermometer size={20} color={isCritical ? "#ef4444" : "#38bdf8"} />
              <h3>Temperature</h3>
            </div>
            <p className={`stat-value ${isCritical ? 'text-red' : 'text-blue'}`}>
              {latest?.temperature?.toFixed(1) || '--'}°C
            </p>
          </div>

          {/* Pressure Card */}
          <div className="card">
            <div style={{display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '10px'}}>
              <Gauge size={20} color="#a855f7" />
              <h3>Pressure</h3>
            </div>
            <p className="stat-value text-purple">
              {latest?.pressure?.toFixed(1) || '--'} <span style={{fontSize: '1.5rem'}}>PSI</span>
            </p>
          </div>

          {/* Vibration Card */}
          <div className="card">
            <div style={{display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '10px'}}>
              <Zap size={20} color="#fbbf24" />
              <h3>Vibration</h3>
            </div>
            <p className="stat-value" style={{color: '#fbbf24'}}>
              {latest?.vibration?.toFixed(1) || '--'} <span style={{fontSize: '1.5rem'}}>Hz</span>
            </p>
          </div>
        </div>

        {/* Main Chart */}
        <div className="chart-container">
          <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '20px'}}>
            <h2>Live Sensor Telemetry</h2>
            <div style={{fontSize: '0.9rem', color: '#94a3b8'}}>Updates every 2s</div>
          </div>
          
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={isCritical ? "#ef4444" : "#38bdf8"} stopOpacity={0.3}/>
                    <stop offset="95%" stopColor={isCritical ? "#ef4444" : "#38bdf8"} stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis 
                  dataKey="timestamp" 
                  tickFormatter={(t) => new Date(t).toLocaleTimeString()} 
                  stroke="#94a3b8"
                  tick={{fill: '#94a3b8'}}
                />
                <YAxis 
                  domain={['auto', 'auto']} 
                  stroke="#94a3b8"
                  tick={{fill: '#94a3b8'}}
                />
                <Tooltip 
                  contentStyle={{backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#fff'}}
                  labelStyle={{color: '#94a3b8'}}
                />
                <Area 
                  type="monotone" 
                  dataKey="temperature" 
                  stroke={isCritical ? "#ef4444" : "#38bdf8"} 
                  strokeWidth={3}
                  fillOpacity={1} 
                  fill="url(#colorTemp)" 
                  animationDuration={500}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}