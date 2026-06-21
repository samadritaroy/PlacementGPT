export interface EvaluationScore {
  clarity: number;
  correctness: number;
  depth: number;
  structure: number;
  overall: number;
  grade: string;
  percentile?: string;
  feedback: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface InterviewStartResponse {
  session_id: string;
  opening_message: string;
  company: string | null;
  role: string | null;
  session_type: string;
  difficulty: string;
}

export interface SessionProgress {
  questions_answered: number;
  avg_score_so_far: number;
  all_scores: { q: number; overall: number; grade: string }[];
}

export interface InterviewContinueResponse {
  response: string;
  evaluation: EvaluationScore;
  session_progress: SessionProgress;
  question_number: number;
}

export interface QuestionBreakdownItem {
  question_number: number;
  question_preview: string;
  scores: {
    clarity: number;
    correctness: number;
    depth: number;
    structure: number;
    overall: number;
  };
  grade: string;
  feedback: string;
}

export interface InterviewEndResponse {
  feedback: string;
  aggregate: EvaluationScore & { total_questions: number };
  question_breakdown: QuestionBreakdownItem[];
  total_questions: number;
  session_summary: string;
}