import { WithRowId } from "models";

export interface ResultByUserStoryInput extends WithRowId {
  m_id: string
  story_number: number
}

export interface ResultByUserStoryOutput extends WithRowId {
  m_id: string
  story_title: string
  gi_title?: string
  local_name: string
  partname: string
  work_sdate: number
  score?: number
  url: string
  am_clickacum_cnt?: number
  am_applyacum_cnt?: number
}

