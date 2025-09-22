import React from 'react';
import footerStyles from '../modules/Footer.module.css';
import logoIcon from '../assets/monero-logo.svg'

const Footer = () => (
    <footer className={footerStyles.footer}>
    <div className={footerStyles.container}>
      <div className={footerStyles.grid}>
        <div>
          <div className={footerStyles.logoContainer}>
            <img src={logoIcon} alt="Logo" className={footerStyles.logoIcon} />
            <span className={footerStyles.logoText}>MemberFlow</span>
          </div>
          <p className={footerStyles.description}>
            The complete membership platform for modern businesses.
          </p>
        </div>
        
        <div>
          <h3 className={footerStyles.heading}>Product</h3>
          <ul className={footerStyles.linkList}>
            <li><a href="#" className={footerStyles.link}>Features</a></li>
            <li><a href="#" className={footerStyles.link}>Pricing</a></li>
            <li><a href="#" className={footerStyles.link}>Integrations</a></li>
          </ul>
        </div>
        
        <div>
          <h3 className={footerStyles.heading}>Company</h3>
          <ul className={footerStyles.linkList}>
            <li><a href="#" className={footerStyles.link}>About</a></li>
            <li><a href="#" className={footerStyles.link}>Contact</a></li>
            <li><a href="#" className={footerStyles.link}>Support</a></li>
          </ul>
        </div>
        
        <div>
          <h3 className={footerStyles.heading}>Legal</h3>
          <ul className={footerStyles.linkList}>
            <li><a href="#" className={footerStyles.link}>Privacy</a></li>
            <li><a href="#" className={footerStyles.link}>Terms</a></li>
            <li><a href="#" className={footerStyles.link}>Security</a></li>
          </ul>
        </div>
      </div>
      
      <div className={footerStyles.copyright}>
        <p>&copy; 2025 MemberFlow. All rights reserved.</p>
      </div>
    </div>
  </footer>
);

export default Footer;