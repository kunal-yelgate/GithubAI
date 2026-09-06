import { useEffect, useState } from "react";
import { analyzeRepository } from "../services/api";
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

function Repository({ repository, onBack }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    analyzeRepository(repository.owner.login, repository.name)
      .then(setAnalysis)
      .catch((requestError) => setError(requestError.message))
      .finally(() => setLoading(false));
  }, [repository]);

  return (
    <main className="shell detail-shell">
      <button className="back-button" onClick={onBack}>
        ← Back to workspace
      </button>
      <header className="detail-header">
        <div>
          <p className="eyebrow accent">Repository analysis</p>
          <h1>{repository.name}</h1>
          <p className="lede">
            {repository.description || "A repository without a description."}
          </p>
        </div>
        <a
          className="outline-button"
          href={repository.html_url}
          target="_blank"
          rel="noreferrer"
        >
          Open on GitHub ↗
        </a>
      </header>
      {loading && (
        <div className="loading-state">Reading repository structure...</div>
      )}
      {error && <div className="notice error">{error}</div>}
      {analysis && (
        <>
          <section className="stats-grid detail-stats">
            <Stat
              label="Stars"
              value={analysis.repository.stars}
              detail="on GitHub"
            />
            <Stat
              label="Files"
              value={analysis.structure.total_files}
              detail="in repository tree"
            />
            <Stat
              label="Commits"
              value={analysis.commits.total_analyzed}
              detail="analyzed recently"
            />
            <Stat
              label="Primary language"
              value={analysis.languages.primary_language || "—"}
              detail="by code volume"
            />
          </section>
          <section className="detail-grid">
            <article className="panel wide-panel">
              <div className="panel-title">
                <div>
                  <p className="eyebrow">Architecture</p>
                  <h2>{analysis.architecture.architecture_type}</h2>
                </div>
                <span className="status-dot">● analyzed</span>
              </div>
              <div className="pill-row">
                {analysis.architecture.layers.map((layer) => (
                  <span className="pill" key={layer}>
                    {layer}
                  </span>
                ))}
              </div>
              <div className="architecture-line">
                <strong>
                  {analysis.architecture.frontend || "Repository"}
                </strong>
                <span>→</span>
                <strong>{analysis.architecture.backend || "Source"}</strong>
              </div>
            </article>
            <article className="panel">
              <p className="eyebrow">Technologies</p>
              <h2>{analysis.technologies.length}</h2>
              <div className="pill-row">
                {analysis.technologies.map((technology) => (
                  <span className="pill" key={technology}>
                    {technology}
                  </span>
                ))}
              </div>
            </article>
            <article className="panel">
              <p className="eyebrow">README signal</p>
              <h2>
                {analysis.readme.exists
                  ? `${analysis.readme.length.toLocaleString()} chars`
                  : "Missing"}
              </h2>
              <p className="muted">
                {analysis.readme.sections.length} sections ·{" "}
                {analysis.readme.has_installation
                  ? "setup included"
                  : "no setup detected"}
              </p>
            </article>
            <article className="panel wide-panel">
              <p className="eyebrow">Important files</p>
              <h2>
                {analysis.important_files.important_files.length} selected files
              </h2>
              <ul className="file-list">
                {analysis.important_files.important_files.map((file) => (
                  <li key={file}>
                    <code>{file}</code>
                    <span>
                      {analysis.important_files.entry_points.includes(file)
                        ? "entry point"
                        : "configuration"}
                    </span>
                  </li>
                ))}
              </ul>
            </article>
            <article className="panel wide-panel">
              <p className="eyebrow">Source map</p>
              <h2>{analysis.source_analysis.length} source files understood</h2>
              <div className="source-list">
                {analysis.source_analysis.map((file) => (
                  <div key={file.file}>
                    <code>{file.file}</code>
                    <span>
                      {file.functions?.length || 0} functions ·{" "}
                      {file.classes?.length || file.components?.length || 0}{" "}
                      types/components
                    </span>
                  </div>
                ))}
              </div>
            </article>
          </section>
          <ChatBox
            owner={repository.owner.login}
            repo={repository.name}
            title={`Ask about ${repository.name}`}
          />
        </>
      )}
    </main>
  );
}

export default Repository;
