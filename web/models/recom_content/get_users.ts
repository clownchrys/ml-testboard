import { WithRowId } from "models";

export interface GetUsersOutput extends WithRowId {
  uid: string
  activity_count: number
}
