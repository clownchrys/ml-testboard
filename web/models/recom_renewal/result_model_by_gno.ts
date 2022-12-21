import { WithRowId } from "models";

export interface ResultModelByGnoInput {
  env: string
  gno: number
}

export interface ResultModelByGnoOutput extends WithRowId {
  gno: number
  gi_title: string
  age_limit_over: number
  age_limit_under: number
  career: string
  edu_level_name: string
  jobname: string
  score: number
  link: string
}
