import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function ArcGauge({ value, color }) {
  const arcLen = Math.PI * 60;
  const offset = arcLen - (value / 100) * arcLen;
  return (
    <svg width="160" height="95" viewBox="0 0 160 95">
      <path d="M 16 88 A 64 64 0 0 1 144 88" fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="12" strokeLinecap="round"/>
      <path d="M 16 88 A 64 64 0 0 1 144 88" fill="none" stroke={color} strokeWidth="12" strokeLinecap="round"
        strokeDasharray={arcLen} strokeDashoffset={offset}
        style={{transition:'stroke-dashoffset 1.4s cubic-bezier(0.4,0,0.2,1)', filter:`drop-shadow(0 0 8px ${color}88)`}}/>
      <text x="80" y="80" textAnchor="middle" fill="white" fontSize="26" fontWeight="700" fontFamily="'Barlow Condensed',sans-serif" letterSpacing="1">{value}%</text>
    </svg>
  );
}

function ProbBar({ label, value, color, delay }) {
  const [width, setWidth] = useState(0);
  useEffect(() => { const t = setTimeout(() => setWidth(value), 200 + delay); return () => clearTimeout(t); }, [value, delay]);
  return (
    <div className="prob-bar-wrap">
      <div className="prob-bar-label">
        <span>{label}</span>
        <span style={{color}}>{value}%</span>
      </div>
      <div className="prob-bar-track">
        <div className="prob-bar-fill" style={{width: width+'%', background: color, boxShadow:`0 0 12px ${color}66`, transition:'width 1s cubic-bezier(0.4,0,0.2,1)'}}/>
      </div>
    </div>
  );
}

const RISK_CONFIG = {
  Low:    { color: '#00e676', bg: 'rgba(0,230,118,0.12)', icon: '🟢' },
  Medium: { color: '#ffb300', bg: 'rgba(255,179,0,0.12)',  icon: '🟡' },
  High:   { color: '#ff4b4b', bg: 'rgba(255,75,75,0.12)',  icon: '🔴' },
};

export default function App() {
  const [form, setForm] = useState({
    warehouse_block:'A', mode_of_shipment:'Flight', customer_care_calls:'',
    customer_rating:'', cost_of_the_product:'', prior_purchases:'',
    product_importance:'high', gender:'M', discount_offered:'', weight_in_gms:'',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [visible, setVisible] = useState(false);
  const resultRef = useRef(null);

  const handleChange = e => setForm({...form, [e.target.name]: e.target.value});

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setError(''); setVisible(false); setResult(null);
    try {
      const res = await fetch('http://127.0.0.1:5000/predict', {
        method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(form),
      });
      const data = await res.json();
      setResult(data);
      setTimeout(() => { setVisible(true); resultRef.current?.scrollIntoView({behavior:'smooth', block:'center'}); }, 50);
    } catch {
      setError('Cannot connect to backend. Make sure Flask is running on port 5000.');
    }
    setLoading(false);
  };

  const isOnTime = result?.prediction?.includes('On Time');
  const riskCfg = result ? RISK_CONFIG[result.risk_level] : null;
  const gaugeColor = result ? (isOnTime ? '#00e676' : '#ff4b4b') : '#00d4ff';

  return (
    <div className="page">
      <div className="bg-grid"/>

      <header className="header">
        <div className="logo">
          <span className="logo-icon">⬡</span>
          <span className="logo-text">SHIPMENT<span>SURE</span></span>
        </div>
        <p className="tagline">AI-Powered On-Time Delivery Prediction</p>
      </header>

      <main className="main">
        <div className="card form-card">
          <div className="card-label">INPUT PARAMETERS</div>
          <form onSubmit={handleSubmit}>

            <div className="section-title">Shipment Details</div>
            <div className="grid-4">
              {[
                {label:'Warehouse Block', name:'warehouse_block', opts:['A','B','C','D','F']},
                {label:'Mode of Shipment', name:'mode_of_shipment', opts:['Flight','Ship','Road']},
                {label:'Product Importance', name:'product_importance', opts:['high','medium','low']},
                {label:'Gender', name:'gender', opts:[], optPairs:[['M','Male'],['F','Female']]},
              ].map(f => (
                <div className="field" key={f.name}>
                  <label>{f.label}</label>
                  <select name={f.name} value={form[f.name]} onChange={handleChange}>
                    {f.optPairs ? f.optPairs.map(([v,l]) => <option key={v} value={v}>{l}</option>)
                      : f.opts.map(v => <option key={v}>{v}</option>)}
                  </select>
                </div>
              ))}
            </div>

            <div className="section-title" style={{marginTop:'24px'}}>Order Metrics</div>
            <div className="grid-3">
              {[
                {label:'Customer Care Calls', name:'customer_care_calls', ph:'e.g. 3'},
                {label:'Customer Rating (1–5)', name:'customer_rating', ph:'e.g. 4'},
                {label:'Cost of Product ($)', name:'cost_of_the_product', ph:'e.g. 200'},
                {label:'Prior Purchases', name:'prior_purchases', ph:'e.g. 3'},
                {label:'Discount Offered (%)', name:'discount_offered', ph:'e.g. 10'},
                {label:'Weight (gms)', name:'weight_in_gms', ph:'e.g. 3000'},
              ].map(f => (
                <div className="field" key={f.name}>
                  <label>{f.label}</label>
                  <input type="number" name={f.name} value={form[f.name]} onChange={handleChange} placeholder={f.ph} required/>
                </div>
              ))}
            </div>

            {error && <div className="error-msg">⚠ {error}</div>}

            <button type="submit" className="predict-btn" disabled={loading}>
              {loading ? <span className="spinner"/> : null}
              {loading ? 'Analyzing...' : 'Run Prediction →'}
            </button>
          </form>
        </div>

        {result && (
          <div className={`card result-card ${visible ? 'revealed' : ''}`} ref={resultRef}>
            <div className="card-label">PREDICTION RESULT</div>

            <div className={`verdict ${isOnTime ? 'verdict-success' : 'verdict-danger'}`}>
              <span className="verdict-icon">{isOnTime ? '✓' : '✕'}</span>
              <span className="verdict-text">{isOnTime ? 'Delivered On Time' : 'Likely Delayed'}</span>
            </div>

            <div className="metrics-row">
              <div className="metric-box">
                <div className="metric-label">CONFIDENCE</div>
                <ArcGauge value={result.confidence} color={gaugeColor}/>
                <div className="metric-sub">Model certainty</div>
              </div>

              <div className="metric-box">
                <div className="metric-label">RISK LEVEL</div>
                <div className="risk-badge" style={{background: riskCfg.bg, border:`1px solid ${riskCfg.color}44`}}>
                  <span className="risk-icon">{riskCfg.icon}</span>
                  <span className="risk-text" style={{color: riskCfg.color}}>{result.risk_level} Risk</span>
                </div>
                <div className="metric-sub">Delay probability</div>
              </div>

              <div className="metric-box">
                <div className="metric-label">RELIABILITY</div>
                <div className="reliability-score" style={{color: isOnTime ? '#00e676' : '#ff4b4b'}}>
                  {result.reliability}
                  <span className="reliability-unit">%</span>
                </div>
                <div className="metric-sub">On-time score</div>
              </div>
            </div>

            <div className="prob-section">
              <div className="prob-title">PROBABILITY BREAKDOWN</div>
              <ProbBar label="On Time" value={result.on_time_probability} color="#00e676" delay={0}/>
              <ProbBar label="Delayed" value={result.delayed_probability} color="#ff4b4b" delay={200}/>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">ShipmentSure · Infosys Springboard 2026</footer>
    </div>
  );
}