"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import {
  Lock,
  Loader2,
  ArrowRight,
  Eye,
  EyeOff,
} from "lucide-react";

export default function UpdatePasswordPage() {
  const [password, setPassword] = useState("");
  const [showPwd, setShowPwd] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const router = useRouter();

  async function handleUpdate(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    const { error } = await supabase.auth.updateUser({
      password,
    });

    setLoading(false);

    if (error) {
      setMessage(error.message);
      return;
    }

    setMessage("Password updated successfully!");

    setTimeout(() => {
      router.push("/login");
    }, 2000);
  }

  return (
    <div className="min-h-screen bg-[#0A0C10] flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-[#ECE8DE]">
            Reset Password
          </h1>

          <p className="text-[#8B92A3] text-sm mt-2">
            Enter your new password.
          </p>
        </div>

        <form
          onSubmit={handleUpdate}
          className="bg-[#11141B] border border-[#252B38] rounded-2xl p-7 space-y-4"
        >
          <div>
            <label className="block text-xs font-mono text-[#8B92A3] mb-1.5">
              New Password
            </label>

            <div className="relative">
              <Lock
                size={15}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8B92A3]"
              />

              <input
                type={showPwd ? "text" : "password"}
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-[#0A0C10] border border-[#252B38] rounded-lg pl-9 pr-10 py-2.5 text-[#ECE8DE] focus:border-[#D9A441] focus:outline-none"
              />

              <button
                type="button"
                onClick={() => setShowPwd(!showPwd)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8B92A3]"
              >
                {showPwd ? (
                  <EyeOff size={16} />
                ) : (
                  <Eye size={16} />
                )}
              </button>
            </div>
          </div>

          {message && (
            <p className="text-center text-sm text-[#D9A441]">
              {message}
            </p>
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
                Update Password
                <ArrowRight size={15} />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}