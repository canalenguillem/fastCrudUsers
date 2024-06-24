import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import Welcome from "./components/Welcome";
import UserList from "./components/UserList";
import CreateUser from "./components/CreateUser";
import Login from "./components/Login";
import Header from "./components/Header";
import axios from "axios";
import "./App.css";

const App: React.FC = () => {
  const [user, setUser] = useState<{
    username: string;
    email: string;
    profile: { name: string };
  } | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await axios.get("http://localhost:8000/users/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          setUser(response.data);
        } catch (error) {
          console.error("Error fetching user:", error);
        }
      }
    };

    fetchUser();
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <Router>
      {user && <Header user={user} logout={logout} />}
      <div className="content">
        <Routes>
          <Route
            path="/login"
            element={user ? <Navigate to="/" /> : <Login setUser={setUser} />}
          />
          <Route
            path="/"
            element={user ? <Welcome user={user} /> : <Navigate to="/login" />}
          />
          {user && user.profile && user.profile.name === "admin" && (
            <>
              <Route path="/users" element={<UserList />} />
              <Route path="/create-user" element={<CreateUser />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
