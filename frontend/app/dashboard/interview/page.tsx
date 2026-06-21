"use client";
import ReactMarkdown from "react-markdown";
import { useEffect, useRef, useState } from "react";
import { useRequireAuth } from "@/lib/useRequireAuth";
import { api } from "@/lib/api";
import ScoreDial from "@/components/ScoreDial";
import { Loader2, Send, StopCircle, Play, ChevronDown, RotateCcw } from "lucide-react";
import type {
  ChatMessage, EvaluationScore, SessionProgress,
  InterviewStartResponse, InterviewContinueResponse, InterviewEndResponse,
} from "@/lib/types";

const SESSION_TYPES = [
  { key: "technical", label: "Technical" },
  { key: "hr", label: "HR Round" },
  { key: "dsa", label: "DSA / Coding" },
  { key: "system_design", label: "System Design" },
];

const COMPANIES = ["Amazon", "Google", "Microsoft", "TCS", "Infosys", "Wipro", "Flipkart"];

const DIFFICULTIES: { key: "easy" | "medium" | "hard"; label: string; color: string }[] = [
  { key: "easy", label: "Easy", color: "#5FA777" },
  { key: "medium", label: "Medium", color: "#D9A441" },
  { key: "hard", label: "Hard", color: "#C1554B" },
];

function gradeColor(grade?: string) {
  if (!grade) return "#8B92A3";
  if (["A+", "A"].includes(grade)) return "#5FA777";
  if (["B+", "B"].includes(grade)) return "#D9A441";
  return "#C1554B";
}

export default function InterviewPage() {
  const { loading: authLoading } = useRequireAuth();

  const [phase, setPhase] = useState<"config" | "active" | "ended">("config");
  const [config, setConfig] = useState({
    session_type: "technical",
    company: "",
    role: "",
    difficulty: "medium" as "easy" | "medium" | "hard",
  });

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [currentScore, setCurrentScore] = useState<EvaluationScore | null>(null);
  const [progress, setProgress] = useState<SessionProgress | null>(null);
  const [results, setResults] = useState<InterviewEndResponse | null>(null);
  const [tab, setTab] = useState<"feedback" | "breakdown">("feedback");

  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (authLoading) {
    return (
      <div className="min-h-screen bg-[#0A0C10] flex items-center justify-center">
        <Loader2 size={28} className="animate-spin text-[#D9A441]" />
      </div>
    );
  }

  async function startInterview() {
    setLoading(true);
    try {
      const { data } = await api.post<InterviewStartResponse>("/mock-interview/start", {
        session_type: config.session_type,
        company: config.company || undefined,
        role: config.role || undefined,
        difficulty: config.difficulty,
      });
      setSessionId(data.session_id);
      setMessages([{ role: "assistant", content: data.opening_message }]);
      setProgress({ questions_answered: 0, avg_score_so_far: 0, all_scores: [] });
      setCurrentScore(null);
      setPhase("active");
      setTimeout(() => inputRef.current?.focus(), 100);
    } catch (e: any) {
      alert("Failed to start interview: " + e.message);
    } finally {
      setLoading(false);
    }
  }

  async function sendAnswer() {
    if (!input.trim() || loading || !sessionId) return;
    const answer = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: answer }]);
    setLoading(true);
    setCurrentScore(null);

    try {
      const { data } = await api.post<InterviewContinueResponse>("/mock-interview/continue", {
        session_id: sessionId,
        answer,
      });
      setMessages((m) => [...m, { role: "assistant", content: data.response }]);
      setCurrentScore(data.evaluation);
      setProgress(data.session_progress);
      inputRef.current?.focus();
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", content: "⚠️ " + e.message }]);
    } finally {
      setLoading(false);
    }
  }

  async function endInterview() {
    if (!sessionId) return;
    setLoading(true);
    try {
      const { data } = await api.post<InterviewEndResponse>("/mock-interview/end", {
        session_id: sessionId,
      });
      setResults(data);
      setPhase("ended");
    } catch (e: any) {
      alert("Failed to end interview: " + e.message);
    } finally {
      setLoading(false);
    }
  }

  function resetAll() {
    setPhase("config");
    setSessionId(null);
    setMessages([]);
    setInput("");
    setCurrentScore(null);
    setProgress(null);
    setResults(null);
  }

  // ── CONFIG SCREEN ──────────────────────────────────────────
  if (phase === "config") {
    return (
      <div className="min-h-screen bg-[#0A0C10] px-6 py-12">
        <div className="max-w-md mx-auto">
          <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-3">MOCK INTERVIEW</p>
          <h1 className="text-2xl font-bold text-[#ECE8DE] mb-2">Configure your session</h1>
          <p className="text-sm text-[#8B92A3] mb-8">
            Every answer gets scored live. Full breakdown at the end.
          </p>

          <div className="bg-[#11141B] border border-[#252B38] rounded-2xl p-6 space-y-6">
            <div>
              <label className="block text-xs font-mono text-[#8B92A3] mb-2">INTERVIEW TYPE</label>
              <div className="grid grid-cols-2 gap-2">
                {SESSION_TYPES.map(({ key, label }) => (
                  <button
                    key={key}
                    onClick={() => setConfig((c) => ({ ...c, session_type: key }))}
                    className={`py-2.5 rounded-lg text-sm font-medium border transition-colors ${
                      config.session_type === key
                        ? "border-[#D9A441] bg-[#D9A441]/10 text-[#D9A441]"
                        : "border-[#252B38] text-[#8B92A3] hover:text-[#ECE8DE]"
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-mono text-[#8B92A3] mb-2">
                COMPANY <span className="text-[#8B92A3]/50">(optional)</span>
              </label>
              <div className="relative">
                <select
                  value={config.company}
                  onChange={(e) => setConfig((c) => ({ ...c, company: e.target.value }))}
                  className="w-full bg-[#0A0C10] border border-[#252B38] rounded-lg px-3.5 py-2.5 text-sm text-[#ECE8DE] focus:border-[#D9A441] outline-none appearance-none cursor-pointer"
                >
                  <option value="">Generic / Any</option>
                  {COMPANIES.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
                <ChevronDown size={15} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8B92A3] pointer-events-none" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-mono text-[#8B92A3] mb-2">
                ROLE <span className="text-[#8B92A3]/50">(optional)</span>
              </label>
              <input
                value={config.role}
                onChange={(e) => setConfig((c) => ({ ...c, role: e.target.value }))}
                placeholder="Software Engineer"
                className="w-full bg-[#0A0C10] border border-[#252B38] rounded-lg px-3.5 py-2.5 text-sm text-[#ECE8DE] placeholder:text-[#8B92A3]/50 focus:border-[#D9A441] outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-mono text-[#8B92A3] mb-2">DIFFICULTY</label>
              <div className="flex gap-2">
                {DIFFICULTIES.map(({ key, label, color }) => (
                  <button
                    key={key}
                    onClick={() => setConfig((c) => ({ ...c, difficulty: key }))}
                    className="flex-1 py-2 rounded-lg text-sm font-medium border transition-colors"
                    style={
                      config.difficulty === key
                        ? { borderColor: color, backgroundColor: `${color}1A`, color }
                        : { borderColor: "#252B38", color: "#8B92A3" }
                    }
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={startInterview}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-[#D9A441] text-[#0A0C10] font-semibold text-sm py-3 rounded-lg hover:bg-[#E8C171] disabled:opacity-50 transition-colors"
            >
              {loading ? <Loader2 size={16} className="animate-spin" /> : <><Play size={15} /> Start interview</>}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── ENDED / RESULTS SCREEN ─────────────────────────────────
  if (phase === "ended" && results) {
    const agg = results.aggregate;
    return (
      <div className="min-h-screen bg-[#0A0C10] px-6 py-12">
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <div className="text-4xl mb-3">{agg.overall >= 8 ? "🏆" : agg.overall >= 6 ? "💪" : "📚"}</div>
            <h1 className="text-2xl font-bold text-[#ECE8DE]">Interview complete</h1>
            <p className="text-sm text-[#8B92A3] mt-2 font-mono">{results.session_summary}</p>
          </div>

          <div className="grid grid-cols-5 gap-2.5 mb-8">
            {[
              { label: "Overall", value: agg.overall, special: true },
              { label: "Clarity", value: agg.clarity, special: false },
              { label: "Correct.", value: agg.correctness, special: false },
              { label: "Depth", value: agg.depth, special: false },
              { label: "Struct.", value: agg.structure, special: false },
            ].map(({ label, value, special }) => (
              <div
                key={label}
                className="rounded-xl p-3 text-center border"
                style={
                  special
                    ? { borderColor: "#D9A44140", backgroundColor: "#D9A44115" }
                    : { borderColor: "#252B38", backgroundColor: "#11141B" }
                }
              >
                <div className="font-mono font-bold" style={{ fontSize: special ? 24 : 18, color: gradeColor(agg.grade) }}>
                  {value.toFixed(1)}
                </div>
                <div className="text-[10px] text-[#8B92A3] mt-1">{label}</div>
              </div>
            ))}
          </div>

          <div className="flex justify-center mb-8">
            <span
              className="text-xs font-mono font-semibold px-3 py-1.5 rounded-md border"
              style={{ color: gradeColor(agg.grade), borderColor: `${gradeColor(agg.grade)}40`, backgroundColor: `${gradeColor(agg.grade)}15` }}
            >
              {agg.grade}{agg.percentile ? ` · ${agg.percentile}` : ""}
            </span>
          </div>

          <div className="flex gap-2 mb-5">
            {(["feedback", "breakdown"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                  tab === t ? "border-[#D9A441] text-[#D9A441] bg-[#D9A441]/10" : "border-[#252B38] text-[#8B92A3]"
                }`}
              >
                {t === "feedback" ? "AI feedback" : "Question breakdown"}
              </button>
            ))}
          </div>

          {tab === "feedback" && (
            <div className="bg-[#11141B] border border-[#252B38] rounded-xl p-6">
              <div className="prose prose-invert max-w-none prose-p:text-[#ECE8DE] prose-strong:text-[#D9A441] prose-li:text-[#ECE8DE]">
                <ReactMarkdown>
                    {results.feedback}
                </ReactMarkdown>
                </div>
            </div>
          )}

          {tab === "breakdown" && (
            <div className="space-y-3">
              {results.question_breakdown.map((q) => (
                <div key={q.question_number} className="bg-[#11141B] border border-[#252B38] rounded-xl p-5">
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="flex items-start gap-2">
                      <span className="text-xs font-mono text-[#D9A441] border border-[#D9A441]/30 bg-[#D9A441]/10 rounded px-1.5 py-0.5 shrink-0">
                        Q{q.question_number}
                      </span>
                      <span className="text-sm text-[#ECE8DE]">{q.question_preview}</span>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="font-mono font-bold" style={{ color: gradeColor(q.grade) }}>
                        {q.scores.overall.toFixed(1)}
                      </span>
                      <span className="text-xs font-mono px-1.5 py-0.5 rounded border" style={{ color: gradeColor(q.grade), borderColor: `${gradeColor(q.grade)}40` }}>
                        {q.grade}
                      </span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 mb-3">
                    {(["clarity", "correctness", "depth", "structure"] as const).map((dim) => (
                      <div key={dim}>
                        <div className="flex justify-between text-[10px] font-mono text-[#8B92A3] mb-0.5">
                          <span className="capitalize">{dim}</span><span>{q.scores[dim]}/10</span>
                        </div>
                        <div className="h-1 bg-[#1A1F2A] rounded-full">
                          <div className="h-full rounded-full" style={{ width: `${q.scores[dim] * 10}%`, backgroundColor: gradeColor(q.grade) }} />
                        </div>
                      </div>
                    ))}
                  </div>
                  {q.feedback && (
                    <div className="text-xs bg-[#0A0C10] rounded-lg p-3">
                        <div className="prose prose-invert max-w-none prose-p:text-[#8B92A3] prose-li:text-[#8B92A3] prose-strong:text-[#D9A441]">
                            <ReactMarkdown>
                                {q.feedback}
                            </ReactMarkdown>
                        </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-10">
            <button
              onClick={resetAll}
              className="inline-flex items-center gap-2 bg-[#D9A441] text-[#0A0C10] font-semibold text-sm px-6 py-3 rounded-lg hover:bg-[#E8C171] transition-colors"
            >
              <RotateCcw size={15} /> Start new interview
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── ACTIVE INTERVIEW ───────────────────────────────────────
  return (
    <div className="min-h-screen bg-[#0A0C10] px-6 py-6">
      <div className="max-w-4xl mx-auto flex gap-5">
        <div className="flex-1 flex flex-col" style={{ height: "calc(100vh - 80px)" }}>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2.5">
              <span className="w-2 h-2 rounded-full bg-[#5FA777] animate-pulse" />
              <span className="text-sm font-semibold text-[#ECE8DE] capitalize">
                {config.session_type.replace("_", " ")}
              </span>
              {config.company && <span className="text-sm text-[#8B92A3]">· {config.company}</span>}
              {progress && progress.questions_answered > 0 && (
                <span className="text-xs font-mono text-[#D9A441] bg-[#D9A441]/10 border border-[#D9A441]/30 rounded px-2 py-0.5">
                  Q{progress.questions_answered}
                </span>
              )}
            </div>
            <button
              onClick={endInterview}
              disabled={loading}
              className="flex items-center gap-1.5 text-xs text-[#C1554B] border border-[#C1554B]/30 rounded-full px-3 py-1.5 hover:bg-[#C1554B]/10 transition-colors disabled:opacity-50"
            >
              <StopCircle size={13} /> End & get results
            </button>
          </div>

          <div className="flex-1 bg-[#11141B] border border-[#252B38] rounded-xl p-4 overflow-y-auto flex flex-col gap-3">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`max-w-[85%] rounded-xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap ${
                  m.role === "user" ? "self-end bg-[#D9A441] text-[#0A0C10]" : "self-start bg-[#0A0C10] border border-[#252B38] text-[#ECE8DE]"
                }`}
              >
                {m.role === "assistant" && (
                  <div className="text-[10px] font-mono text-[#8B92A3] mb-1">INTERVIEWER</div>
                )}
                {m.content}
              </div>
            ))}
            {loading && (
              <div className="self-start bg-[#0A0C10] border border-[#252B38] rounded-xl px-4 py-3 flex gap-1.5">
                {[0, 1, 2].map((i) => (
                  <span key={i} className="w-1.5 h-1.5 rounded-full bg-[#8B92A3] animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="bg-[#11141B] border border-[#252B38] rounded-xl p-3 mt-3 flex gap-2.5 items-end">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendAnswer();
                }
              }}
              placeholder="Type your answer… (Enter to send, Shift+Enter for new line)"
              rows={3}
              className="flex-1 bg-transparent text-sm text-[#ECE8DE] placeholder:text-[#8B92A3]/50 outline-none resize-none"
            />
            <button
              onClick={sendAnswer}
              disabled={loading || !input.trim()}
              className="w-10 h-10 rounded-lg bg-[#D9A441] flex items-center justify-center hover:bg-[#E8C171] disabled:opacity-40 transition-colors shrink-0"
            >
              <Send size={15} className="text-[#0A0C10]" />
            </button>
          </div>

          {/* mobile fallback — sidebar below is hidden under lg, so show a compact strip here instead */}
          {currentScore && (
            <div className="lg:hidden mt-3 bg-[#11141B] border border-[#252B38] rounded-xl p-3 flex items-center justify-between">
              <span className="text-xs font-mono text-[#8B92A3]">Last answer</span>
              <div className="flex items-center gap-3">
                <span className="font-mono font-bold" style={{ color: gradeColor(currentScore.grade) }}>
                  {currentScore.overall.toFixed(1)}
                </span>
                <span className="text-xs font-mono px-1.5 py-0.5 rounded border" style={{ color: gradeColor(currentScore.grade), borderColor: `${gradeColor(currentScore.grade)}40` }}>
                  {currentScore.grade}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* live score sidebar — desktop only */}
        <div className="w-56 shrink-0 hidden lg:block">
          <div className="bg-[#11141B] border border-[#252B38] rounded-xl p-4 sticky top-6">
            <div className="text-[10px] font-mono text-[#8B92A3] tracking-wide mb-4">LIVE SCORE</div>

            {currentScore ? (
              <>
                <div className="flex justify-center mb-3">
                  <ScoreDial value={currentScore.overall} size={100} />
                </div>
                <div className="flex justify-center mb-4">
                  <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded border" style={{ color: gradeColor(currentScore.grade), borderColor: `${gradeColor(currentScore.grade)}40` }}>
                    {currentScore.grade}
                  </span>
                </div>
                {(["clarity", "correctness", "depth", "structure"] as const).map((dim) => (
                  <div key={dim} className="mb-2">
                    <div className="flex justify-between text-[10px] font-mono text-[#8B92A3] mb-0.5">
                      <span className="capitalize">{dim}</span><span>{currentScore[dim]}/10</span>
                    </div>
                    <div className="h-1 bg-[#1A1F2A] rounded-full">
                      <div className="h-full rounded-full transition-all duration-500" style={{ width: `${currentScore[dim] * 10}%`, backgroundColor: gradeColor(currentScore.grade) }} />
                    </div>
                  </div>
                ))}
                {currentScore.feedback && (
                  <p className="text-[11px] text-[#8B92A3] leading-relaxed bg-[#0A0C10] rounded-lg p-2.5 mt-3">
                    {currentScore.feedback}
                  </p>
                )}
              </>
            ) : (
              <p className="text-xs text-[#8B92A3] text-center py-6">
                Answer a question to see your score
              </p>
            )}

            {progress && progress.questions_answered > 0 && (
              <div className="mt-4 pt-4 border-t border-[#252B38] text-center">
                <div className="text-[10px] font-mono text-[#8B92A3]">SESSION AVG</div>
                <div className="text-xl font-mono font-bold text-[#ECE8DE] mt-1">
                  {progress.avg_score_so_far.toFixed(1)}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}