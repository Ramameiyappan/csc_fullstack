import { useEffect, useState } from "react";
import api from "../api/axios";

const UserDetail = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get("/category/userdetail/").then((res) => {
      setUsers(res.data);
    });
  }, []);

  return (
    <div>
      <h3 className="section-title">All Users</h3>

      <table className="table">
        <thead>
          <tr>
            <th>Username</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u, i) => (
            <tr key={i}>
              <td>{u.username}</td>
              <td>{u.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserDetail;
