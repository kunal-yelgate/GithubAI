function Login() {

  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/github";
  };

  return (
    <div>
      <h1>GitHub AI Repo Analyzer</h1>

      <p>
        Analyze your GitHub repositories using AI.
      </p>

      <button onClick={handleLogin}>
        Login with GitHub
      </button>
    </div>
  );
}

export default Login;