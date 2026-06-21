import { api } from "@/lib/api";

export async function startInterview(data: {
  session_type: string;
  company?: string;
  role?: string;
  difficulty: string;
}) {
  const response = await api.post("/mock-interview/start", data);
  return response.data;
}

export async function continueInterview(data: {
  session_id: string;
  answer: string;
}) {
  const response = await api.post("/mock-interview/continue", data);
  return response.data;
}

export async function endInterview(data: {
  session_id: string;
}) {
  const response = await api.post("/mock-interview/end", data);
  return response.data;
}