import React from 'react';

const PredictionHistory = ({ history }) => {
  if (!history || history.length === 0) return null;

  return (
    <div className="bg-white border-4 border-black p-6 shadow-neo mt-8">
      <h3 className="text-2xl font-black uppercase mb-4 text-center">Recent Checks</h3>
      
      <div className="overflow-x-auto border-4 border-black">
        <table className="min-w-full bg-white divide-y-4 divide-black text-left font-bold table-auto">
          <thead className="bg-primary text-black divide-y-4 divide-black">
            <tr>
              <th className="px-4 py-3 uppercase border-r-4 border-black border-collapse">ID</th>
              <th className="px-4 py-3 uppercase border-r-4 border-black border-collapse">Prediction</th>
              <th className="px-4 py-3 uppercase">Risk</th>
            </tr>
          </thead>
          <tbody className="divide-y-4 divide-black">
            {history.map((record, index) => (
              <tr key={index} className="hover:bg-yellow-100 transition-colors">
                <td className="px-4 py-3 border-r-4 border-black">#{record.id}</td>
                <td className="px-4 py-3 border-r-4 border-black">{(record.probability * 100).toFixed(1)}%</td>
                <td className="px-4 py-3">
                  <span className={`px-2 border-2 border-black inline-block text-center ${record.risk_level === 'Low' ? 'bg-success' : record.risk_level === 'Medium' ? 'bg-yellow-400' : 'bg-danger'}`}>
                    {record.risk_level}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PredictionHistory;
