import { WithRowId } from "models";

export interface ResultByUserStoryInput extends WithRowId {
  m_id: string
  story_number: number
}

export interface ResultByUserStoryOutput extends WithRowId {
  m_id: string
  gi_title?: string
  bizjobtype_name?: string
  total_score?: number
  url: string
}
