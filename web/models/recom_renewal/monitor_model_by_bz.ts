import { WithRowId } from "models";

export interface MonitorModelByBzOutput extends WithRowId {
  gno: number
  recom_gno: number
  score: number
  title?: string
  title_recom?: string
  BZT_1?: string
  BZT_2?: string
  LOCAL_1?: string
  LOCAL_2?: string
}
