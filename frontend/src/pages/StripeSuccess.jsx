import React from 'react';
import { useNavigate } from 'react-router-dom';

const StripeSuccess = () => {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h2>Success!</h2>
      <p>Payment processed successfully!</p>
      <img 
        src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" 
        alt="Success GIF" 
        style={{ maxWidth: '100%', height: 'auto', display: 'block', margin: '0 auto 20px' }}
      />
      <button onClick={() => navigate('/')} style={{ marginTop: '2rem', display: 'block', margin: '0 auto', marginBottom: '5rem' }}>
        Go to Homepage
      </button>
    </div>
  );
};

export default StripeSuccess;