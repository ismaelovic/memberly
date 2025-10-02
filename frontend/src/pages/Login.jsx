import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getEnv } from "../utils/envUtils";
import styles from "../modules/Login.module.css";

const Login = () => {
  const navigate = useNavigate();
  const tenantId = getEnv("VITE_TENANT_ID");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      let response = await fetch(`${getEnv("VITE_API_URL")}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Tenant-ID": tenantId,
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Invalid credentials!");
      }

      const { member_auth_id, role } = await response.json();
      localStorage.setItem("member_auth_id", member_auth_id);
      console.log("Login successful, member_auth_id:", member_auth_id);

      switch (role) {
        case "member":
          navigate("/user-dashboard");
          break;
        case "tenant_admin":
          navigate("/admin-dashboard");
          break;
        case "system_admin":
          navigate("/system-admin-dashboard");
          break;
        default:
          throw new Error("Unknown role");
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h1 className={styles.title}>Login</h1>
        {error && <p className={styles.error}>{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
          required
        />
        <button type="submit" className={styles.button}>
          Login
        </button>
        <p className={styles.switchText}>
          Don't have an account?{" "}
          <span onClick={() => navigate("/register")} className={styles.link}>
            Register
          </span>
        </p>
      </form>
    </div>
  );
};

export default Login;
