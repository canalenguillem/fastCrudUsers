import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Header.css";

interface HeaderProps {
  user: {
    username: string;
    email: string;
  } | null;
}

const Header: React.FC<HeaderProps> = ({ user }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <header className="header">
      <div className="logo">
        <Link to="/">Logo</Link>
      </div>
      <nav className="menu">
        <Link to="/users">Users</Link>
        {/* Agrega más enlaces de menú aquí si es necesario */}
      </nav>
      <div className="user-info">
        {user ? (
          <>
            <span>
              {user.username} ({user.email})
            </span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </header>
  );
};

export default Header;
