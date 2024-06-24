import React, { useEffect, useState } from "react";
import axios from "axios";
import "./UserList.css";

interface User {
  id: number;
  username: string;
  email: string;
}

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await axios.get("http://localhost:8000/users", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          setUsers(response.data);
        } catch (error) {
          console.error("Error fetching users:", error);
        }
      } else {
        console.error("No token found");
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="user-list-container">
      <div className="user-list-box">
        <h2>User List</h2>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              {user.username} - {user.email}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default UserList;
