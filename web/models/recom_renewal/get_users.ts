import { WithRowId } from "models";

export interface GetUsersInput {
  env: string
}

export interface GetUsersOutput extends WithRowId {
  m_id: string
}
