import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { Divider } from "antd";
import SingleParamForm from "components/FormModule/SingleParamForm";
import InfoComponent from "components/InfoComponent";
import TableComponent from "components/OutputModule/TableComponent";
import LoadingComponent from "components/LoadingComponent";
import { actions as menuActions } from "reducers/menu";
import { actions as tableActions } from "reducers/table";
import type { FieldDesc } from "types/form";
import type { ColumnType2 } from "types/table";
import type { ResultByUserStoryInput, ResultByUserStoryOutput } from "models/recom_am_adv/result_by_user_story";

type InputModel = ResultByUserStoryInput
type OutputModel = ResultByUserStoryOutput

const Description = `
  - 유저별 각 스토리 결과 검증
`



const story_options = [
      // { name: "-1", value: -1 }, // outlier test

  { name: "1", value: 1 },
  { name: "2", value: 2 },
  { name: "3", value: 3 },
  { name: "4", value: 4 },
  { name: "5", value: 5 },
  { name: "7", value: 7 },
  { name: "8", value: 8 },
  { name: "18", value: 18 },
  { name: "19", value: 19 },
  { name: "23", value: 23 },
  { name: "24", value: 24 },
  { name: "25", value: 25 },
  { name: "26", value: 26 },
  { name: "27", value: 27 },
  { name: "28", value: 28 },
  { name: "30", value: 30 },
  { name: "32", value: 32 },
  { name: "33", value: 33 },
  { name: "73", value: 73 },
  { name: "97", value: 97 },
  { name: "98", value: 98 },
]

const fields: FieldDesc<InputModel>[] = [
  {
    param: "story_number",
    label: "스토리 번호",
    required: true,
    message: "story_number is required",
    placeholder: "스토리 번호",
    inputType: "Select",
    inputStyle: { width: 120 },
    selectOptions: story_options.sort((a, b) => a.value - b.value)
  },
  {
    param: "m_id",
    label: "유저 아이디",
    required: true,
    message: "m_id is required",
    placeholder: "유저 아이디",
    inputType: "Input",
  },
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid", width: 150 },
  { title: "m_id", dataIndex: "m_id" },
  { title: "story_title", dataIndex: "story_title" },
  { title: "gi_title", dataIndex: "gi_title" },
  { title: "local_name", dataIndex: "local_name" },
  { title: "partname", dataIndex: "partname" },
  { title: "work_sdate", dataIndex: "work_sdate" },
  { title: "score", dataIndex: "score" },
  { title: "url", dataIndex: "url" },
  { title: "am_clickacum_cnt", dataIndex: "am_clickacum_cnt" },
  { title: "am_applyacum_cnt", dataIndex: "am_applyacum_cnt" },
]

function ResultByUserStory() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_am_adv/result_by_user_story"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="AM Adv 추천" functionName="유저별 스토리 결과 조회" desc={ Description }/>
      <SingleParamForm
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_am_adv/result_by_user_story" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default ResultByUserStory;
