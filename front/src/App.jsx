import { useState } from 'react'
import axios from 'axios'
import { Truck, AlertTriangle, CheckCircle, Package, Phone, Star, DollarSign, Repeat, ArrowRight, User, Percent, Scale } from 'lucide-react'

function App() {
  const [formData, setFormData] = useState({
    Warehouse_block: 'A',
    Mode_of_Shipment: 'Flight',
    Customer_care_calls: 4,
    Customer_rating: 3,
    Cost_of_the_Product: 200,
    Prior_purchases: 3,
    Product_importance: 'medium',
    Gender: 'F',
    Discount_offered: 10,
    Weight_in_gms: 1500
  })

  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: ['Customer_care_calls', 'Customer_rating', 'Cost_of_the_Product', 'Prior_purchases', 'Discount_offered', 'Weight_in_gms'].includes(name) 
        ? parseFloat(value) 
        : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Assuming backend is running on localhost:8000
      const response = await axios.post('http://localhost:8000/predict', formData)
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to the backend server. Make sure it is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header style={{ marginBottom: '3rem' }}>
        <h1>AI ShipmentSure</h1>
        <p style={{ color: '#94a3b8', fontSize: '1.2rem', maxWidth: '600px', margin: '0.5rem auto' }}>
          Intelligent delivery prediction using state-of-the-art supply chain analytics.
        </p>
      </header>

      <main className="glass-card" style={{ padding: '2.5rem', marginBottom: '4rem', maxWidth: '1000px', margin: '0 auto' }}>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label><Package size={14} style={{ marginRight: '4px' }} /> Warehouse Block</label>
              <select name="Warehouse_block" value={formData.Warehouse_block} onChange={handleChange}>
                {['A', 'B', 'C', 'D', 'F'].map(block => <option key={block} value={block}>{block}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label><Truck size={14} style={{ marginRight: '4px' }} /> Shipment Mode</label>
              <select name="Mode_of_Shipment" value={formData.Mode_of_Shipment} onChange={handleChange}>
                {['Flight', 'Ship', 'Road'].map(mode => <option key={mode} value={mode}>{mode}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label><Phone size={14} style={{ marginRight: '4px' }} /> Care Calls</label>
              <input type="number" name="Customer_care_calls" value={formData.Customer_care_calls} min="2" max="7" onChange={handleChange} />
            </div>

            <div className="form-group">
              <label><Star size={14} style={{ marginRight: '4px' }} /> Customer Rating</label>
              <input type="number" name="Customer_rating" value={formData.Customer_rating} min="1" max="5" onChange={handleChange} />
            </div>

            <div className="form-group">
              <label><DollarSign size={14} style={{ marginRight: '4px' }} /> Product Cost ($)</label>
              <input type="number" name="Cost_of_the_Product" value={formData.Cost_of_the_Product} onChange={handleChange} />
            </div>

            <div className="form-group">
              <label><Repeat size={14} style={{ marginRight: '4px' }} /> Prior Purchases</label>
              <input type="number" name="Prior_purchases" value={formData.Prior_purchases} min="2" max="10" onChange={handleChange} />
            </div>

            <div className="form-group">
              <label><AlertTriangle size={14} style={{ marginRight: '4px' }} /> Importance</label>
              <select name="Product_importance" value={formData.Product_importance} onChange={handleChange}>
                {['low', 'medium', 'high'].map(imp => <option key={imp} value={imp}>{imp}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label><User size={14} style={{ marginRight: '4px' }} /> Gender</label>
              <select name="Gender" value={formData.Gender} onChange={handleChange}>
                <option value="F">Female</option>
                <option value="M">Male</option>
              </select>
            </div>

            <div className="form-group">
              <label><Percent size={14} style={{ marginRight: '4px' }} /> Discount (%)</label>
              <input type="number" name="Discount_offered" value={formData.Discount_offered} min="0" max="100" onChange={handleChange} />
            </div>

            <div className="form-group">
              <label><Scale size={14} style={{ marginRight: '4px' }} /> Weight (gms)</label>
              <input type="number" name="Weight_in_gms" value={formData.Weight_in_gms} onChange={handleChange} />
            </div>
          </div>

          <div style={{ marginTop: '2.5rem', textAlign: 'center' }}>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div className="pulse" style={{ width: '8px', height: '8px', background: 'white', borderRadius: '50%' }}></div>
                  Analyzing Data...
                </span>
              ) : (
                <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  Predict Delivery Status <ArrowRight size={18} />
                </span>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="result-box" style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', color: '#f87171', marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
              <AlertTriangle />
              <span>{error}</span>
            </div>
          </div>
        )}

        {result && (
          <div className={`result-box ${result.prediction === 1 ? 'status-on-time' : 'status-delayed'}`}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
              {result.prediction === 1 ? (
                <CheckCircle size={48} strokeWidth={2.5} />
              ) : (
                <AlertTriangle size={48} strokeWidth={2.5} />
              )}
              <h2 style={{ margin: 0, fontSize: '2rem', color: 'inherit' }}>
                {result.status === 'On Time' ? 'EXPECTED ON TIME' : 'SHIPMENT DELAYED'}
              </h2>
              <div style={{ background: 'rgba(255, 255, 255, 0.1)', padding: '0.5rem 1.5rem', borderRadius: '20px', fontSize: '0.875rem' }}>
                Confidence Score: {(result.confidence * 100).toFixed(2)}%
              </div>
            </div>
          </div>
        )}
      </main>

      <footer style={{ marginTop: '4rem', paddingBottom: '2rem', color: '#64748b', fontSize: '0.875rem' }}>
        <p>&copy; 2026 AI ShipmentSure &bull; Built with FastAPI & React</p>
      </footer>
    </div>
  )
}

export default App
