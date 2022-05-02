import { WithRowId } from "models";

export interface UserProfile extends WithRowId {
  m_id: string
  story_number: string
  jk_latestjobtitle_code?: string
  jk_jobtitle_code?: string
  jk_latestjobtitle_name?: string
  jk_jobtitle_name?: string
}
