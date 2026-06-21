"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { supabase } from "@/lib/supabase";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  Loader2,
} from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPwd, setShowPwd] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    setError("");
    setLoading(true);

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    setLoading(false);

    if (error) {
      setError(error.message);
      return;
    }

    router.push("/dashboard");
    router.refresh();
  }

  return (
    <div className="min-h-screen bg-[#0A0C10] flex items-center justify-center px-6 relative overflow-hidden">
      {/* Ambient glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[480px] h-[480px] bg-[#D9A441]/[0.06] rounded-full blur-[100px] pointer-events-none" />

      <div className="w-full max-w-sm relative">
        {/* Header */}
        <div className="text-center mb-8">
          <p className="text-[11px] font-mono text-[#D9A441] tracking-[0.2em] mb-3">
            AI PLACEMENT PREP
          </p>

          <h1 className="text-2xl font-bold text-[#ECE8DE]">
            Placement<span className="text-[#D9A441]">GPT</span>
          </h1>

          <p className="text-[#8B92A3] text-sm mt-2">
            Welcome back. Let's keep preparing.
          </p>
        </div>

        {/* Login Card */}
        <form
          onSubmit={handleLogin}
          className="bg-[#11141B] border border-[#252B38] rounded-2xl p-7 space-y-4"
        >
          {/* Email */}
          <div>
            <label className="block text-xs font-mono text-[#8B92A3] mb-1.5">
              Email
            </label>

            <div className="relative">
              <Mail
                size={15}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8B92A3]"
              />

              <input
                type="email"
                required
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError("");
                }}
                placeholder="you@iem.edu.in"
                className="w-full bg-[#0A0C10] border border-[#252B38] rounded-lg pl-9 pr-3.5 py-2.5 text-sm text-[#ECE8DE] placeholder:text-[#8B92A3]/60 focus:border-[#D9A441] focus:outline-none transition-colors"
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="block text-xs font-mono text-[#8B92A3] mb-1.5">
              Password
            </label>

            <div className="relative">
              <Lock
                size={15}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8B92A3]"
              />

              <input
                type={showPwd ? "text" : "password"}
                required
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setError("");
                }}
                placeholder="••••••••"
                className="w-full bg-[#0A0C10] border border-[#252B38] rounded-lg pl-9 pr-10 py-2.5 text-sm text-[#ECE8DE] placeholder:text-[#8B92A3]/60 focus:border-[#D9A441] focus:outline-none transition-colors"
              />

              <button
                type="button"
                onClick={() => setShowPwd((s) => !s)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8B92A3] hover:text-[#ECE8DE]"
                tabIndex={-1}
              >
                {showPwd ? (
                  <EyeOff size={16} />
                ) : (
                  <Eye size={16} />
                )}
              </button>
            </div>
          </div>

          {/* Forgot Password */}
          <div className="flex justify-end">
            <Link
              href="/forgot-password"
              className="text-xs text-[#D9A441] hover:underline"
            >
              Forgot Password?
            </Link>
          </div>

          {/* Error */}
          {error && (
            <p className="text-xs text-[#C1554B] bg-[#C1554B]/10 border border-[#C1554B]/30 rounded-lg px-3 py-2.5">
              {error}
            </p>
          )}

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-[#D9A441] text-[#0A0C10] font-semibold text-sm py-3 rounded-lg hover:bg-[#E8C171] disabled:opacity-50 transition-colors"
          >
            {loading ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <>
                Sign In <ArrowRight size={15} />
              </>
            )}
          </button>
        </form>

        {/* Footer */}
        <p className="text-center text-sm text-[#8B92A3] mt-6">
          New here?{" "}
          <Link
            href="/signup"
            className="text-[#D9A441] hover:underline"
          >
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}

