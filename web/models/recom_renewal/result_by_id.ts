import { WithRowId } from "models";

export interface ResultByIdInput {
  m_id: string
  env: string
}

export interface ResultByIdOutput extends WithRowId {
  kind?: string
  m_id?: string
  gno?: number
  actvt_code?: string
  is_include?: string
  dt?: string
  score?: number
  TITLE?: string
  BZT_1?: string
  BZT_2?: string
  LOCAL_1?: string
  LOCAL_2?: string
  IS_PAID?: string
  URL?: string
}
