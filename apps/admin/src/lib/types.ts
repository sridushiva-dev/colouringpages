export type BookStatus =
  | "IDEA"
  | "RESEARCHED"
  | "BRIEFED"
  | "ART_IN_PROGRESS"
  | "ART_COMPLETE"
  | "PRODUCTION"
  | "QA_PASSED"
  | "LISTING_READY"
  | "AWAITING_PUBLISH_APPROVAL"
  | "PUBLISHED"
  | "LIVE_IN_APP";

export interface PendingAction {
  type: string;
  created_at: string;
  notes?: string;
}

export interface BookRecord {
  id: string;
  title: string;
  subtitle?: string;
  line: string;
  status: BookStatus;
  target_audience: string;
  trim: string;
  page_count?: number;
  art_page_count?: number;
  theme?: string;
  approvals?: Record<string, string>;
  pending_actions?: PendingAction[];
  agent_log?: Array<{ agent: string; at: string; message: string }>;
  updated_at?: string;
  rejection_notes?: string;
  pages?: Array<{ number: number; prompt?: string; subject?: string }>;
  listing?: { keywords?: string[] };
  app?: { qr_url?: string };
}
