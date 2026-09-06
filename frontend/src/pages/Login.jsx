function Login() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/github";
  };

  return (
    <main className="shell login-shell">
      <p className="eyebrow accent">Repository intelligence</p>
      <h1>See the shape of your code.</h1>
      <p className="lede">
        Connect GitHub to map your repositories, understand the architecture,
        and find the projects where your work is moving fastest.
      </p>
      <button className="primary-button" onClick={handleLogin}>
        Continue with GitHub ↗
      </button>
    </main>
  );
}

export default Login;
