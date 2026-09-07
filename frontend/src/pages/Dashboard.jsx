import { useEffect, useState } from "react";
import {
  analyzeAllRepositories,
  getActivitySummary,
  getCurrentUser,
  getRepositories,
  signOut,
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

function Dashboard({ onOpenRepository, onSignedOut }) {
  const [user, setUser] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [activity, setActivity] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [languageFilter, setLanguageFilter] = useState("All");
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const [profileOpen, setProfileOpen] = useState(false);
  const [signingOut, setSigningOut] = useState(false);

  useEffect(() => {
    Promise.all([getCurrentUser(), getRepositories(), getActivitySummary()])
      .then(([userData, repoData, activityData]) => {
        setUser(userData);
        setRepositories(repoData);
        setActivity(activityData);
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

  async function handleSignOut() {
    setSigningOut(true);
    try {
      await signOut();
      onSignedOut();
    } catch (requestError) {
      setError(requestError.message);
      setSigningOut(false);
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
  const languages = [
    "All",
    ...new Set(repositories.map((repo) => repo.language).filter(Boolean)),
  ];
  const filteredRepositories = repositories.filter((repo) => {
    const matchesSearch = repo.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesLanguage =
      languageFilter === "All" || repo.language === languageFilter;
    return matchesSearch && matchesLanguage;
  });

  return (
    <main className="shell dashboard-shell">
      <header className="topbar">
        <div className="brand-mark">GA</div>
        <div>
          <p className="eyebrow">Repository intelligence</p>
          <h1>GitHub Atlas</h1>
        </div>
        {user && (
          <div className="profile-area">
            <button
              className="user-chip"
              type="button"
              aria-expanded={profileOpen}
              onClick={() => setProfileOpen((open) => !open)}
            >
              <img src={user.avatar_url} alt="" />
              <span>
                <strong>{user.name || user.login}</strong>
                <small>@{user.login}</small>
              </span>
              <b>{profileOpen ? "↑" : "↓"}</b>
            </button>
            {profileOpen && (
              <div className="profile-menu">
                <div className="profile-menu-head">
                  <img src={user.avatar_url} alt="" />
                  <div>
                    <strong>{user.name || user.login}</strong>
                    <span>@{user.login}</span>
                  </div>
                </div>
                <a href={user.html_url} target="_blank" rel="noreferrer">
                  View GitHub profile <span>↗</span>
                </a>
                <button
                  type="button"
                  onClick={handleSignOut}
                  disabled={signingOut}
                >
                  {signingOut ? "Signing out..." : "Sign out"}
                  <span>→</span>
                </button>
              </div>
            )}
          </div>
        )}
      </header>
      <section className="intro-row dashboard-hero">
        <div>
          <p className="eyebrow accent">Your workspace</p>
          <h2>
            A clearer map of <span>how you build.</span>
          </h2>
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
      <section
        className="stats-grid dashboard-stats"
        aria-label="Workspace summary"
      >
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
      {activity && (
        <section className="activity-band">
          <div className="activity-intro">
            <span className="activity-spark">✦</span>
            <div>
              <p className="eyebrow accent">Contribution pulse</p>
              <h2>Your open-source footprint</h2>
            </div>
          </div>
          <div className="activity-metric">
            <strong>{activity.pull_requests}</strong>
            <span>Pull requests made</span>
          </div>
          <div className="activity-metric">
            <strong>{activity.issues}</strong>
            <span>Issues opened</span>
          </div>
          <a
            href={`https://github.com/${activity.username}?tab=activity`}
            target="_blank"
            rel="noreferrer"
            className="activity-link"
          >
            View activity ↗
          </a>
        </section>
      )}
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
        <span className="muted">
          {filteredRepositories.length} of {repositories.length} projects
        </span>
      </section>
      <div className="repo-toolbar">
        <label className="search-field">
          <span>⌕</span>
          <input
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="Search repositories"
          />
        </label>
        <div className="filter-pills">
          {languages.map((language) => (
            <button
              key={language}
              className={languageFilter === language ? "active" : ""}
              onClick={() => setLanguageFilter(language)}
            >
              {language}
            </button>
          ))}
        </div>
      </div>
      <section className="repo-grid" aria-label="Repositories">
        {filteredRepositories.map((repo) => (
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
