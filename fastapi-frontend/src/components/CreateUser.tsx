import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./CreateUser.css";

const CreateUser: React.FC = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [profile, setProfile] = useState("user");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    try {
      await axios.post(
        "http://localhost:8000/users",
        { username, email, password, profile_id: profile === "admin" ? 1 : 2 },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      navigate("/users");
    } catch (error) {
      console.error("Error creating user:", error);
    }
  };

  return (
    <div className="create-user-container">
      <div className="create-user-box">
        <h2>Crear Usuario</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <select
            value={profile}
            onChange={(e) => setProfile(e.target.value)}
            required
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
          <button type="submit">Crear</button>
        </form>
      </div>
    </div>
  );
};

export default CreateUser;
