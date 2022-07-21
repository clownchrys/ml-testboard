import { WithRowId } from "models";

export interface ResultByGuestStoryInput extends WithRowId {
  story_number: number
}

export interface ResultByGuestStoryOutput extends WithRowId {
  story_title: string
  gno: number
  gi_title?: string
  //AGI_BizJobType_Name?: string
  recom_score?: number
  url?: string
}
