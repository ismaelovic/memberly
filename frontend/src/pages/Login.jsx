import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getEnv } from '../utils/envUtils';
import styles from '../modules/Login.module.css';

const Login = () => {
  const navigate = useNavigate();
  const tenantId = getEnv('VITE_TENANT_ID');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch(`${getEnv('VITE_API_URL')}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId,
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      // Save token and navigate to dashboard
      localStorage.setItem('token', data.token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h1 className={styles.title}>Login</h1>
        {error && <p className={styles.error}>{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
          required
        />
        <button type="submit" className={styles.button}>Login</button>
        <p className={styles.switchText}>
          Don't have an account? <span onClick={() => navigate('/register')} className={styles.link}>Register</span>
        </p>
      </form>
    </div>
  );
};

export default Login;