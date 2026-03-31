import React, { useState, useEffect } from 'react';
import InputForm from '../components/InputForm';
import PredictionCard from '../components/PredictionCard';
import PredictionHistory from '../components/PredictionHistory';
import { predictDelivery } from '../services/api';
import { Info } from 'lucide-react';

const Dashboard = () => {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [errorMsg, setErrorMsg] = useState('');

  // Load history from localStorage on initial render
  useEffect(() => {
    const saved = localStorage.getItem('shipmentsure_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to parse history");
      }
    }
  }, []);

  const handlePredict = async (formData) => {
    setIsLoading(true);
    setErrorMsg('');
    try {
      const data = await predictDelivery(formData);
      setResult(data);

      // Update history
      const newRecord = {
        id: Math.floor(Math.random() * 90000) + 10000,
        ...data
      };

      const updatedHistory = [newRecord, ...history].slice(0, 10);
      setHistory(updatedHistory);
      localStorage.setItem('shipmentsure_history', JSON.stringify(updatedHistory));

    } catch (error) {
      setErrorMsg(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-6 md:p-12 font-sans overflow-hidden">

      {/* HEADER */}
      <header className="mb-12 text-center relative z-10 transition-transform hover:-translate-y-1">
        <div className="flex justify-center mb-4">
           <span className="bg-black text-white px-3 py-1 font-bold text-sm tracking-widest border-2 border-black inline-block shadow-neo-sm transform -rotate-2">
              V1.0 • ML POWERED
           </span>
        </div>
        <h1 className="text-5xl md:text-7xl flex justify-center items-center font-black uppercase text-black italic tracking-tighter drop-shadow-neo">
          <span className="bg-primary px-4 border-4 border-black inline-flex items-center shadow-neo">
            ShipmentSure AI
            <span title="This model predicts delivery reliability using XGBoost ML algorithm" className="ml-4 cursor-help inline-flex items-center justify-center text-black hover:text-gray-700 transition-colors">
              <Info size={40} strokeWidth={3} />
            </span>
          </span>
        </h1>
        <p className="mt-6 text-xl md:text-2xl font-bold bg-white inline-block border-4 border-black px-6 py-2 shadow-neo-sm transform -rotate-1">
          AI-powered delivery prediction system
        </p>
      </header>

      {errorMsg && (
        <div className="max-w-4xl mx-auto mb-8 bg-danger border-4 border-black p-4 text-center font-bold text-white shadow-neo">
          ERROR: {errorMsg}
        </div>
      )}

      {/* MAIN CONTENT */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12">

        {/* LEFT PANEL: INPUT */}
        <div className="lg:col-span-7">
          <InputForm onSubmit={handlePredict} isLoading={isLoading} />
        </div>

        {/* RIGHT PANEL: OUTPUT */}
        <div className="lg:col-span-5 flex flex-col">
          <PredictionCard result={result} />

          {history.length > 0 && (
            <PredictionHistory history={history} />
          )}
        </div>
      </div>

      {/* FOOTER */}
      <footer className="mt-20 text-center text-gray-500 text-sm font-bold tracking-widest uppercase">
        © 2026 ShipmentSure AI • Designed with Precision
      </footer>
    </div>
  );
};

export default Dashboard;
