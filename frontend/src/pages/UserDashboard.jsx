import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getEnv } from '../utils/envUtils';
import styles from '../modules/Dashboard.module.css';

const UserDashboard = () => {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState(null);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }

        const userResponse = await fetch(`${getEnv('VITE_API_URL')}/api/auth/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        const paymentsResponse = await fetch(`${getEnv('VITE_API_URL')}/api/payments/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!userResponse.ok || !paymentsResponse.ok) {
          throw new Error('Failed to fetch data');
        }

        const userData = await userResponse.json();
        const paymentsData = await paymentsResponse.json();

        setUserInfo(userData);
        setPayments(paymentsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  const handleEditProfile = () => {
    navigate('/edit-profile');
  };

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Dashboard</h1>

      {userInfo && (
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Profile Information</h2>
          <p><strong>Name:</strong> {userInfo.firstName} {userInfo.lastName}</p>
          <p><strong>Email:</strong> {userInfo.email}</p>
          <p><strong>Phone:</strong> {userInfo.phone}</p>
          <button onClick={handleEditProfile} className={styles.button}>Edit Profile</button>
        </div>
      )}

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Payments</h2>
        {payments.length > 0 ? (
          <ul className={styles.paymentsList}>
            {payments.map((payment) => (
              <li key={payment.id} className={styles.paymentItem}>
                <p><strong>Amount:</strong> ${payment.amount / 100}</p>
                <p><strong>Status:</strong> {payment.status}</p>
                <p><strong>Date:</strong> {new Date(payment.date).toLocaleDateString()}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No payments found.</p>
        )}
      </div>
    </div>
  );
};

export default UserDashboard;