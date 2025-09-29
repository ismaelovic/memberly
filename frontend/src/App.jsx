import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Navbar from './pages/Navbar';
// import Footer from './pages/Footer';
// import Login from './pages/Login';
import LandingPage from './pages/Landingpage';
import Header from './pages/Header';
import Footer from './pages/Footer';
import Login from './pages/Login';
import Register from './pages/Register';
import './index.css';
import StripeSuccess from './pages/StripeSuccess';
import StripeFailure from './pages/StripeFailure';
import UserDashboard from './pages/UserDashboard';

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/stripe_success/" element={<StripeSuccess />} />
        <Route path="/stripe_failure/" element={<StripeFailure />} />
        <Route path="/dashboard" element={<UserDashboard />} /> {/* Updated to UserDashboard */}
        {/* Add other routes here */}
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;