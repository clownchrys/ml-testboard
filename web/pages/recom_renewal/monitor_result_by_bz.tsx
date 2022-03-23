import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { Divider } from "antd";
import InfoComponent from "components/InfoComponent";
import NoParamForm from "components/FormModule/NoParamForm";
import TableComponent from "components/OutputModule/TableComponent";
import LoadingComponent from "components/LoadingComponent";
import { actions as menuActions } from "reducers/menu";
import { actions as tableActions } from "reducers/table";
import type { ColumnType2 } from "types/table";
import type { MonitorResultByBzOutput } from "models/recom_renewal/monitor_result_by_bz";

type OutputModel = MonitorResultByBzOutput

const Description = `
  - 직무별 유저 샘플링
  - 실제 추천 결과 확인을 위해 사용
`

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
      <NoParamForm
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
