import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../modules/SuccessPage.module.css';

const SuccessPage = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <img 
        src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" 
        alt="Success GIF" 
        className={styles.successGif} 
      />
      <h3 className={styles.title}>Payment Successful!</h3>
      <p className={styles.message}>Welcome aboard! Your registration is complete.</p>
      <button 
        className={styles.button}
        onClick={() => navigate('/login')}
      >
        Go to Login
      </button>
    </div>
  );
};

export default SuccessPage;