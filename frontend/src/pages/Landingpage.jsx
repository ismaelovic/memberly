import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from '../modules/Landingpage.module.css';
import 'react-multi-carousel/lib/styles.css';

import { Play, Check, Star } from 'lucide-react';
import bmwLogo from '../assets/bmw-logo-svgrepo-com.svg';
import chanelLogo from '../assets/chanel-2-logo-svgrepo-com.svg';
import creativeCloudLogo from '../assets/creative-cloud-cc-logo-svgrepo-com.svg';
import grabLogo from '../assets/grab-logo-svgrepo-com.svg';
import mercedesLogo from '../assets/mercedes-benz-9-logo-svgrepo-com.svg';
import porscheLogo from '../assets/porsche-6-logo-svgrepo-com.svg';
import redbullLogo from '../assets/redbull-logo-svgrepo-com.svg';
import slackLogo from '../assets/slack-logo-svgrepo-com.svg';
import sonyLogo from '../assets/sony-2-logo-svgrepo-com.svg';
import spotifyLogo from '../assets/spotify-1-logo-svgrepo-com.svg'; 
import northFaceLogo from '../assets/the-north-face-1-logo-svgrepo-com.svg';
import underArmourLogo from '../assets/under-armour-logo-svgrepo-com.svg';
import visaLogo from '../assets/visa-logo-svgrepo-com.svg';
import volkswagenLogo from '../assets/volkswagen-1-logo-svgrepo-com.svg';
import whatsappLogo from '../assets/whatsapp-icon-logo-svgrepo-com.svg';

const LandingPage = () => {
  const [activeTab, setActiveTab] = useState(0);

  const features = [
    { icon: 'Users', text: 'Complete membership management' },
    { icon: 'Calendar', text: 'Advanced booking & scheduling system' },
    { icon: 'CreditCard', text: 'Integrated payment processing' },
    { icon: 'Smartphone', text: 'Mobile check-in & QR codes' },
    { icon: 'BarChart3', text: 'Real-time analytics & reporting' },
    { icon: 'Globe', text: 'Multi-location support' },
  ];

  const howToTabs = [
    {
      title: 'Setup & Configure',
      description: 'Get your platform ready in minutes',
      videoPlaceholder: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600&h=400&fit=crop',
    },
    {
      title: 'Manage & Scale',
      description: 'Grow your business effortlessly',
      videoPlaceholder: 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=600&h=400&fit=crop',
    },
  ];

const testimonialLogos = [
    bmwLogo,
    chanelLogo,
    creativeCloudLogo,
    grabLogo,
    mercedesLogo,
    porscheLogo,
    redbullLogo,
    slackLogo,
    sonyLogo,
    spotifyLogo,
    northFaceLogo,
    underArmourLogo,
    visaLogo,
    volkswagenLogo,
    whatsappLogo,
];

  return (
    <div className={styles.container}>

    {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <p className={styles.heroSubtitle}>
            Plug and play
          </p>
          <h1 className={styles.heroTitle}>
            A tailored platform, 
            <br />
            <span className={styles.heroTitleGradient}>for your business needs</span>
          </h1>
          <p className={styles.heroSubtitle}>
            A comprehensive solution for managing memberships, bookings, payments, and more.
          </p>
          <div className={styles.heroButtons}>
            <button className={styles.primaryButton}>Start free trial</button>
            <Link to="/register" className={styles.secondaryButton}>Register</Link>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className={styles.trustSection}>
        <div className={styles.trustContent}>
          <div className={styles.trustText}>
            <p className={styles.trustDescription}>
              <strong>Join 10,000+ businesses, gyms, studios, and organizations</strong>
            </p>
            <div className={styles.logoMarquee}>
              <div className={styles.logoTrack}>
                {testimonialLogos.map((logo, index) => (
                  <div key={index} className={styles.logoItem}>
                    <img
                      src={logo}
                      alt={`Client ${index + 1}`}
                      className={styles.logoImage}
                    />
                  </div>
                ))}
                {testimonialLogos.map((logo, index) => (
                  <div key={`duplicate-${index}`} className={styles.logoItem}>
                    <img
                      src={logo}
                      alt={`Client duplicate ${index + 1}`}
                      className={styles.logoImage}
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className={styles.featuresSection}>
        <div className={styles.featuresContent}>
          <div className={styles.featuresHeader}>
            <h2 className={styles.featuresTitle}>
              Everything you need,
              <br />
              nothing you don't
            </h2>
            <p className={styles.featuresSubtitle}>
              From membership management to payment processing, we've got all the tools
              your business needs to thrive.
            </p>
          </div>

          <div className={styles.featuresGrid}>
            {features.map((feature, index) => (
              <div key={index} className={styles.featureCard}>
                <div className={styles.featureIcon}>
                  <feature.icon className={styles.featureIconSvg} />
                </div>
                <div className={styles.featureContent}>
                  <Check className={styles.checkIcon} />
                  <p className={styles.featureText}>{feature.text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className={styles.howItWorksSection}>
        <div className={styles.howItWorksContent}>
          <div className={styles.howItWorksHeader}>
            <h2 className={styles.howItWorksTitle}>How it works</h2>
            <p className={styles.howItWorksSubtitle}>
              Get started in minutes with our intuitive setup process
            </p>
          </div>

          <div className={styles.tabsContainer}>
            <div className={styles.tabsWrapper}>
              {/* Tabs */}
              <div className={styles.tabsList}>
                <div className={styles.tabsInner}>
                  {howToTabs.map((tab, index) => (
                    <button
                      key={index}
                      onClick={() => setActiveTab(index)}
                      className={`${styles.tab} ${activeTab === index ? styles.tabActive : ''}`}
                    >
                      <h3 className={`${styles.tabTitle} ${activeTab === index ? styles.tabTitleActive : ''}`}>
                        {tab.title}
                      </h3>
                      <p className={styles.tabDescription}>{tab.description}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Video/Image Display */}
              <div className={styles.tabContent}>
                <div className={styles.videoContainer}>
                  <img
                    src={howToTabs[activeTab].videoPlaceholder}
                    alt={howToTabs[activeTab].title}
                    className={styles.videoImage}
                  />
                  <div className={styles.playOverlay}>
                    <button className={styles.playButton}>
                      <Play className={styles.playIcon} />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial Section */}
      <section className={styles.testimonialSection}>
        <div className={styles.testimonialContent}>
          <div className={styles.stars}>
            {[...Array(5)].map((_, i) => (
              <Star key={i} className={styles.star} />
            ))}
          </div>
          <blockquote className={styles.testimonialQuote}>
            "If a different platform offered us ten years free, we'd tell them we're not interested.
            Memberly just works perfectly for our business."
          </blockquote>
          <div className={styles.testimonialAuthor}>
            <img
              src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=64&h=64&fit=crop&crop=face"
              alt="Customer"
              className={styles.authorImage}
            />
            <div className={styles.authorInfo}>
              <p className={styles.authorName}>Mike Johnson</p>
              <p className={styles.authorTitle}>Fitness Studio Owner</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className={styles.ctaSection}>
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Ready to <br />transform your business?</h2>
          <p className={styles.ctaSubtitle}>
            Join thousands of businesses already using Memberly to streamline their operations
            and grow their revenue.
          </p>
          <div className={styles.ctaButtons}>
            <button className={styles.ctaPrimaryButton}>Start free trial</button>
            <button className={styles.ctaSecondaryButton}>Schedule demo</button>
          </div>
        </div>
      </section>

      {/* Footer */}
    </div>
  );
};

export default LandingPage;