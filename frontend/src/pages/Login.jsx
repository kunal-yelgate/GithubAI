function Login() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/github";
  };

  return (
    <main className="shell login-shell">
      <div className="login-copy">
        <p className="eyebrow accent">Repository intelligence</p>
        <h1>See the shape of your code.</h1>
        <p className="lede">
          Connect GitHub to map your repositories, understand the architecture,
          and find the projects where your work is moving fastest.
        </p>
        <button className="primary-button" onClick={handleLogin}>
          Continue with GitHub ↗
        </button>
      </div>
      <aside className="login-flow" aria-label="Analysis flow">
        <div className="flow-heading">
          <span className="eyebrow">Atlas / 01</span>
          <span className="flow-live">
            <i /> ready
          </span>
        </div>
        <div className="flow-line" />
        <div className="flow-step flow-step-active">
          <span>01</span>
          <div>
            <strong>Map the repository</strong>
            <p>Structure, languages, and entry points</p>
          </div>
        </div>
        <div className="flow-step">
          <span>02</span>
          <div>
            <strong>Read the architecture</strong>
            <p>Layers, modules, and dependencies</p>
          </div>
        </div>
        <div className="flow-step">
          <span>03</span>
          <div>
            <strong>Ask better questions</strong>
            <p>Grounded answers from your code</p>
          </div>
        </div>
        <div className="flow-footer">
          <span>PRIVATE CONTEXT</span>
          <span>GITHUB OAUTH</span>
        </div>
      </aside>
    </main>
  );
}

export default Login;
