import { useState } from "react";
import { askAI } from "../services/api";

function formatText(text) {
  return text
    .replace(/<\|[^>]+\|>/g, "")
    .replace(/\*\*/g, "")
    .replace(/\*/g, "")
    .replace(/`/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

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
  const lines = formatText(answer).split("\n");
  const blocks = [];

  lines.forEach((line, index) => {
    const trimmed = line.trim();
    if (!trimmed) return;

    if (
      /^(?:Overview|Summary|Key findings?|Findings?|Impact|Recommendation|Limitations?)\s*:/i.test(
        trimmed,
      )
    ) {
      blocks.push(<h3 key={`heading-${index}`}>{renderInline(trimmed)}</h3>);
      return;
    }

    if (/^[-*]\s+/.test(trimmed)) {
      blocks.push(
        <li key={`bullet-${index}`}>
          {renderInline(trimmed.replace(/^[-*]\s+/, ""))}
        </li>,
      );
      return;
    }

    if (/^\d+[.)]\s+/.test(trimmed)) {
      blocks.push(
        <li className="numbered-item" key={`number-${index}`}>
          {renderInline(trimmed.replace(/^\d+[.)]\s+/, ""))}
        </li>,
      );
      return;
    }

    blocks.push(<p key={`paragraph-${index}`}>{renderInline(trimmed)}</p>);
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

  function streamAnswer(text) {
    const cleaned = formatText(text);
    let index = 0;

    setAnswer("");
    const timer = setInterval(() => {
      index += 1;
      setAnswer(cleaned.slice(0, index));

      if (index >= cleaned.length) {
        clearInterval(timer);
      }
    }, 18);
  }

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
      setProvider(result.provider);
      setQuestion("");
      streamAnswer(result.answer);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mx-auto mt-8 w-full max-w-5xl rounded-2xl border border-stone-200 bg-white/80 p-5 shadow-[0_18px_50px_rgba(15,23,42,0.06)] backdrop-blur-sm sm:p-6">
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <p className="mb-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-stone-500">
            AI assistant
          </p>
          <h2 className="text-2xl font-semibold tracking-[-0.04em] text-stone-900">
            {title}
          </h2>
        </div>
        <span className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-1 text-[10px] font-medium text-emerald-700">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          private context
        </span>
      </div>

      <div className="mb-5 flex flex-wrap gap-2">
        <button
          type="button"
          className="rounded-full border border-stone-200 bg-stone-50 px-3 py-2 text-xs font-medium text-stone-700 transition hover:border-orange-300 hover:text-orange-600"
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
          className="rounded-full border border-stone-200 bg-stone-50 px-3 py-2 text-xs font-medium text-stone-700 transition hover:border-orange-300 hover:text-orange-600"
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

      <label className="mb-5 flex items-center gap-3 text-[11px] font-medium uppercase tracking-[0.12em] text-stone-500">
        Provider
        <select
          value={providerChoice}
          onChange={(event) => setProviderChoice(event.target.value)}
          className="rounded-lg border border-stone-200 bg-stone-50 px-2.5 py-2 text-[11px] font-medium text-stone-700 outline-none transition focus:border-orange-400"
        >
          <option value="">Automatic</option>
          <option value="groq">Groq</option>
          <option value="mistral">Mistral</option>
        </select>
      </label>

      {answer && (
        <div className="mb-5 rounded-2xl border border-orange-100 bg-orange-50/40 p-4">
          <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-stone-500">
            {provider} response
          </div>
          <div className="space-y-3 text-sm leading-7 text-stone-700">
            <AnswerContent answer={answer} />
          </div>
        </div>
      )}

      {error && (
        <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <form className="flex gap-3" onSubmit={submit}>
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder={
            owner
              ? "Ask about this repository..."
              : "Ask about your GitHub profile..."
          }
          maxLength={4000}
          className="min-w-0 flex-1 rounded-xl border border-stone-200 bg-stone-50 px-4 py-3 text-sm text-stone-800 placeholder:text-stone-400 outline-none transition focus:border-orange-400 focus:bg-white"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-stone-900 px-5 py-3 text-sm font-semibold text-white shadow-[4px_4px_0_rgba(244,114,182,0.25)] transition hover:bg-stone-700 disabled:cursor-wait disabled:opacity-70"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>
    </section>
  );
}

export default ChatBox;
