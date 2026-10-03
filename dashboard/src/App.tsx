import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Battery, Sun, Zap, BrainCircuit, Link, Power } from 'lucide-react'
import './App.css'

function App() {
  const [currentData, setCurrentData] = useState(null)
  const [history, setHistory] = useState([])
  const [ledger, setLedger] = useState([])
  const [aiEnabled, setAiEnabled] = useState(true) // NAYA: Toggle State

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/telemetry')
        setCurrentData(response.data)
        setAiEnabled(response.data.ai_enabled) // Server se sync
        
        setHistory(prev => {
          const newHistory = [...prev, response.data]
          if (newHistory.length > 15) newHistory.shift()
          return newHistory
        })

        const ledgerRes = await axios.get('http://localhost:8000/ledger')
        setLedger(ledgerRes.data)
      } catch (error) {
        console.error("API Error", error)
      }
    }

    const interval = setInterval(fetchData, 2000)
    return () => clearInterval(interval)
  }, [])

  // NAYA: Button click hone par Waiter ko naya signal bhejna
  const handleToggleAI = async () => {
    const newState = !aiEnabled
    setAiEnabled(newState)
    try {
      await axios.post('http://localhost:8000/toggle-ai', { ai_enabled: newState })
    } catch (error) {
      console.error("Toggle Failed", error)
    }
  }

  if (!currentData) return <div style={{ padding: '50px', fontSize: '24px' }}>Loading GridMind AI...</div>

  const batteryColor = currentData.battery_soc > 20 ? "#4ade80" : "#f87171"

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#1e1e2f', color: 'white', minHeight: '100vh' }}>
      
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h1 style={{ color: '#4ade80', margin: '0 0 10px 0' }}>⚡ GridMind: Smart Microgrid AI ⚡</h1>
        <p style={{ fontSize: '18px', margin: '0 0 20px 0' }}>Live Time: <b>{currentData.hour}</b></p>
        
        {/* NAYA: The Toggle Button */}
        <button 
          onClick={handleToggleAI}
          style={{
            backgroundColor: aiEnabled ? '#c084fc' : '#ef4444',
            color: 'white', border: 'none', padding: '12px 24px', borderRadius: '30px',
            cursor: 'pointer', fontSize: '18px', fontWeight: 'bold', display: 'inline-flex',
            alignItems: 'center', gap: '10px', transition: '0.3s', boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
          }}
        >
          <Power size={24} />
          {aiEnabled ? "AI Brain is ON" : "AI Brain is OFF"}
        </button>
      </div>

      <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap', alignItems: 'stretch' }}>
        <Card title="Solar Power" value={`${currentData.solar_kw} kW`} color="#fbbf24" icon={<Sun />} />
        <Card title="Demand (Load)" value={`${currentData.demand_kw} kW`} color="#f87171" icon={<Zap />} />
        
        <div style={{ backgroundColor: '#282a36', padding: '20px', borderRadius: '10px', width: '220px', textAlign: 'center', borderBottom: `4px solid ${batteryColor}`, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: batteryColor, marginBottom: '10px' }}>
            <h3 style={{ margin: 0 }}>Battery SoC</h3>
            <Battery />
          </div>
          <div style={{ height: '120px', overflow: 'hidden' }}>
            <PieChart width={220} height={220} style={{ margin: '0 auto', transform: 'translateY(-20px)' }}>
              <Pie
                data={[{ name: 'Charged', value: currentData.battery_soc }, { name: 'Empty', value: 100 - currentData.battery_soc }]}
                cx="50%" cy="50%" startAngle={180} endAngle={0} innerRadius={60} outerRadius={80} dataKey="value" stroke="none"
              >
                <Cell fill={batteryColor} />
                <Cell fill="#374151" />
              </Pie>
            </PieChart>
          </div>
          <h2 style={{ margin: '-20px 0 0 0', fontSize: '28px', color: batteryColor }}>{currentData.battery_soc}%</h2>
        </div>

        <Card title="Grid Import" value={`${currentData.grid_import_kw} kW`} color="#60a5fa" icon={<Zap />} />
      </div>

      <div style={{ margin: '30px auto', maxWidth: '800px', backgroundColor: aiEnabled ? '#374151' : '#451a1a', padding: '20px', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '15px', border: `1px solid ${aiEnabled ? '#c084fc' : '#ef4444'}` }}>
        <BrainCircuit size={40} color={aiEnabled ? "#c084fc" : "#ef4444"} />
        <div>
          <h3 style={{ margin: 0, color: aiEnabled ? "#c084fc" : "#ef4444" }}>
            {aiEnabled ? "AI Brain Action" : "System Warning"}
          </h3>
          <p style={{ margin: '5px 0 0 0', fontSize: '18px' }}>{currentData.action_reason}</p>
        </div>
      </div>

      <div style={{ height: '400px', maxWidth: '900px', margin: '0 auto', backgroundColor: '#282a36', padding: '20px', borderRadius: '10px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={history}>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis dataKey="hour" stroke="#aaa" />
            <YAxis stroke="#aaa" />
            <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none' }} />
            <Legend />
            <Line type="monotone" dataKey="solar_kw" name="Solar (kW)" stroke="#fbbf24" strokeWidth={3} />
            <Line type="monotone" dataKey="demand_kw" name="Demand (kW)" stroke="#f87171" strokeWidth={3} />
            <Line type="monotone" dataKey="battery_soc" name="Battery (kWh)" stroke={batteryColor} strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ maxWidth: '900px', margin: '30px auto', backgroundColor: '#282a36', padding: '20px', borderRadius: '10px' }}>
        <h2 style={{ color: '#4ade80', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Link size={24} /> Live Carbon Blockchain
        </h2>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #444', color: '#aaa' }}>
              <th style={{ padding: '10px' }}>Time</th>
              <th>Solar Used (kWh)</th>
              <th>CO2 Saved (kg)</th>
              <th>Secure Hash (SHA-256)</th>
            </tr>
          </thead>
          <tbody>
            {ledger.map((record, index) => (
              <tr key={index} style={{ borderBottom: '1px solid #444' }}>
                <td style={{ padding: '10px' }}>{new Date(record.timestamp).toLocaleTimeString()}</td>
                <td style={{ color: '#fbbf24' }}>{record.solar_kwh.toFixed(1)}</td>
                <td style={{ color: '#4ade80' }}>{record.avoided_kg_co2}</td>
                <td style={{ fontFamily: 'monospace', color: '#a78bfa', fontSize: '14px' }}>
                  {record.hash.substring(0, 24)}...
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  )
}

function Card({ title, value, color, icon }) {
  return (
    <div style={{ backgroundColor: '#282a36', padding: '20px', borderRadius: '10px', width: '200px', borderBottom: `4px solid ${color}`, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', color: color }}>
        <h3 style={{ margin: 0 }}>{title}</h3>
        {icon}
      </div>
      <h2 style={{ margin: '15px 0 0 0', fontSize: '28px' }}>{value}</h2>
    </div>
  )
}

export default App