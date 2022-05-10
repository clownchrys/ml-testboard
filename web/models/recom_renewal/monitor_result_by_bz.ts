import { WithRowId } from "models";

export interface MonitorResultByBzInput {
  env: string
}

export interface MonitorResultByBzOutput extends WithRowId {
  m_id: string,
  bizjobtype_bctgr_name?: string,
  bizjobtype_name?: string
}
