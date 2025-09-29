import React from 'react';
import { useNavigate } from 'react-router-dom';

const StripeFailure = () => {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h2>Error</h2>
      <p>Payment failed or was canceled.</p>
      <img 
        src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWk3M2owdzJwYjh3a3hmNjF0ZGwxcDJvaG96dWs3OTBtZGh0Nzg2NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/D7knpKzFbgDPBmdrVM/giphy.gif" 
        alt="Error GIF" 
        style={{ maxWidth: '100%', height: 'auto', display: 'block', margin: '0 auto 20px' }}
      />
      <button onClick={() => navigate('/')} style={{ marginTop: '20px', display: 'block', margin: 'auto', marginBottom: '5rem' }}>
        Go to Homepage
      </button>
    </div>
  );
};

export default StripeFailure;