import React from 'react';
import { Link } from 'react-router-dom';
import headerStyles from '../modules/Header.module.css'
import logoIcon from '../assets/monero-logo.svg'
const Header = () => (
    <header className={headerStyles.header}>
      <div className={headerStyles.headerContent}>
        <div className={headerStyles.headerInner}>
          <div className={headerStyles.logo}>
            <img src={logoIcon} alt="Logo" className={headerStyles.logoIcon} />
            {/* <Link to="/" className={headerStyles.logoIcon}>
              <img src={logoIcon} alt="Logo" />
            </Link> */}
            <Link to="/" className={headerStyles.logoText}>Memberly</Link>
          </div>
          <nav className={headerStyles.nav}>
            <Link to="#features" className={headerStyles.navLink}>Features</Link>
            <Link to="#how-it-works" className={headerStyles.navLink}>How it works</Link>
            <Link to="#pricing" className={headerStyles.navLink}>Pricing</Link>
          </nav>
          <div className={headerStyles.headerButtons}>
            <Link to="/login" className={headerStyles.signInButton}>Login</Link>
            {/* <button className={headerStyles.signInButton}>Sign in</button> */}
            <button className={headerStyles.getStartedButton}>Get started</button>
          </div>
        </div>
      </div>
    </header>
);

export default Header;