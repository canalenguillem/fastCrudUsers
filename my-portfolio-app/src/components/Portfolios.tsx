// src/components/Portfolios.tsx
import React from "react";

const Portfolios: React.FC<{ user: any }> = ({ user }) => {
  if (!user) {
    return <div>Please register or login to manage your portfolios.</div>;
  }
  return <div>Portfolio Management for {user.username}</div>;
};

export default Portfolios;
