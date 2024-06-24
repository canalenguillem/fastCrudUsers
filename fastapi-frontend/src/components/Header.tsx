import React from "react";
import "./Header.css";

interface HeaderProps {
  user: { username: string; email: string } | null;
  logout: () => void;
}

const Header: React.FC<HeaderProps> = ({ user, logout }) => {
  return (
    <header>
      <div className="logo">Logo</div>
      {user && (
        <nav>
          <span>{user.username}</span>
          <button onClick={logout}>Logout</button>
        </nav>
      )}
    </header>
  );
};

export default Header;
