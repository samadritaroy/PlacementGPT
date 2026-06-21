import Link from "next/link";
import type { Metadata } from "next";
import {
  MessageSquareCode, Binary, FileText, Building2, ArrowRight,
} from "lucide-react";
import MiniDial from "@/components/MiniDial";

export const metadata: Metadata = {
  title: "PlacementGPT — AI placement preparation",
  description:
    "Mock interviews scored on clarity, correctness, depth and structure. DSA practice with hints, not answers. Resume scoring tuned to ATS systems.",
};

const FEATURES = [
  {
    icon: MessageSquareCode,
    title: "Mock interviews",
    desc: "Technical, HR, DSA and system-design rounds, each scored live across four dimensions — not just a transcript at the end.",
  },
  {
    icon: Binary,
    title: "DSA practice",
    desc: "Graduated hints: a nudge first, the pattern second, the full approach third. The answer is the last resort, not the first one.",
  },
  {
    icon: FileText,
    title: "Resume & ATS score",
    desc: "Upload your resume, paste the job description, get a score plus the exact keywords you're missing.",
  },
  {
    icon: Building2,
    title: "Company-specific prep",
    desc: "Amazon's leadership principles, Google's optimal-solution bias, TCS's fresher-level basics — tuned to how each company actually interviews.",
  },
];

const STEPS = [
  { n: "01", title: "Pick your target", desc: "Company, role, and round type — technical, HR, DSA, or system design." },
  { n: "02", title: "Answer like it's real", desc: "Chat with an AI interviewer that asks one question at a time and follows up on weak answers." },
  { n: "03", title: "Get scored immediately", desc: "Clarity, correctness, depth, and structure — after every single answer, not just at the end." },
  { n: "04", title: "Track what's improving", desc: "A dashboard that shows which dimension is actually getting better, and which one isn't." },
];

const COMPANIES = [
  { emoji: "📦", name: "Amazon" },
  { emoji: "🔍", name: "Google" },
  { emoji: "🪟", name: "Microsoft" },
  { emoji: "💼", name: "TCS" },
  { emoji: "🏢", name: "Infosys" },
  { emoji: "💡", name: "Wipro" },
  { emoji: "🛒", name: "Flipkart" },
];

const SCORES = [
  { label: "Clarity", value: 9 },
  { label: "Correctness", value: 8 },
  { label: "Depth", value: 7 },
  { label: "Structure", value: 9 },
];

export default function Home() {
  return (
    <div className="bg-[#0A0C10] min-h-screen">
      {/* ── NAV ────────────────────────────────────────────────── */}
      <header className="h-20 flex items-center justify-between px-6 sm:px-10 max-w-6xl mx-auto">
        <span className="font-bold text-[#ECE8DE]">
          Placement<span className="text-[#D9A441]">GPT</span>
        </span>

        <nav className="hidden sm:flex items-center gap-8 text-sm text-[#8B92A3]">
          <a href="#features" className="hover:text-[#ECE8DE] transition-colors">Features</a>
          <a href="#how-it-works" className="hover:text-[#ECE8DE] transition-colors">How it works</a>
        </nav>

        <div className="flex items-center gap-3">
          <Link href="/login" className="text-sm text-[#8B92A3] hover:text-[#ECE8DE] transition-colors hidden sm:block">
            Sign in
          </Link>
          <Link
            href="/signup"
            className="bg-[#D9A441] text-[#0A0C10] text-sm font-semibold px-4 py-2 rounded-lg hover:bg-[#E8C171] transition-colors"
          >
            Get started
          </Link>
        </div>
      </header>

      {/* ── HERO ───────────────────────────────────────────────── */}
      <section className="relative px-6 sm:px-10 py-16 sm:py-24 max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center overflow-hidden">
        <div className="absolute -top-20 left-1/4 w-[420px] h-[420px] bg-[#D9A441]/[0.06] rounded-full blur-[110px] pointer-events-none" />

        <div className="relative">
          <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-4">
            AI PLACEMENT PREPARATION
          </p>
          <h1 className="text-4xl sm:text-5xl font-bold text-[#ECE8DE] leading-[1.12] mb-6">
            Practice until the real interview feels like the rerun.
          </h1>
          <p className="text-[#8B92A3] text-base leading-relaxed mb-8 max-w-md">
            Mock interviews scored on clarity, correctness, depth, and
            structure. DSA practice that gives hints instead of answers.
            Resume scoring built around what ATS systems actually check.
            One tool, the whole placement cycle.
          </p>
          <div className="flex items-center gap-4">
            <Link
              href="/signup"
              className="flex items-center gap-2 bg-[#D9A441] text-[#0A0C10] font-semibold text-sm px-6 py-3.5 rounded-lg hover:bg-[#E8C171] transition-colors"
            >
              Start preparing — it's free <ArrowRight size={16} />
            </Link>
            <Link href="/login" className="text-sm text-[#8B92A3] hover:text-[#ECE8DE] transition-colors">
              I have an account
            </Link>
          </div>
        </div>

        {/* live mockup of the actual product, not a stock photo */}
        <div className="relative flex justify-center lg:justify-end">
          <div className="bg-[#11141B] border border-[#252B38] rounded-2xl p-5 w-full max-w-sm shadow-2xl shadow-black/50">
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-2 rounded-full bg-[#5FA777] animate-pulse" />
              <span className="text-xs font-mono text-[#8B92A3]">Technical · Amazon</span>
            </div>

            <div className="space-y-2.5 mb-4">
              <div className="bg-[#0A0C10] border border-[#252B38] rounded-lg rounded-bl-sm px-3.5 py-2.5 max-w-[88%]">
                <div className="text-[10px] text-[#8B92A3] font-mono mb-1">INTERVIEWER</div>
                <p className="text-xs text-[#ECE8DE] leading-relaxed">
                  Walk me through how you'd find two numbers in an array that sum to a target.
                </p>
              </div>
              <div className="bg-[#D9A441] rounded-lg rounded-br-sm px-3.5 py-2.5 max-w-[88%] ml-auto">
                <p className="text-xs text-[#0A0C10] leading-relaxed">
                  I'd use a hash map — store each number as I scan, check if the complement already exists. One pass, O(n).
                </p>
              </div>
            </div>

            <div className="flex items-center justify-between border-t border-[#252B38] pt-4">
              <div className="space-y-1.5 flex-1 mr-4">
                {SCORES.map(({ label, value }) => (
                  <div key={label}>
                    <div className="flex justify-between text-[10px] font-mono text-[#8B92A3] mb-0.5">
                      <span>{label}</span><span>{value}/10</span>
                    </div>
                    <div className="h-1 bg-[#1A1F2A] rounded-full">
                      <div className="h-full bg-[#5FA777] rounded-full" style={{ width: `${value * 10}%` }} />
                    </div>
                  </div>
                ))}
              </div>
              <MiniDial value={8.4} size={84} />
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS STRIP ────────────────────────────────────────── */}
      <section className="border-y border-[#252B38] py-8 px-6 sm:px-10">
        <div className="max-w-6xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
          {[
            ["4", "interview modes"],
            ["4", "scoring dimensions"],
            ["7", "companies profiled"],
            ["3", "graduated DSA hints"],
          ].map(([num, label]) => (
            <div key={label}>
              <div className="text-2xl font-bold text-[#D9A441] font-mono">{num}</div>
              <div className="text-xs text-[#8B92A3] mt-1">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── FEATURES ───────────────────────────────────────────── */}
      <section id="features" className="px-6 sm:px-10 py-20 max-w-6xl mx-auto">
        <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-3">WHAT IT DOES</p>
        <h2 className="text-2xl sm:text-3xl font-bold text-[#ECE8DE] mb-12 max-w-lg">
          Everything between "I should start preparing" and walking into the room.
        </h2>

        <div className="grid sm:grid-cols-2 gap-5">
          {FEATURES.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="bg-[#11141B] border border-[#252B38] rounded-xl p-6">
              <div className="w-10 h-10 rounded-lg bg-[#D9A441]/10 flex items-center justify-center mb-4">
                <Icon size={18} className="text-[#D9A441]" strokeWidth={1.75} />
              </div>
              <h3 className="text-[#ECE8DE] font-semibold mb-2">{title}</h3>
              <p className="text-sm text-[#8B92A3] leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── HOW IT WORKS ───────────────────────────────────────── */}
      <section id="how-it-works" className="px-6 sm:px-10 py-20 max-w-6xl mx-auto border-t border-[#252B38]">
        <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-3">HOW IT WORKS</p>
        <h2 className="text-2xl sm:text-3xl font-bold text-[#ECE8DE] mb-12 max-w-lg">
          Four steps, repeated until it's boring.
        </h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {STEPS.map(({ n, title, desc }) => (
            <div key={n}>
              <div className="text-3xl font-mono font-bold text-[#252B38] mb-3">{n}</div>
              <h3 className="text-[#ECE8DE] font-semibold mb-2">{title}</h3>
              <p className="text-sm text-[#8B92A3] leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── COMPANIES ──────────────────────────────────────────── */}
      <section className="px-6 sm:px-10 py-16 max-w-6xl mx-auto border-t border-[#252B38]">
        <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-6">
          INTERVIEW STYLES COVERED
        </p>
        <div className="flex flex-wrap gap-3">
          {COMPANIES.map(({ emoji, name }) => (
            <div
              key={name}
              className="flex items-center gap-2 bg-[#11141B] border border-[#252B38] rounded-full px-4 py-2"
            >
              <span>{emoji}</span>
              <span className="text-sm text-[#ECE8DE]">{name}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── FINAL CTA ──────────────────────────────────────────── */}
      <section className="px-6 sm:px-10 py-24 max-w-3xl mx-auto text-center border-t border-[#252B38]">
        <h2 className="text-3xl font-bold text-[#ECE8DE] mb-4">
          Your placement cycle starts now.
        </h2>
        <p className="text-[#8B92A3] mb-8">
          Free to start. No credit card, no recruiter watching.
        </p>
        <Link
          href="/signup"
          className="inline-flex items-center gap-2 bg-[#D9A441] text-[#0A0C10] font-semibold text-sm px-7 py-3.5 rounded-lg hover:bg-[#E8C171] transition-colors"
        >
          Create your account <ArrowRight size={16} />
        </Link>
      </section>

      {/* ── FOOTER ─────────────────────────────────────────────── */}
      <footer className="border-t border-[#252B38] px-6 sm:px-10 py-8">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="font-bold text-[#ECE8DE] text-sm">
            Placement<span className="text-[#D9A441]">GPT</span>
          </span>
          <p className="text-xs text-[#8B92A3] font-mono">
            AI-powered placement preparation platform.
          </p>
        </div>
      </footer>
    </div>
  );
}