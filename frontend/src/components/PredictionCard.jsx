import React, { useEffect, useState } from 'react';
import { ShieldAlert, ShieldCheck, Gauge } from 'lucide-react';

const PredictionCard = ({ result }) => {
  const [animatedProb, setAnimatedProb] = useState(0);

  useEffect(() => {
    if (!result) return;
    
    const target = result.probability * 100;
    let start = 0;
    const duration = 1000;
    const steps = 100;
    const increment = target / steps;
    const stepTime = duration / steps;
    
    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        setAnimatedProb(target);
        clearInterval(timer);
      } else {
        setAnimatedProb(start);
      }
    }, stepTime);
    
    return () => clearInterval(timer);
  }, [result]);

  if (!result) {
    return (
      <div className="bg-white border-4 border-black p-8 shadow-neo h-full flex flex-col justify-center items-center">
         <span className="text-2xl font-black uppercase text-center text-gray-400">WAITING FOR DATA...</span>
         <span className="text-xl mt-4 font-bold border-4 border-gray-200 px-6 py-2">NO PREDICTION YET</span>
      </div>
    );
  }

  const { prediction, confidence, risk_level } = result;
  
  // Status logic
  let statusBg = 'bg-yellow-100';
  let StatusIcon = ShieldAlert;
  
  if (risk_level === 'Low') {
    statusBg = 'bg-green-400';
    StatusIcon = ShieldCheck;
  } else if (risk_level === 'Medium') {
    statusBg = 'bg-yellow-400';
  } else {
    statusBg = 'bg-red-400';
  }

  return (
    <div className={`border-4 border-black p-8 shadow-neo transition-colors duration-500 animate-slideDown ${statusBg} flex flex-col gap-6`}>
      
      {/* BIG RESULT */}
      <div className="bg-white border-4 border-black p-6 shadow-neo-sm text-center">
        <h2 className="text-2xl font-bold uppercase mb-2">DELIVERY RELIABILITY</h2>
        <div className="text-7xl font-black text-black">
          {animatedProb.toFixed(1)}%
        </div>
        <div className="text-3xl font-black uppercase tracking-widest mt-2">{prediction}</div>
      </div>

      <div className="grid grid-cols-2 gap-4">
         {/* CONFIDENCE */}
         <div className="bg-white border-4 border-black p-4 shadow-neo-sm flex flex-col items-center justify-center">
            <Gauge size={40} className="mb-2" />
            <span className="text-sm font-bold uppercase tracking-wide">CONFIDENCE</span>
            <span className="text-2xl font-black">{confidence}</span>
         </div>
         
         {/* RISK LEVEL */}
         <div className="bg-white border-4 border-black p-4 shadow-neo-sm flex flex-col items-center justify-center">
            <StatusIcon size={40} className="mb-2" />
            <span className="text-sm font-bold uppercase tracking-wide">RISK LEVEL</span>
            <span className="text-2xl font-black">{risk_level}</span>
         </div>
      </div>
      
    </div>
  );
};

export default PredictionCard;
