import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import ModelInsights from './pages/ModelInsights';
import { Database, LineChart } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('predictor');

  return (
    <div className="min-h-screen bg-background font-sans">
      
      {/* TABS CONSOLE */}
      <div className="bg-white border-b-8 border-black p-4 flex justify-center gap-4 relative z-50">
        <button 
          onClick={() => setActiveTab('predictor')}
          className={`flex items-center gap-2 px-6 py-3 border-4 border-black font-black text-xl uppercase transition-transform ${activeTab === 'predictor' ? 'bg-primary translate-y-1 shadow-none' : 'bg-white hover:-translate-y-1 shadow-neo-hover relative top-1'}`}
        >
          <Database strokeWidth={3} size={24} />
          UI Predictor
        </button>
        
        <button 
          onClick={() => setActiveTab('insights')}
          className={`flex items-center gap-2 px-6 py-3 border-4 border-black font-black text-xl uppercase transition-transform ${activeTab === 'insights' ? 'bg-blue-300 translate-y-1 shadow-none' : 'bg-white hover:-translate-y-1 shadow-neo-hover relative top-1'}`}
        >
          <LineChart strokeWidth={3} size={24} />
          Model Insights
        </button>
      </div>

      {/* RENDER ACTIVE TAB */}
      <div className={activeTab === 'insights' ? "p-6 md:p-12 animate-slideDown" : ""}>
        {activeTab === 'predictor' ? <Dashboard /> : <ModelInsights />}
      </div>
    </div>
  );
}

export default App;
