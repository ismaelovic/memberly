import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Navbar from './pages/Navbar';
// import Footer from './pages/Footer';
// import Login from './pages/Login';
import LandingPage from './pages/Landingpage';
import './index.css';

const App = () => {
  return (
    <Router>
      {/* <Navbar /> */}
      <Routes>
        <Route path="/" element={<LandingPage />} />
        {/* Add other routes here */}
      </Routes>
      {/* <Footer /> */}
    </Router>
  );
};

export default App;