import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Brain, Target, ShieldCheck } from 'lucide-react';

const insightData = [
  { name: 'Discount Offered', importance: 71.3, color: '#fef08a' },
  { name: 'Prior Purchases', importance: 5.4, color: '#86efac' },
  { name: 'Weight (g)', importance: 5.3, color: '#93c5fd' },
  { name: 'Care Calls', importance: 2.0, color: '#fca5a5' },
  { name: 'Shipping Mode', importance: 1.5, color: '#d8b4fe' },
  { name: 'All Others', importance: 1.5, color: '#d1d5db' }
];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border-4 border-black p-4 shadow-neo">
        <p className="font-bold uppercase">{payload[0].payload.name}</p>
        <p className="font-black text-2xl">{payload[0].value}% Impact</p>
      </div>
    );
  }
  return null;
};

const ModelInsights = () => {
  return (
    <div className="animate-slideDown">
      {/* METRICS ROW */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {/* Metric 1 */}
        <div className="bg-green-300 border-4 border-black p-6 shadow-neo flex flex-col items-center text-center transform hover:-translate-y-1 transition-transform">
          <Target size={48} className="mb-4" strokeWidth={2.5} />
          <div className="text-sm font-bold uppercase tracking-widest mb-2">CV Accuracy Rate</div>
          <div className="text-5xl font-black">68.3%</div>
          <div className="mt-2 text-sm font-semibold italic bg-white border-2 border-black px-2 py-1 transform rotate-1">Mathematical Ceiling</div>
        </div>

        {/* Metric 2 */}
        <div className="bg-yellow-300 border-4 border-black p-6 shadow-neo flex flex-col items-center text-center transform hover:-translate-y-1 transition-transform">
          <ShieldCheck size={48} className="mb-4" strokeWidth={2.5} />
          <div className="text-sm font-bold uppercase tracking-widest mb-2">Primary Rule Engine</div>
          <div className="text-3xl font-black uppercase mt-2">Discount &gt; 10%</div>
          <div className="mt-2 text-sm font-bold">= 100% On-Time Trigger</div>
        </div>

        {/* Metric 3 */}
        <div className="bg-blue-300 border-4 border-black p-6 shadow-neo flex flex-col items-center text-center transform hover:-translate-y-1 transition-transform">
          <Brain size={48} className="mb-4" strokeWidth={2.5} />
          <div className="text-sm font-bold uppercase tracking-widest mb-2">Algorithm Class</div>
          <div className="text-3xl font-black mt-2 uppercase">XGBoost API</div>
          <div className="mt-2 text-sm font-bold bg-white border-2 border-black px-2 py-1 transform -rotate-2">RandomizedSearchCV</div>
        </div>
      </div>

      {/* CHART SECTION */}
      <div className="bg-white border-4 border-black p-8 shadow-neo mb-12">
        <h2 className="text-3xl font-black uppercase mb-6 flex items-center gap-4">
          <span className="bg-black text-white px-2 py-1">#1</span> Structural Feature Importance
        </h2>
        
        <p className="text-lg font-semibold mb-8 border-l-8 border-primary pl-4 py-2 bg-gray-50">
          The chart below illustrates exactly <span className="font-bold italic">how</span> the ML model makes its internal decisions. 
          As shown, over <strong className="bg-yellow-200 px-1 border border-black">71%</strong> of its entire predictive weight relies solely on the Discount threshold, while physical traits like product weight serve as secondary validation checks.
        </p>

        <div className="h-[32rem] w-full border-4 border-black bg-gray-50 p-4 shadow-inner">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={insightData}
              margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
            >
              <XAxis 
                dataKey="name" 
                height={100}
                tick={{ fill: 'black', fontWeight: 'bold' }} 
                axisLine={{ stroke: 'black', strokeWidth: 4 }}
                tickLine={{ stroke: 'black', strokeWidth: 4 }}
                angle={-45}
                textAnchor="end"
              />
              <YAxis 
                tick={{ fill: 'black', fontWeight: 'bold' }}
                axisLine={{ stroke: 'black', strokeWidth: 4 }}
                tickLine={{ stroke: 'black', strokeWidth: 4 }}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.1)' }} />
              <Bar 
                dataKey="importance" 
                stroke="black"
                strokeWidth={3}
              >
                {insightData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* FOOTER TEXT PLACED INSIDE TO MATCH HEIGHT */}
      <div className="bg-red-300 border-4 border-black p-6 shadow-neo relative overflow-hidden group">
        <div className="relative z-10">
          <h3 className="text-2xl font-black uppercase mb-2">Noise Filtering 🗑️</h3>
          <p className="font-semibold text-lg max-w-4xl">
            You will notice that parameters like **Warehouse Block** and **Product Importance** barely register on the chart. 
            High-grade XGBoost estimators intelligently quarantine these as 'statistical noise', ensuring the core production logic remains robust entirely against real-world driver inputs.
          </p>
        </div>
      </div>

    </div>
  );
};

export default ModelInsights;
