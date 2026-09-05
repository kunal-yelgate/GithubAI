import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function App() {

  const isLoggedIn = false;

  if (!isLoggedIn) {
    return <Login />;
  }

  return <Dashboard />;
}

export default App;