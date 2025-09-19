import React from 'react';
import '../modules/Navbar.module.css'

const Navbar = () => (
  <nav className="top-nav">
    <div className="logo">
      <div className="logo-icon">M</div>
      <h1>Memberly</h1>
    </div>
    <div className="nav-menu">
      <a href="#" className="nav-link">Home</a>
      <a href="#" className="nav-link">About</a>
      <a href="#" className="nav-link">Contact</a>
    </div>
  </nav>
);

export default Navbar;