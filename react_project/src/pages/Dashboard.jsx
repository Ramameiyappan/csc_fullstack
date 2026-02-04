import { useEffect, useState } from "react";
import api from "../api/axios";
import { services } from "../config/services";
import Modal from "../components/Modal";
import DynamicForm from "../components/DynamicForm";
import "../styles/dashboard.css";
import UserDetail from "./UserDetail";
import { exportToExcel } from "../utils/exportExcel";

const formatDateTime = (dateStr) => {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleString("en-IN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
};

const Dashboard = () => {
  const [selectedService, setSelectedService] = useState(null);
  const [records, setRecords] = useState([]);
  const [view, setView] = useState("dashboard");
  const [pendingUsers, setPendingUsers] = useState([]);

  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");
  const isAdmin = localStorage.getItem("is_superuser") === "true";
  const token = localStorage.getItem("access");

  useEffect(() => {
    if (!token) window.location.href = "/";
  }, [token]);

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const loadRecords = async () => {
    const res = await api.get("/category/dashboard/");
    setRecords(res.data);
  };

  const loadManagerRequests = async () => {
    const res = await api.get("/auth/manager-requests/");
    setPendingUsers(res.data);
  };

  useEffect(() => {
    if (view === "dashboard") loadRecords();
    if (view === "managerRequests") loadManagerRequests();
  }, [view]);

  const exportLedger = () => {
    const excelData = records.map((r) => ({
      Work: r.work_name,
      Customer: r.customer_name,
      Detail: r.account_no,
      Mobile: r.mobile,
      Amount: r.amount,
      Commission: r.commission,
      Topup: r.topup,
      IsCSC: r.iscsc ? "Yes" : "No",
      Balance: r.balance,
      Created_At: r.createdat,
      ...(role === "manager" && { Operator: r.operator }),
    }));

    exportToExcel(excelData, "Ledger_Records");
  };

  return (
    <div>
      <header className="topbar">
        <div className="left">
          <button onClick={() => setView("dashboard")}>
            Dashboard
          </button>

          {role === "manager" && (
            <button onClick={() => setView("users")}>
              User Detail
            </button>
          )}

          {isAdmin && (
            <button onClick={() => setView("managerRequests")}>
              Manager Requests
            </button>
          )}
        </div>

        <div className="right">
          <span>
            {username} ({role})
          </span>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      {role === "operator" && (
      <div className="manager-request">
        <button
          className="manager-request-btn"
          onClick={async () => {
            try {
              await api.post("/auth/request-manager/");
              alert("Manager request sent");
            } catch (err) {
              alert(err.response?.data?.error);
            }
          }}
        >
          Request Manager Access
        </button>
      </div>
      )}

      {view === "dashboard" && (
      <>
        <h3 className="section-title">Services</h3>

        <div className="grid">
          {services.map((service) => (
          <div
            key={service.name}
            className="card"
            onClick={() =>
              setSelectedService(service)
            }
          >
            {service.name}
          </div>
          ))}
        </div>

        <h3 className="section-title">Ledger Records</h3>

        <button
          className="export-btn"
          onClick={exportLedger}
        >
          Export Ledger to Excel
        </button>

        <table className="table">
          <thead>
            <tr>
              <th>Work</th>
              <th>Customer</th>
              <th>Detail</th>
              <th>Mobile</th>
              <th>Amount</th>
              <th>Commission</th>
              <th>Topup</th>
              <th>IsCSC</th>
              <th>Balance</th>
              <th>Created At</th>
              {role === "manager" && (
                <th>Operator</th>
              )}
            </tr>
          </thead>

          <tbody>
            {records.map((r, i) => (
              <tr key={i}>
                <td>{r.work_name}</td>
                <td>{r.customer_name}</td>
                <td>{r.account_no}</td>
                <td>{r.mobile}</td>
                <td>{r.amount}</td>
                <td>{r.commission}</td>
                <td>{r.topup}</td>
                <td>{r.iscsc ? "Yes" : "No"}</td>
                <td>{r.balance}</td>
                <td>
                  {formatDateTime(r.createdat)}
                </td>
                {role === "manager" && (
                  <td>{r.operator}</td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </>
      )}

      {view === "users" && role === "manager" && (
        <UserDetail />
      )}

      {view === "managerRequests" && isAdmin && (
        <div className="admin-box">
          <h3>Pending Manager Requests</h3>

          {pendingUsers.length === 0 ? (
            <p>No pending requests</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {pendingUsers.map((u) => (
                  <tr key={u.id}>
                    <td>{u.id}</td>
                    <td>{u.username}</td>
                    <td>
                      <button
                        onClick={async () => {
                          await api.post(
                            `/auth/manager-approve/${u.id}/`
                          );
                          loadManagerRequests();
                        }}
                      >
                        Approve
                      </button>

                      <button
                        onClick={async () => {
                          await api.post(
                            `/auth/manager-reject/${u.id}/`
                          );
                          loadManagerRequests();
                        }}
                        style={{ marginLeft: "10px" }}
                      >
                        Reject
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {selectedService && (
      <Modal
        show={!!selectedService}
        onClose={() => setSelectedService(null)}
      >
        <DynamicForm
          service={selectedService}
          onClose={() => {
            setSelectedService(null);
            loadRecords();
          }}
        />
      </Modal>
      )}
    </div>
  );
};

export default Dashboard;
