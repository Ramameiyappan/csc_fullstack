import { useEffect, useState } from "react";
import api from "../api/axios";

const AdminDashboard = () => {
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState("");

  const fetchRequests = async () => {
    const res = await api.get("/auth/manager-requests/");
    setRequests(res.data);
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const approve = async (id) => {
    await api.post(`/auth/manager-approve/${id}/`);
    setMessage("Approved successfully");
    fetchRequests();
  };

  const reject = async (id) => {
    await api.post(`/auth/manager-reject/${id}/`);
    setMessage("Rejected successfully");
    fetchRequests();
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Admin Dashboard</h2>

      {message && <p>{message}</p>}

      {requests.length === 0 ? (
        <p>No pending manager requests</p>
      ) : (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Username</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.username}</td>
                <td>
                  <button onClick={() => approve(u.id)}>Approve</button>
                  <button onClick={() => reject(u.id)} style={{ marginLeft: "10px" }}>
                    Reject
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AdminDashboard;
