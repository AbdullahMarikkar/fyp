import { Navigate } from "react-router-dom";

const AuthGuard = ({
  children,
  isAuthenticated,
}: {
  children: any;
  isAuthenticated: any;
}) => {
  if (isAuthenticated()) {
    return children;
  } else {
    return <Navigate to="/login" replace />;
  }
};

export default AuthGuard;
