import { WithRowId } from "models";

export interface UserProfile extends WithRowId {
  m_id: string
  abn_bizjobtype_name?: string
  job_bizjobtype_name?: string
  jk_jobtitle_name?: string
}
