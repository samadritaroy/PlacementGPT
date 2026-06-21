"use client";

import { useState } from "react";
import Link from "next/link";
import { supabase } from "@/lib/supabase";
import { User, Mail, Lock, Eye, EyeOff, ArrowRight, Loader2, CheckCircle2 } from "lucide-react";

export default function SignupPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPwd, setShowPwd] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "ok" | "err"; text: string } | null>(null);

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setMessage(null);
    setLoading(true);

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { full_name: fullName } }, // ← captured for the dashboard greeting
    });

    setLoading(false);

    if (error) {
      setMessage({ type: "err", text: error.message });
    } else {
      setMessage({
        type: "ok",
        text: "Account created. Check your email to confirm, then sign in.",
      });
    }
  }

  return (
    <div className="min-h-screen bg-[#0A0C10] flex items-center justify-center px-6 relative overflow-hidden">
      {/* one tasteful ambient glow — the only decoration on this page */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[480px] h-[480px] bg-[#D9A441]/[0.06] rounded-full blur-[100px] pointer-events-none" />

      <div className="w-full max-w-sm relative">
        <div className="text-center mb-8">
          <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-3">
            AI PLACEMENT PREP
          </p>
          <h1 className="text-2xl font-bold text-[#ECE8DE]">
            Placement<span className="text-[#D9A441]">GPT</span>
          </h1>
          <p className="text-[#8B92A3] text-sm mt-2">
            Create your account to start preparing
          </p>
        </div>

        <form
          onSubmit={handleSignup}
          className="bg-[#11141B] border border-[#252B38] rounded-2xl p-7 space-y-4"
        >
          <Field icon={User} label="Full name">
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Samadrita Roy"
              className={inputClass}
            />
          </Field>

          <Field icon={Mail} label="Email">
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@iem.edu.in"
              className={inputClass}
            />
          </Field>

          <Field icon={Lock} label="Password">
            <div className="relative">
              <input
                type={showPwd ? "text" : "password"}
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="min. 6 characters"
                className={inputClass + " pr-10"}
              />
              <button
                type="button"
                onClick={() => setShowPwd((s) => !s)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8B92A3] hover:text-[#ECE8DE]"
                tabIndex={-1}
              >
                {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </Field>

          {message && (
            <div
              className={`flex items-start gap-2 text-xs rounded-lg px-3 py-2.5 border ${
                message.type === "ok"
                  ? "text-[#5FA777] bg-[#5FA777]/10 border-[#5FA777]/30"
                  : "text-[#C1554B] bg-[#C1554B]/10 border-[#C1554B]/30"
              }`}
            >
              {message.type === "ok" && <CheckCircle2 size={14} className="mt-0.5 shrink-0" />}
              <span>{message.text}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-[#D9A441] text-[#0A0C10] font-semibold text-sm py-3 rounded-lg hover:bg-[#E8C171] disabled:opacity-50 transition-colors"
          >
            {loading ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <>
                Create account <ArrowRight size={15} />
              </>
            )}
          </button>
        </form>

        <p className="text-center text-sm text-[#8B92A3] mt-6">
          Already have an account?{" "}
          <Link href="/login" className="text-[#D9A441] hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

// ── shared field wrapper (keeps labels + icons consistent) ──────
const inputClass =
  "w-full bg-[#0A0C10] border border-[#252B38] rounded-lg pl-9 pr-3.5 py-2.5 text-sm text-[#ECE8DE] placeholder:text-[#8B92A3]/60 focus:border-[#D9A441] focus:outline-none transition-colors";

function Field({
  icon: Icon,
  label,
  children,
}: {
  icon: React.ComponentType<{ size?: number; className?: string }>;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="block text-xs font-mono text-[#8B92A3] mb-1.5">{label}</label>
      <div className="relative">
        <Icon size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8B92A3]" />
        {children}
      </div>
    </div>
  );
}