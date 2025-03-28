import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import AuthGuard from "./utils/AuthGuard";
import Login from "./components/Authentication/Login";
import SignUp from "./components/Authentication/SignUp";
import { getAccessToken } from "./utils/cookieService";
import History from "./components/History/History";

const isAuthenticated = () => {
  console.log("Get Access Token ", getAccessToken());
  // Implement your authentication logic here
  // For example, check if the user is logged in or has a valid token
  return !!getAccessToken(); // Return true if authenticated, false otherwise
};

export const router = createBrowserRouter([
  { path: "login", element: <Login /> },
  { path: "signup", element: <SignUp /> },
  {
    path: "",
    element: (
      <AuthGuard isAuthenticated={isAuthenticated}>
        <App />
      </AuthGuard>
    ),
  },
  {
    path: "history",
    element: (
      <AuthGuard isAuthenticated={isAuthenticated}>
        <History />
      </AuthGuard>
    ),
  },
]);
