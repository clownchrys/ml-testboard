import { WithRowId } from "models";

export interface ResultByUserStoryInput extends WithRowId {
  m_id: string
  story_number: number
}

export interface ResultByUserStoryOutput extends WithRowId {
  m_id?: string
  story_title: string
  gno: number
  gi_title?: string
  abn_bizjobtype_name?: string
  job_bizjobtype_name?: string
  jk_jobtitle_name?: string
  recom_score?: number
  url?: string
}
