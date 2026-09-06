import { useEffect, useState } from "react";
import {
  analyzeAllRepositories,
  getCurrentUser,
  getRepositories,
} from "../services/api";
import ChatBox from "../components/ChatBox";

function Stat({ label, value, detail }) {
  return (
    <div className="stat">
      <span className="stat-label">{label}</span>
      <strong>{value}</strong>
      <span className="stat-detail">{detail}</span>
    </div>
  );
}

function Dashboard({ onOpenRepository }) {
  const [user, setUser] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getCurrentUser(), getRepositories()])
      .then(([userData, repoData]) => {
        setUser(userData);
        setRepositories(repoData);
      })
      .catch(() => setError("GitHub data could not be loaded."))
      .finally(() => setLoading(false));
  }, []);

  async function handleAnalyzeAll() {
    setAnalyzing(true);
    setError("");
    try {
      setProfile((await analyzeAllRepositories()).profile);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setAnalyzing(false);
    }
  }

  if (loading)
    return (
      <main className="loading-state">Loading your GitHub workspace...</main>
    );

  const languageCount = profile
    ? Object.keys(profile.languages).length
    : new Set(repositories.map((repo) => repo.language).filter(Boolean)).size;
  const totalStars = repositories.reduce(
    (total, repo) => total + repo.stargazers_count,
    0,
  );

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand-mark">GA</div>
        <div>
          <p className="eyebrow">Repository intelligence</p>
          <h1>GitHub Atlas</h1>
        </div>
        {user && (
          <div className="user-chip">
            <img src={user.avatar_url} alt="" />
            <span>@{user.login}</span>
          </div>
        )}
      </header>
      <section className="intro-row">
        <div>
          <p className="eyebrow accent">Your workspace</p>
          <h2>A clearer map of how you build.</h2>
          <p className="lede">
            Analyze repository structure, technologies, activity, and
            architecture from one quiet workspace.
          </p>
        </div>
        <button
          className="primary-button"
          onClick={handleAnalyzeAll}
          disabled={analyzing}
        >
          {analyzing ? "Analyzing account..." : "Analyze all repositories"}
        </button>
      </section>
      {error && <div className="notice error">{error}</div>}
      <section className="stats-grid">
        <Stat
          label="Repositories"
          value={profile?.total_repositories ?? repositories.length}
          detail="visible on GitHub"
        />
        <Stat
          label="Languages"
          value={languageCount}
          detail="detected across projects"
        />
        <Stat
          label="Stars"
          value={totalStars}
          detail="across your repositories"
        />
        <Stat
          label="Commits analyzed"
          value={profile?.total_commits_analyzed ?? "—"}
          detail={profile ? "from cached analyses" : "run account analysis"}
        />
      </section>
      {profile && (
        <section className="profile-strip">
          <div>
            <span className="eyebrow">Most active</span>
            <strong>{profile.most_active_repository || "No data"}</strong>
          </div>
          <div>
            <span className="eyebrow">Most starred</span>
            <strong>{profile.most_starred_repository || "No data"}</strong>
          </div>
          <div>
            <span className="eyebrow">Top technology</span>
            <strong>{Object.keys(profile.technologies)[0] || "No data"}</strong>
          </div>
        </section>
      )}
      <ChatBox />
      <section className="section-heading">
        <div>
          <p className="eyebrow">Library</p>
          <h2>Your repositories</h2>
        </div>
        <span className="muted">{repositories.length} projects</span>
      </section>
      <section className="repo-grid">
        {repositories.map((repo) => (
          <button
            className="repo-card"
            key={repo.id}
            onClick={() => onOpenRepository(repo)}
          >
            <div className="repo-card-head">
              <span className="repo-icon">
                {repo.name.slice(0, 2).toUpperCase()}
              </span>
              <span className="arrow">↗</span>
            </div>
            <h3>{repo.name}</h3>
            <p>{repo.description || "No description yet."}</p>
            <div className="repo-meta">
              <span>{repo.language || "Unknown"}</span>
              <span>★ {repo.stargazers_count}</span>
              <span>⑂ {repo.forks_count}</span>
            </div>
          </button>
        ))}
      </section>
    </main>
  );
}

export default Dashboard;
