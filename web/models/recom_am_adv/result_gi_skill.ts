import { WithRowId } from "models";

export interface ResultGiSkillInput extends WithRowId {
  al_gi_no: number
}

export interface ResultGiSkillOutput extends WithRowId {
  al_gi_no: number
  profile_skl: string
}

