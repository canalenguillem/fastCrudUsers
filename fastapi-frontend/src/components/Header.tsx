import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";

interface HeaderProps {
  user: { username: string; email: string; profile: { name: string } };
  logout: () => void;
}

const Header: React.FC<HeaderProps> = ({ user, logout }) => {
  return (
    <header>
      <div className="logo">Logo</div>
      {user && (
        <nav>
          <span>{user.username}</span>
          {user.profile.name === "admin" && (
            <>
              <Link to="/users">Ver Usuarios</Link>
              <Link to="/create-user">Crear Usuario</Link>
            </>
          )}
          <button onClick={logout}>Logout</button>
        </nav>
      )}
    </header>
  );
};

export default Header;
