import React from 'react';

const Badge = ({ variant = 'info', children, style, className = '' }) => {
  const baseClass = 'badge';
  const variantClass = `badge-${variant}`; // info, danger, warning, success
  
  return (
    <span className={`${baseClass} ${variantClass} ${className}`} style={style}>
      {children}
    </span>
  );
};

export default Badge;
