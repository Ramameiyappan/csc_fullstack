import { useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import api from "../api/axios";
import "../styles/landing.css";

const Landing = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        const res = await api.post("/auth/login/", form);

        localStorage.setItem("access", res.data.access);
        localStorage.setItem("refresh", res.data.refresh);
        localStorage.setItem("username", res.data.username);
        localStorage.setItem("role", res.data.role);
        localStorage.setItem("is_superuser", res.data.is_superuser);

        window.location.href = "/dashboard";
      } else {
        await api.post("/auth/register/", form);
        alert("Registered successfully. Please login.");
        setIsLogin(true);
      }
    } 
    catch (error) { 
      if (error.response) { 
        const errObj = error.response.data.error; 
        if (typeof errObj === "object") { 
          const messages = Object.values(errObj).flat().join("\n"); 
          alert(messages); 
        } else { 
          alert(errObj); 
        } 
      } 
      else { 
        alert("Server not reachable"); 
      }
    }
    finally {
      setLoading(false);
    }
  };

  const googleLoginSuccess = async (credentialResponse) => {
    try {
      const res = await api.post("/auth/google/jwt/", {
        id_token: credentialResponse.credential,
      });

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      localStorage.setItem("username", res.data.username);
      localStorage.setItem("role", res.data.role);
      localStorage.setItem("is_superuser", res.data.is_superuser);

      window.location.href = "/dashboard";
    } catch {
      alert("Google login failed");
    }
  };

  return (
    <div className="landing">
      <div className="landing-left">
        <h1>CSC e-Governance</h1>
        <h4>
          This portal allows operators to record their daily activities
          while working under the CSC platform.
        </h4>
        <p>
          Managers can view all operational records. Users must first
          register as an operator and can later request access to the
          manager role.
        </p>
      </div>

      <div className="landing-right">
        <form onSubmit={submit} className="auth-box">
          <h2>{isLogin ? "Login" : "Register"}</h2>

          <input
            type="username"
            placeholder="Username"
            value={form.username}
            onChange={(e) =>
              setForm({ ...form, username: e.target.value })
            }
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
            required
          />

          {loading && (
            <div className="cold-start-note">
              ⏳ If the server has been inactive, it may take 1–2 minutes to start.
              Please wait and do not refresh or close the page.
            </div>
          )}

          <button disabled={loading}>
            {loading ? "Please wait..." : isLogin ? "Login" : "Register"}
          </button>

          <p className="switch">
            {isLogin ? "New user?" : "Already have an account?"}
            <span onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? " Register" : " Login"}
            </span>
          </p>

          <div className="google-box">
            <GoogleLogin
              onSuccess={googleLoginSuccess}
              onError={() =>
                alert("Google authentication error")
              }
            />
          </div>
        </form>
      </div>
    </div>
  );
};

export default Landing;
