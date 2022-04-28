import { WithRowId } from "models";

export interface ResultOfInterviewReviewInput {
  uid: string
}

export interface ResultOfInterviewReviewOutput extends WithRowId {
  uid: string
  cont_no: number
  tag_type?: number
  tag_name?: string
  activity_count: number
  score?: number
  url: string
  sort_idx: number
}

