import { useState } from "react";
import { askAI } from "../services/api";

function renderInline(text) {
  return text
    .split(/(`[^`]+`)/g)
    .map((part, index) =>
      part.startsWith("`") && part.endsWith("`") ? (
        <code key={`${part}-${index}`}>{part.slice(1, -1)}</code>
      ) : (
        <span key={`${part}-${index}`}>{part}</span>
      ),
    );
}

function AnswerContent({ answer }) {
  const lines = answer.replace(/<\|[^>]+\|>/g, "").split("\n");
  const blocks = [];
  let codeLines = [];
  let inCodeBlock = false;

  lines.forEach((line, index) => {
    if (line.trim().startsWith("```")) {
      if (inCodeBlock) {
        blocks.push(
          <pre key={`code-${index}`}>
            <code>{codeLines.join("\n")}</code>
          </pre>,
        );
        codeLines = [];
      }
      inCodeBlock = !inCodeBlock;
      return;
    }
    if (inCodeBlock) {
      codeLines.push(line);
      return;
    }

    const trimmed = line.trim();
    if (!trimmed) return;
    if (trimmed.startsWith("### ") || trimmed.startsWith("## ")) {
      blocks.push(
        <h3 key={`heading-${index}`}>
          {renderInline(trimmed.replace(/^#+\s+/, ""))}
        </h3>,
      );
    } else if (/^[-*]\s+/.test(trimmed)) {
      blocks.push(
        <li key={`bullet-${index}`}>
          {renderInline(trimmed.replace(/^[-*]\s+/, ""))}
        </li>,
      );
    } else if (/^\d+[.)]\s+/.test(trimmed)) {
      blocks.push(
        <li className="numbered-item" key={`number-${index}`}>
          {renderInline(trimmed.replace(/^\d+[.)]\s+/, ""))}
        </li>,
      );
    } else {
      blocks.push(<p key={`paragraph-${index}`}>{renderInline(trimmed)}</p>);
    }
  });

  return <div className="answer-content">{blocks}</div>;
}

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
          <AnswerContent answer={answer} />
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
