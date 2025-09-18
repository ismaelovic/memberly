import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import './index.css';

// Placeholder components for pages
const LandingPage = () => (
  <div className="landing-page">
    <header className="hero-section">
      <h1>Welcome to FlexHub</h1>
      <p>Your complete membership platform solution.</p>
      <div className="cta-buttons">
        <button className="btn btn-primary">Become a Member</button>
        <button className="btn btn-secondary">Contact Us</button>
      </div>
    </header>
    <section className="about-section">
      <h2>About Us</h2>
      <p>FlexHub is designed to streamline memberships, bookings, and payments for modern businesses.</p>
    </section>
    <footer className="social-section">
      <h2>Follow Us</h2>
      <div className="social-icons">
        <div className="social-icon facebook">📘</div>
        <div className="social-icon instagram">📷</div>
        <div className="social-icon twitter">🐦</div>
      </div>
    </footer>
  </div>
);

const MemberDashboard = () => (
  <div className="dashboard-layout">
    <aside className="sidebar">
      <h2>Member Dashboard</h2>
      <nav>
        <ul>
          <li><Link to="/membership">Membership</Link></li>
          <li><Link to="/payments">Payments</Link></li>
          <li><Link to="/training-sessions">Book Training Session</Link></li>
          <li><Link to="/weekly-sessions">Check Weekly Sessions</Link></li>
          <li><Link to="/check-in">Check-in</Link></li>
        </ul>
      </nav>
    </aside>
    <main className="main-content">
      <h1>Welcome, Member!</h1>
      <p>Manage your membership and payments here.</p>
    </main>
  </div>
);

const AdminDashboard = () => (
  <div className="dashboard-layout">
    <aside className="sidebar">
      <h2>Admin Dashboard</h2>
      <nav>
        <ul>
          <li><Link to="/admin-overview">Overview</Link></li>
          <li><Link to="/member-management">Manage Members</Link></li>
          <li><Link to="/payment-overview">Payments</Link></li>
        </ul>
      </nav>
    </aside>
    <main className="main-content">
      <h1>Welcome, Admin!</h1>
      <p>Manage members, payments, and more.</p>
    </main>
  </div>
);

const Membership = () => <div>Membership Management</div>;
const Payments = () => <div>Payments Overview</div>;
const TrainingSessions = () => <div>Book Training Session (Coming Soon)</div>;
const WeeklySessions = () => <div>Check Weekly Sessions (Coming Soon)</div>;
const CheckIn = () => <div>Check-in (GPS Feature Coming Soon)</div>;
const MemberManagement = () => <div>Member Management</div>;
const AdminOverview = () => <div>Admin Overview</div>;

const App = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/login', {
        email,
        password
      }, {
        withCredentials: true
      });
      setMessage('Login successful!');
    } catch (error) {
      setMessage('Login failed. Please check your credentials.');
    }
  };

  return (
    <Router>
      <div className="app-layout">
        <aside className="sidebar">
          <h2>Memberly</h2>
          <nav>
            <ul>
              <li><Link to="/membership">Membership</Link></li>
              <li><Link to="/payments">Payments</Link></li>
              <li><Link to="/training-sessions">Book Training Session</Link></li>
              <li><Link to="/weekly-sessions">Check Weekly Sessions</Link></li>
              <li><Link to="/check-in">Check-in</Link></li>
              <li><Link to="/member-management">Member Management</Link></li>
              <li><Link to="/admin-overview">Admin Overview</Link></li>
            </ul>
          </nav>
        </aside>
        <main className="main-content">
          <header className="header">
            <h1>Welcome to Memberly</h1>
          </header>
          <div className="content">
            <form onSubmit={handleLogin}>
              <div>
                <label>Email:</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div>
                <label>Password:</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit">Login</button>
            </form>
            {message && <p>{message}</p>}
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/member-dashboard" element={<MemberDashboard />} />
              <Route path="/admin-dashboard" element={<AdminDashboard />} />
              <Route path="/membership" element={<Membership />} />
              <Route path="/payments" element={<Payments />} />
              <Route path="/training-sessions" element={<TrainingSessions />} />
              <Route path="/weekly-sessions" element={<WeeklySessions />} />
              <Route path="/check-in" element={<CheckIn />} />
              <Route path="/member-management" element={<MemberManagement />} />
              <Route path="/admin-overview" element={<AdminOverview />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
};

export default App;