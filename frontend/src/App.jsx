import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import { getCurrentUser } from "./services/api";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);

  useEffect(() => {
    getCurrentUser()
      .then(() => setIsLoggedIn(true))
      .catch(() => setIsLoggedIn(false))
      .finally(() => setCheckingSession(false));
  }, []);

  if (checkingSession) {
    return <h2>Checking GitHub session...</h2>;
  }

  if (!isLoggedIn) {
    return <Login />;
  }

  return <Dashboard />;
}

export default App;
