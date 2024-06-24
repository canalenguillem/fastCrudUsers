import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import UserList from "./components/UserList";
import Login from "./components/Login";
import Header from "./components/Header";
import PrivateRoute from "./components/PrivateRoute";
import axios from "axios";
import "./App.css";

const App: React.FC = () => {
  const [user, setUser] = useState<{ username: string; email: string } | null>(
    null
  );

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

  return (
    <Router>
      <Header user={user} />
      <div className="content">
        <Routes>
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route element={<PrivateRoute />}>
            <Route path="/users" element={<UserList />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
};

export default App;
