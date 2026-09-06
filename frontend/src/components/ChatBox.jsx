import { useState } from "react";
import { askAI } from "../services/api";

function ChatBox({ owner, repo, title = "Ask Atlas" }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [provider, setProvider] = useState("");
  const [providerChoice, setProviderChoice] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    try {
      const result = await askAI(question, {
        owner,
        repo,
        ...(providerChoice ? { provider: providerChoice } : {}),
      });
      setAnswer(result.answer);
      setProvider(result.provider);
      setQuestion("");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="chat-panel">
      <div className="chat-heading">
        <div>
          <p className="eyebrow accent">AI assistant</p>
          <h2>{title}</h2>
        </div>
        <span className="status-dot">● private context</span>
      </div>
      <div className="suggestions">
        <button
          type="button"
          onClick={() =>
            setQuestion(
              owner
                ? "Explain this repository architecture and the most important files."
                : "What are my strongest technologies and most active repositories?",
            )
          }
        >
          Give me a technical overview
        </button>
        <button
          type="button"
          onClick={() =>
            setQuestion(
              owner
                ? "Where is authentication or API behavior implemented?"
                : "Which repositories use React or FastAPI?",
            )
          }
        >
          Find the important parts
        </button>
      </div>
      <label className="provider-control">
        Provider
        <select
          value={providerChoice}
          onChange={(event) => setProviderChoice(event.target.value)}
        >
          <option value="">Automatic</option>
          <option value="groq">Groq</option>
          <option value="mistral">Mistral</option>
        </select>
      </label>
      {answer && (
        <div className="chat-answer">
          <span className="eyebrow">{provider} response</span>
          <p>{answer}</p>
        </div>
      )}
      {error && <div className="notice error">{error}</div>}
      <form className="chat-form" onSubmit={submit}>
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder={
            owner
              ? "Ask about this repository..."
              : "Ask about your GitHub profile..."
          }
          maxLength={4000}
        />
        <button className="primary-button" disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>
    </section>
  );
}

export default ChatBox;
