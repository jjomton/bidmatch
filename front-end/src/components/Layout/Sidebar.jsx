import React, { useContext } from 'react';
import { Building2, LayoutDashboard, List, SlidersHorizontal, Bell, User, Settings, LogOut, Calendar } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useContext(AuthContext);

  const isActive = (path) => location.pathname.startsWith(path);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <Building2 size={24} color="#fff" />
        <div style={{display: 'flex', flexDirection: 'column'}}>
          <span style={{fontSize: '18px', fontWeight: 700, lineHeight: 1.2}}>BidMatch</span>
          <span style={{fontSize: '11px', color: '#94a3b8'}}>나라장터 공고 알림</span>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <button className={`nav-item ${isActive('/dashboard') ? 'active' : ''}`} onClick={() => navigate('/dashboard')}>
          <LayoutDashboard size={20} />
          <span>대시보드</span>
        </button>
        <button className={`nav-item ${isActive('/notices') ? 'active' : ''}`} onClick={() => navigate('/notices')}>
          <List size={20} />
          <span>공고 목록</span>
        </button>
        <button className={`nav-item ${isActive('/conditions') ? 'active' : ''}`} onClick={() => navigate('/conditions')}>
          <SlidersHorizontal size={20} />
          <span>관심 조건 관리</span>
        </button>
        <button className={`nav-item ${isActive('/calendar') ? 'active' : ''}`} onClick={() => navigate('/calendar')}>
          <Calendar size={20} />
          <span>전체 캘린더</span>
        </button>
        <button className={`nav-item ${isActive('/notifications') ? 'active' : ''}`} onClick={() => navigate('/notifications')}>
          <Bell size={20} />
          <span>알림 이력</span>
        </button>
        <button className={`nav-item ${isActive('/profile') ? 'active' : ''}`} onClick={() => navigate('/profile')}>
          <User size={20} />
          <span>내 정보</span>
        </button>
        {user?.role === 'ADMIN' && (
          <button className={`nav-item ${isActive('/admin') ? 'active' : ''}`} onClick={() => navigate('/admin')}>
            <Settings size={20} />
            <span>설정 (관리자)</span>
          </button>
        )}
      </nav>

      <div className="sidebar-footer">
        <button className="nav-item" onClick={handleLogout}>
          <LogOut size={20} />
          <span>로그아웃</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
