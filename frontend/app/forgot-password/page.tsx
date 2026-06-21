"use client";

import { useState } from "react";
import Link from "next/link";
import { supabase } from "@/lib/supabase";
import { Mail, Loader2, ArrowRight, CheckCircle2 } from "lucide-react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: "ok" | "err";
    text: string;
  } | null>(null);

  async function handleReset(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);
    setMessage(null);

    const { error } = await supabase.auth.resetPasswordForEmail(
      email,
      {
        redirectTo: "http://localhost:3000/update-password",
      }
    );

    setLoading(false);

    if (error) {
      setMessage({
        type: "err",
        text: error.message,
      });
    } else {
      setMessage({
        type: "ok",
        text: "Password reset link sent. Check your email.",
      });
    }
  }

  return (
    <div className="min-h-screen bg-[#0A0C10] flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-[#ECE8DE]">
            Forgot Password
          </h1>

          <p className="text-[#8B92A3] text-sm mt-2">
            Enter your email to receive a reset link.
          </p>
        </div>

        <form
          onSubmit={handleReset}
          className="bg-[#11141B] border border-[#252B38] rounded-2xl p-7 space-y-4"
        >
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
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full bg-[#0A0C10] border border-[#252B38] rounded-lg pl-9 pr-3 py-2.5 text-[#ECE8DE] focus:border-[#D9A441] focus:outline-none"
              />
            </div>
          </div>

          {message && (
            <div
              className={`text-xs rounded-lg px-3 py-3 border ${
                message.type === "ok"
                  ? "text-[#5FA777] bg-[#5FA777]/10 border-[#5FA777]/30"
                  : "text-[#C1554B] bg-[#C1554B]/10 border-[#C1554B]/30"
              }`}
            >
              {message.type === "ok" && (
                <CheckCircle2
                  size={14}
                  className="inline mr-2"
                />
              )}
              {message.text}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#D9A441] text-[#0A0C10] py-3 rounded-lg font-semibold flex items-center justify-center gap-2"
          >
            {loading ? (
              <Loader2
                size={16}
                className="animate-spin"
              />
            ) : (
              <>
                Send Reset Link
                <ArrowRight size={15} />
              </>
            )}
          </button>
        </form>

        <p className="text-center mt-6 text-sm text-[#8B92A3]">
          Remember your password?{" "}
          <Link
            href="/login"
            className="text-[#D9A441] hover:underline"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}