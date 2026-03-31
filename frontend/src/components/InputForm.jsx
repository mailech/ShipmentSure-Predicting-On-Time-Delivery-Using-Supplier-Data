import React, { useState } from 'react';

const InputForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    Warehouse_block: 'A',
    Mode_of_Shipment: 'Flight',
    Product_importance: 'low',
    Customer_care_calls: 3,
    Customer_rating: 3,
    Prior_purchases: 3,
    Discount_offered: 10,
    Weight_in_gms: 2000
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const inputClass = "w-full border-4 border-black p-3 bg-white font-bold focus:outline-none focus:ring-0 shadow-neo-hover transition-all mt-1";
  const labelClass = "text-xl font-bold uppercase tracking-wide";

  return (
    <form onSubmit={handleSubmit} className="bg-yellow-100 border-4 border-black p-8 shadow-neo max-w-2xl mx-auto flex flex-col gap-6">

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Dropdowns */}
        <div>
          <label className={labelClass}>WAREHOUSE BLOCK</label>
          <select name="Warehouse_block" value={formData.Warehouse_block} onChange={handleChange} className={inputClass}>
            {['A', 'B', 'C', 'D', 'F'].map(opt => <option key={opt} value={opt}>{opt}</option>)}
          </select>
        </div>

        <div>
          <label className={labelClass}>MODE OF SHIPMENT</label>
          <select name="Mode_of_Shipment" value={formData.Mode_of_Shipment} onChange={handleChange} className={inputClass}>
            {['Flight', 'Ship', 'Road'].map(opt => <option key={opt} value={opt}>{opt}</option>)}
          </select>
        </div>

        <div>
          <label className={labelClass}>PRODUCT IMPORTANCE</label>
          <select name="Product_importance" value={formData.Product_importance} onChange={handleChange} className={inputClass}>
            {['low', 'medium', 'high'].map(opt => <option key={opt} value={opt}>{opt}</option>)}
          </select>
        </div>

        {/* Numbers */}
        <div>
          <label className={labelClass}>CUSTOMER CARE CALLS</label>
          <input type="number" name="Customer_care_calls" value={formData.Customer_care_calls} onChange={handleChange} className={inputClass} />
        </div>

        <div>
          <label className={labelClass}>CUSTOMER RATING (1-5)</label>
          <input type="number" min="1" max="5" name="Customer_rating" value={formData.Customer_rating} onChange={handleChange} className={inputClass} />
        </div>

        <div>
          <label className={labelClass}>PRIOR PURCHASES</label>
          <input type="number" name="Prior_purchases" value={formData.Prior_purchases} onChange={handleChange} className={inputClass} />
        </div>

        <div>
          <label className={labelClass}>DISCOUNT OFFERED (%)</label>
          <input type="number" name="Discount_offered" value={formData.Discount_offered} onChange={handleChange} className={inputClass} />
        </div>

        <div>
          <label className={labelClass}>WEIGHT (g)</label>
          <input type="number" name="Weight_in_gms" value={formData.Weight_in_gms} onChange={handleChange} className={inputClass} />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="mt-6 w-full p-4 border-4 border-black bg-primary text-2xl font-black uppercase shadow-neo hover:translate-y-1 hover:shadow-neo-hover active:translate-y-2 active:shadow-none transition-all disabled:opacity-50"
      >
        {isLoading ? 'ANALYZING SHIPMENT...' : 'PREDICT DELIVERY'}
      </button>

    </form>
  );
};

export default InputForm;
