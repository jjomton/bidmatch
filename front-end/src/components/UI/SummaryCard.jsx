import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

const SummaryCard = ({ title, value, icon: Icon, trend, trendValue }) => {
  const isPositive = trend === 'up';
  
  return (
    <div className="card summary-card">
      <div className="summary-icon">
        <Icon size={24} />
      </div>
      <div className="summary-title text-body-md">{title}</div>
      <div className="summary-value">{value}</div>
      {trendValue && (
        <div className={`summary-trend ${isPositive ? 'positive' : 'negative'}`}>
          {isPositive ? <ArrowUpRight size={14} style={{display:'inline', verticalAlign:'middle'}}/> : <ArrowDownRight size={14} style={{display:'inline', verticalAlign:'middle'}}/>}
          {' '}{trendValue}
        </div>
      )}
    </div>
  );
};

export default SummaryCard;
