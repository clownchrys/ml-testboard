import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { Divider } from "antd";
import InfoComponent from "components/InfoComponent";
import SingleParamForm from "components/FormModule/SingleParamForm";
import TableComponent from "components/OutputModule/TableComponent";
import LoadingComponent from "components/LoadingComponent";
import { actions as menuActions } from "reducers/menu";
import { actions as tableActions } from "reducers/table";
import type { FieldDesc } from "types/form";
import type { ColumnType2 } from "types/table";
import type { MonitorResultByBzInput, MonitorResultByBzOutput } from "models/recom_renewal/monitor_result_by_bz";

type InputModel = MonitorResultByBzInput
type OutputModel = MonitorResultByBzOutput

const Description = `
  - 직무별 유저 샘플링
  - 실제 추천 결과 확인을 위해 사용
`

const fields: FieldDesc<InputModel>[] = [
  {
    param: "env",
    label: "개발환경",
    required: true,
    message: "env is required",
    placeholder: "개발환경",
    inputType: "Select",
    inputStyle: { width: 120 },
    availableOpt: [
      { name: "staging", value: "staging" },
      { name: "production", value: "prod" },
    ]
  },
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid", width: 150 },
  { title: "m_id", dataIndex: "m_id" },
  { title: "bizjobtype_bctgr_name", dataIndex: "bizjobtype_bctgr_name" },
  { title: "bizjobtype_name", dataIndex: "bizjobtype_name" },
]

function MonitorResultByBz() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_renewal/monitor_result_by_bz"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="추천 구조개선" functionName="추천 결과 조회" desc={ Description }/>
      <SingleParamForm
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_renewal/monitor_result_by_bz" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default MonitorResultByBz;
