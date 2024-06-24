import React from "react";

interface WelcomeProps {
  user: { username: string; email: string; profile: { name: string } };
}

const Welcome: React.FC<WelcomeProps> = ({ user }) => {
  return (
    <div>
      <h1>Bienvenido, {user.username}!</h1>
    </div>
  );
};

export default Welcome;
