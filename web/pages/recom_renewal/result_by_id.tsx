import { useEffect } from "react";
import { Input, Divider } from "antd";
import InfoComponent from "components/InfoComponent";
import TableComponent from "components/OutputModule/TableComponent";
import SingleParamForm from "components/FormModule/SingleParamForm";
import { useDispatch } from "react-redux";
import { actions as menuActions } from "reducers/menu";
import { actions as tableActions } from "reducers/table";
import type { Field } from "types/form";
import type { ColumnType2 } from "types/table";
import type { ResultByIdInput, ResultByIdOutput } from "models/recom_renewal/result_by_id";
import { useRouter } from "next/router";
import LoadingComponent from "../../components/LoadingComponent"; // change this to use other models

type InputModel = ResultByIdInput
type OutputModel = ResultByIdOutput

const Description = `
  - 유저별 추천 공고 검증
  - 공고유사도 Threshold: 0.9
  - 추천 스코어 산술식: avg( similarity + (1 - similarity) * weight )
`

const fields: Field<InputModel>[] = [
  {
    param: "m_id",
    label: "유저 아이디",
    required: true,
    message: "m_id is required",
    placeholder: "유저 아이디",
    inputCls: "Input",
  },
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "rowid", dataIndex: "rowid" },
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

function ResultById() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_renewal/result_by_id"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="추천 구조개선" functionName="유저별 검증" desc={ Description }/>
      <SingleParamForm<InputModel, OutputModel>
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_renewal/result_by_id" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default ResultById;
