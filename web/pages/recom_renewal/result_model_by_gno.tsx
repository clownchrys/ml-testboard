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
import type { ResultModelByGnoInput, ResultModelByGnoOutput } from "models/recom_renewal/result_model_by_gno";

type InputModel = ResultModelByGnoInput
type OutputModel = Partial<ResultModelByGnoOutput>

const Description = `
  - 모델 자체 추천 검증
`
const payload = "/recom_renewal/result_model_by_gno"

const fields: FieldDesc<InputModel>[] = [
  {
    param: "env",
    label: "개발환경",
    required: true,
    message: "env is required",
    placeholder: "개발환경",
    inputType: "Select",
    inputStyle: { width: 120 },
    selectOptions: [
      { name: "staging", value: "staging" },
      { name: "production", value: "prod" },
    ],
    // selectDefaultValue: "staging"
  },
  {
    param: "gno",
    label: "공고번호",
    required: true,
    message: "gno is required",
    placeholder: "공고번호",
    inputType: "Input",
    inputStyle: { width: 200 },
  }
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "rowid", dataIndex: "rowid", width: 100 },
  { title: "gno", dataIndex: "gno", width: 200 },
  { title: "gi_title", dataIndex: "gi_title" },
  { title: "jobname", dataIndex: "jobname", width: 300 },
  { title: "score", dataIndex: "score", width: 100 },
  { title: "link", dataIndex: "link", width: 200, ellipsis: true },
]

function ResultModelByGno() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu(payload))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="추천 구조개선" functionName="모델 결과 조회" desc={ Description }/>
      <SingleParamForm
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api" + payload }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default ResultModelByGno;
