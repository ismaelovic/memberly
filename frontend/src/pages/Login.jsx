import React from 'react';
import '../modules/Login.module.css';

const Login = () => (
  <div className="login-container">
    <h2>Login</h2>
    <form className="login-form">
      <input type="email" placeholder="Email" className="login-input" />
      <input type="password" placeholder="Password" className="login-input" />
      <button type="submit" className="login-button">Login</button>
    </form>
  </div>
);

export default Login;