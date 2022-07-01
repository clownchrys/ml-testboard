import { WithRowId } from "models";

export interface UserProfile extends WithRowId {
  m_id: string
  location_count: number
  story_number: string
  location_name: string
  location_code: string
}

