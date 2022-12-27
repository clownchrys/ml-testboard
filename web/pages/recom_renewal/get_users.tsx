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
import type { GetUsersInput, GetUsersOutput } from "models/recom_renewal/get_users";

type InputModel = GetUsersInput
type OutputModel = GetUsersOutput

const Description = `
  - 추천 가능한 유저 목록 조회
  - 유저별 검증과 함께 활용
  - 서버 부하상의 이유로 최대 1만개의 유저만 추출
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
]

function GetUsers() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_renewal/get_users"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="추천 구조개선" functionName="유저 목록 조회" desc={ Description }/>
      <SingleParamForm
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_renewal/get_users" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default GetUsers;
