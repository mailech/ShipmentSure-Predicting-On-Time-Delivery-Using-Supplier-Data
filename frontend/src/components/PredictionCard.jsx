import React, { useEffect, useState } from 'react';
import { ShieldAlert, ShieldCheck, Gauge, SlidersHorizontal, RefreshCw } from 'lucide-react';

const PredictionCard = ({ result, lastInput, onWhatIf, isLoading }) => {
  const [animatedProb, setAnimatedProb] = useState(0);
  const [whatIfData, setWhatIfData] = useState(lastInput);
  const [isTweaked, setIsTweaked] = useState(false);

  useEffect(() => {
    if (lastInput && !isTweaked) {
      setWhatIfData(lastInput);
    }
  }, [lastInput, isTweaked]);

  const handleSliderChange = (e) => {
    const { name, value } = e.target;
    setWhatIfData(prev => ({ ...prev, [name]: Number(value) }));
    setIsTweaked(true);
  };

  const applyWhatIf = () => {
    if (onWhatIf && whatIfData) {
      onWhatIf(whatIfData);
      setIsTweaked(false);
    }
  };
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
      
      {/* WHAT-IF SCENARIOS */}
      {whatIfData && (
        <div className="bg-white border-4 border-black p-6 shadow-neo-sm mt-2 relative">
           <h3 className="text-xl font-black uppercase mb-4 flex items-center gap-2">
             <SlidersHorizontal size={24} /> What-If Analysis
           </h3>
           
           <div className="flex flex-col gap-4">
             {/* Discount Slider */}
             <div>
               <div className="flex justify-between font-bold mb-1">
                 <label className="text-sm uppercase tracking-wide">Discount Offered</label>
                 <span>{whatIfData.Discount_offered}%</span>
               </div>
               <input 
                 type="range" 
                 name="Discount_offered" 
                 min="0" 
                 max="65" 
                 value={whatIfData.Discount_offered} 
                 onChange={handleSliderChange}
                 className="w-full accent-black cursor-pointer"
               />
             </div>
             
             {/* Weight Slider */}
             <div>
               <div className="flex justify-between font-bold mb-1">
                 <label className="text-sm uppercase tracking-wide">Weight (g)</label>
                 <span>{whatIfData.Weight_in_gms}g</span>
               </div>
               <input 
                 type="range" 
                 name="Weight_in_gms" 
                 min="1000" 
                 max="10000" 
                 step="100"
                 value={whatIfData.Weight_in_gms} 
                 onChange={handleSliderChange}
                 className="w-full accent-black cursor-pointer"
               />
             </div>
             
             {/* Action */}
             <button 
               onClick={applyWhatIf}
               disabled={!isTweaked || isLoading}
               className={`w-full p-3 mt-4 border-4 border-black font-black uppercase transition-all flex justify-center items-center gap-2
                 ${isTweaked && !isLoading ? 'bg-black text-white hover:bg-gray-800 shadow-neo-sm' : 'bg-gray-200 text-gray-400 cursor-not-allowed'}
               `}
             >
               {isLoading ? (
                  <RefreshCw className="animate-spin" size={20} />
               ) : (
                 'Recalculate Probability'
               )}
             </button>
           </div>
        </div>
      )}

    </div>
  );
};

export default PredictionCard;
