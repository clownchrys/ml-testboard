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
import type { ResultByUserStoryInput, ResultByUserStoryOutput } from "models/recom_adv/result_by_user_story";

type InputModel = ResultByUserStoryInput
type OutputModel = ResultByUserStoryOutput

const Description = `
  - 유저별 각 스토리 결과 검증
`

const story_options = [
      // { name: "-1", value: -1 }, // outlier test

      { name: "89", value: 89 },
      { name: "54", value: 54 },
      { name: "55", value: 55 },
      { name: "56", value: 56 },
      { name: "57", value: 57 },
      { name: "83", value: 83 },

      { name: "41", value: 41 },
      { name: "45", value: 45 },
      { name: "61", value: 61 },
      { name: "62", value: 62 },
      { name: "46", value: 46 },
      { name: "47", value: 47 },

      { name: "79", value: 79 },
      { name: "80", value: 80 },
      { name: "81", value: 81 },
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
  { title: "bizjobtype_name", dataIndex: "bizjobtype_name" },
  { title: "total_score", dataIndex: "total_score" },
  { title: "url", dataIndex: "url" },
]

function ResultByUserStory() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_adv/result_by_user_story"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="Adv 추천" functionName="유저별 스토리 결과 조회" desc={ Description }/>
      <SingleParamForm
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_adv/result_by_user_story" }
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
