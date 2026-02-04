import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";

/* this is to check whether the user has access token
to go to dashboard */
const PrivateRoute = ({ children }) => {
  return localStorage.getItem("access")
    ? children
    : <Navigate to="/" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
