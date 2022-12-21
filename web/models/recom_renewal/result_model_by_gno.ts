import { WithRowId } from "models";

export interface ResultModelByGnoInput {
  env: string
  gno: number
}

export interface ResultModelByGnoOutput extends WithRowId {
  gno: number
  gi_title: string
  jobname: string
  score: number
  link: string
}
