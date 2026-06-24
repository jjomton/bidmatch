import React, { useEffect, useContext, useState, useRef } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { Loader2 } from 'lucide-react';
import api from '../utils/api';

function OAuthCallback() {
  const { provider } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);
  const [error, setError] = useState('');
  const processedRef = useRef(false);

  useEffect(() => {
    if (processedRef.current) return;

    const params = new URLSearchParams(location.search);
    const code = params.get('code');
    const errParam = params.get('error');

    if (errParam) {
      setError('소셜 로그인이 취소되었거나 오류가 발생했습니다.');
      setTimeout(() => navigate('/login'), 3000);
      return;
    }

    if (!code) {
      setError('인증 코드가 없습니다.');
      setTimeout(() => navigate('/login'), 3000);
      return;
    }

    processedRef.current = true;

    // 백엔드로 인가 코드 전송하여 토큰 교환
    api.post(`/auth/oauth/${provider}/callback`, { code })
      .then(res => {
        if (res.data.success) {
          login(res.data.token, res.data.user);
          navigate('/dashboard', { replace: true });
        } else {
          setError(res.data.message || '소셜 로그인 처리에 실패했습니다.');
          setTimeout(() => navigate('/login'), 3000);
        }
      })
      .catch(err => {
        console.error('OAuth Error:', err);
        setError('서버와 통신 중 오류가 발생했습니다.');
        setTimeout(() => navigate('/login'), 3000);
      });
  }, [provider, location, navigate, login]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#0a0a0a]">
      {error ? (
        <div style={{ textAlign: 'center', color: '#ef4444' }}>
          <p style={{ fontSize: '16px', fontWeight: 600, marginBottom: '8px' }}>로그인 실패</p>
          <p style={{ fontSize: '14px', color: '#94a3b8' }}>{error}</p>
          <p style={{ fontSize: '13px', color: '#64748b', marginTop: '16px' }}>잠시 후 로그인 화면으로 이동합니다...</p>
        </div>
      ) : (
        <div style={{ textAlign: 'center' }}>
          <Loader2 className="w-10 h-10 text-blue-500 animate-spin mx-auto mb-4" />
          <h2 style={{ fontSize: '18px', fontWeight: 600, color: '#f8fafc', marginBottom: '8px' }}>
            {provider === 'google' ? '구글' : '카카오'} 계정으로 안전하게 로그인 중입니다...
          </h2>
          <p style={{ fontSize: '14px', color: '#94a3b8' }}>잠시만 기다려 주세요.</p>
        </div>
      )}
    </div>
  );
}

export default OAuthCallback;
