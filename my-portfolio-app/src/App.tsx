// src/App.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
  useParams,
  useNavigate,
} from "react-router-dom";
import Home from "./components/Home";
import Portfolios from "./components/Portfolios";
import VerifyUser from "./components/VerifyUser";

const App: React.FC = () => {
  const [user, setUser] = useState(null);

  const verifyUser = async (token: string) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/auth/verify/${token}`
      );
      setUser(response.data);
    } catch (error) {
      console.error("Error verifying user:", error);
    }
  };

  return (
    <Router>
      <div>
        <h1>Portfolio Management</h1>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/portfolios">Portfolios</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/portfolios" element={<Portfolios user={user} />} />
          <Route
            path="/verify/:token"
            element={<VerifyUser verifyUser={verifyUser} />}
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
