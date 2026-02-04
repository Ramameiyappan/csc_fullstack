import { useState } from "react";
import api from "../api/axios";

const UserDashboard = ({ user }) => {
  const [message, setMessage] = useState("");

  const requestManager = async () => {
    try {
      const res = await api.post("/auth/request-manager/");
      setMessage(res.data.success);
    } catch (err) {
      setMessage(err.response?.data?.error || "Something went wrong");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Welcome, {user.username}</h2>
      <p>Role: {user.role}</p>

      {user.role === "operator" && (
        <button onClick={requestManager}>
          Request Manager Access
        </button>
      )}

      {message && <p>{message}</p>}
    </div>
  );
};

export default UserDashboard;
