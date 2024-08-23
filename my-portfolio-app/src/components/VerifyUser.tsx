// src/components/VerifyUser.tsx
import React, { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

const VerifyUser: React.FC<{ verifyUser: (token: string) => void }> = ({
  verifyUser,
}) => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      verifyUser(token);
      navigate("/portfolios");
    }
  }, [token, verifyUser, navigate]);

  return <div>Verifying...</div>;
};

export default VerifyUser;
