"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { useRequireAuth } from "@/lib/useRequireAuth";
import {
  LogOut, Loader2, MessageSquareCode, FileText,
  Building2, Binary, ChevronRight,
} from "lucide-react";

const QUICK_LINKS = [
  { href: "/dashboard/interview", label: "Start mock interview", desc: "AI interviewer, scored live", icon: MessageSquareCode },
  { href: "/dashboard/resume",    label: "Analyze resume",       desc: "ATS score + skill gaps",      icon: FileText },
  { href: "/dashboard/company",   label: "Company prep",         desc: "Amazon, Google, TCS & more",  icon: Building2 },
  { href: "/dashboard/dsa",       label: "Practice DSA",          desc: "Graduated hints, no spoilers", icon: Binary },
];

export default function DashboardPage() {
  const { user, loading } = useRequireAuth();
  const router = useRouter();

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0C10] flex items-center justify-center">
        <Loader2 size={28} className="animate-spin text-[#D9A441]" />
      </div>
    );
  }

  const fullName = (user?.user_metadata?.full_name as string) || user?.email?.split("@")[0] || "there";
  const firstName = fullName.split(" ")[0];

  async function handleLogout() {
    await supabase.auth.signOut();
    router.push("/login");
  }

  return (
    <div className="min-h-screen bg-[#0A0C10]">
      {/* top bar */}
      <header className="h-20 border-b border-[#252B38] flex items-center justify-between px-6 sm:px-10">
        <span className="font-bold text-[#ECE8DE]">
          Placement<span className="text-[#D9A441]">GPT</span>
        </span>
        <div className="flex items-center gap-4">
          <span className="text-xs text-[#8B92A3] font-mono hidden sm:block">{user?.email}</span>
          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 text-xs text-[#8B92A3] hover:text-[#C1554B] border border-[#252B38] rounded-full px-3 py-1.5 transition-colors"
          >
            <LogOut size={13} /> Sign out
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 sm:px-10 py-10">
        <h1 className="text-2xl font-bold text-[#ECE8DE]">
          Welcome back, {firstName}
        </h1>
        <p className="text-[#8B92A3] text-sm mt-1 font-mono">status: ready to prepare</p>

        <div className="grid sm:grid-cols-2 gap-3 mt-8">
          {QUICK_LINKS.map(({ href, label, desc, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center justify-between bg-[#11141B] border border-[#252B38] rounded-xl px-5 py-4 hover:border-[#D9A441]/40 transition-colors group"
            >
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-[#D9A441]/10 flex items-center justify-center">
                  <Icon size={17} className="text-[#D9A441]" strokeWidth={1.75} />
                </div>
                <div>
                  <div className="text-sm text-[#ECE8DE]">{label}</div>
                  <div className="text-xs text-[#8B92A3]">{desc}</div>
                </div>
              </div>
              <ChevronRight size={16} className="text-[#8B92A3] group-hover:text-[#D9A441] transition-colors" />
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}