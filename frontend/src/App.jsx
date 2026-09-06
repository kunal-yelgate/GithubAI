import { useEffect, useState } from "react";
import "./App.css";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Repository from "./pages/Repository";
import { getCurrentUser } from "./services/api";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);
  const [selectedRepository, setSelectedRepository] = useState(null);

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

  if (selectedRepository) {
    return (
      <Repository
        repository={selectedRepository}
        onBack={() => setSelectedRepository(null)}
      />
    );
  }

  return <Dashboard onOpenRepository={setSelectedRepository} />;
}

export default App;
