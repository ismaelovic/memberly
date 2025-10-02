import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getEnv } from "../utils/envUtils";
import styles from "../modules/Dashboard.module.css";

const UserDashboard = () => {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState(null);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        let memberAuthId = localStorage.getItem("member_auth_id");
        let membershipId = localStorage.getItem("membership_id");
        console.log("Cached memberAuthId:", memberAuthId);
        if (!memberAuthId) {
          navigate("/login");
          return;
        }

        // Fetch memberAuthId and membershipId
        console.log("Fetching profile for memberAuthId:", memberAuthId);
        const profileResponse = await fetch(
          `${getEnv("VITE_API_URL")}/api/auth/profile/${memberAuthId}`
        );
        if (profileResponse.status != 200) {
          const errorText = await profileResponse.text();
          console.error("Profile fetch error:", errorText);
          navigate("/login");
          return;
        }

        const profileData = await profileResponse.json();
        const memberProfileId = profileData.user.id;

        console.log(
          "Fetching membershipId using memberProfileId:",
          memberProfileId
        );
        let membershipCall = await fetch(
          `${getEnv("VITE_API_URL")}/api/memberships/member/${memberProfileId}`,
          { credentials: "include" }
        );
        membershipId = (await membershipCall.json()).membership_id;
        console.log("Fetching payments using membershipId:", membershipId);
        const paymentsResponse = await fetch(
          `${getEnv("VITE_API_URL")}/api/payments/membership/${membershipId}`,
          { credentials: "include" }
        );
        // Cache the IDs
        localStorage.setItem("membership_id", membershipId);

        if (!paymentsResponse.ok) {
          const errorText = await paymentsResponse.text();
          console.error("Memberships or Payments fetch error:", errorText);
          throw new Error("Failed to fetch memberships or payments");
        }

        const paymentsData = await paymentsResponse.json();

        setUserInfo(profileData);
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
    navigate("/edit-profile");
  };

  const handleChangePassword = () => {
    navigate("/change-password");
  };

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  console.log("Payments Info:", payments);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Dashboard</h1>

      {userInfo && (
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Profile Information</h2>
          <p>
            <strong>Name:</strong> {userInfo.user.first_name}{" "}
            {userInfo.user.last_name}
          </p>
          <p>
            <strong>Phone:</strong> {userInfo.user.phone_number}
          </p>
          <button onClick={handleEditProfile} className={styles.button}>
            Edit Profile
          </button>
        </div>
      )}

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Payments</h2>
        {payments.length > 0 ? (
          <ul className={styles.paymentsList}>
            {payments.map((payment) => {
              const startDate = new Date(payment.stripe_period_start * 1000);
              const endDate = new Date(payment.stripe_period_end * 1000);
              const billingMonth = `${startDate.toLocaleString("default", {
                month: "long",
              })} ${startDate.getFullYear()}`;

              return (
                <li key={payment.id} className={styles.paymentItem}>
                  <p>
                    <strong>Billing Month:</strong> {billingMonth}
                  </p>
                  <p>
                    <strong>Amount:</strong> {payment.amount}{" "}
                    {payment.stripe_currency}
                  </p>
                  <p>
                    <strong>Status:</strong> {payment.status}
                  </p>
                </li>
              );
            })}
          </ul>
        ) : (
          <p>No payments found.</p>
        )}
      </div>
      <button onClick={handleChangePassword} className={styles.button}>
        Change Password
      </button>
    </div>
  );
};

export default UserDashboard;
