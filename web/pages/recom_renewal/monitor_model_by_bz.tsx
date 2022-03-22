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
import type { MonitorModelByBzOutput } from "models/recom_renewal/monitor_model_by_bz";

type OutputModel = MonitorModelByBzOutput

const Description = `
  - 직무산업별 모델 출력 확인
`

const columns: ColumnType2<OutputModel>[] = [
  { title: "rowid", dataIndex: "rowid" },
  { title: "gno", dataIndex: "gno" },
  { title: "recom_gno", dataIndex: "recom_gno" },
  { title: "score", dataIndex: "score" },
  { title: "title", dataIndex: "title" },
  { title: "title_recom", dataIndex: "title_recom" },
  { title: "BZT_1", dataIndex: "BZT_1" },
  { title: "BZT_2", dataIndex: "BZT_2" },
  { title: "LOCAL_1", dataIndex: "LOCAL_1" },
  { title: "LOCAL_2", dataIndex: "LOCAL_2" },
]

function MonitorModelByBz() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_renewal/monitor_model_by_bz"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="추천 구조개선" functionName="모델 결과 조회" desc={ Description }/>
      <NoParamForm
        endpointApi={ "/api/recom_renewal/monitor_model_by_bz" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default MonitorModelByBz;
