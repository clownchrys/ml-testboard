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
import type { ResultByIdOutput } from "models/recom_renewal/result_by_id";

type OutputModel = ResultByIdOutput

const Description = `
  - 직무산업별 추천 결과 확인
`

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid" },
  { title: "kind", dataIndex: "kind" },
  { title: "m_id", dataIndex: "m_id" },
  { title: "gno", dataIndex: "gno" },
  { title: "actvt_code", dataIndex: "actvt_code" },
  { title: "is_include", dataIndex: "is_include" },
  { title: "dt", dataIndex: "dt" },
  { title: "score", dataIndex: "score" },
  { title: "TITLE", dataIndex: "TITLE" },
  { title: "BZT_1", dataIndex: "BZT_1" },
  { title: "BZT_2", dataIndex: "BZT_2" },
  { title: "LOCAL_1", dataIndex: "LOCAL_1" },
  { title: "LOCAL_2", dataIndex: "LOCAL_2" },
  { title: "IS_PAID", dataIndex: "IS_PAID" },
  { title: "URL", dataIndex: "URL" },
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
