import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getEnv } from "../utils/envUtils";
import styles from "../modules/SystemAdminDashboard.module.css";

const SystemAdminDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    tenants: 0,
    users: 0,
    activeSubscriptions: 0,
    activeMemberships: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [inviteMessage, setInviteMessage] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(
          `${getEnv("VITE_API_URL")}/api/system-admin/stats`,
          {
            credentials: "include",
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || "Failed to fetch stats");
        }

        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const handleGenerateLink = async () => {
    try {
      const response = await fetch(
        `${getEnv("VITE_API_URL")}/api/system-admin/generate-tenant-link`,
        {
          method: "POST",
          credentials: "include",
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Failed to generate link");
      }

      const { link } = await response.json();
      navigator.clipboard.writeText(link);
      alert("Onboarding link copied to clipboard!");
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleInviteTenantAdmin = async (e) => {
    e.preventDefault();
    setInviteMessage("");

    try {
      const response = await fetch(
        `${getEnv("VITE_API_URL")}/api/system-admin/invite-tenant-admin`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({ email }),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Failed to invite tenant admin");
      }

      const { message } = await response.json();
      setInviteMessage(message);
      setEmail("");
    } catch (err) {
      setInviteMessage(`Error: ${err.message}`);
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>System Admin Dashboard</h1>
      <div className={styles.statsSection}>
        <p>
          <strong>Number of Tenants:</strong> {stats.tenants}
        </p>
        <p>
          <strong>Number of Users:</strong> {stats.users}
        </p>
        <p>
          <strong>Active Subscriptions:</strong> {stats.activeSubscriptions}
        </p>
        <p>
          <strong>Active Memberships:</strong> {stats.activeMemberships}
        </p>
      </div>
      <button
        onClick={handleGenerateLink}
        className={styles.generateLinkButton}
      >
        Generate Onboarding Link
      </button>

      <form onSubmit={handleInviteTenantAdmin} className={styles.inviteForm}>
        <h2>Invite Tenant Admin</h2>
        <input
          type="email"
          placeholder="Enter tenant admin email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className={styles.emailInput}
        />
        <button type="submit" className={styles.inviteButton}>
          Send Invite
        </button>
      </form>
      {inviteMessage && <p className={styles.inviteMessage}>{inviteMessage}</p>}
    </div>
  );
};

export default SystemAdminDashboard;
