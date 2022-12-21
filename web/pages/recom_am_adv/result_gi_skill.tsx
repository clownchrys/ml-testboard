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
import type { ResultGiSkillInput, ResultGiSkillOutput } from "models/recom_am_adv/result_gi_skill";

type InputModel = ResultGiSkillInput
type OutputModel = ResultGiSkillOutput

const Description = `
설명이 없습니다
`

const fields: FieldDesc<InputModel>[] = [
  {
    param: "al_gi_no",
    label: "공고 아이디",
    required: true,
    message: "al_gi_no is required",
    placeholder: "공고 아이디",
    inputType: "Input",
  },
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid" },
  { title: "al_gi_no", dataIndex: "al_gi_no" },
  { title: "profile_skl", dataIndex: "profile_skl" },
]

function ResultGiSkill() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_am_adv/result_gi_skill"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="AM Adv 추천" functionName="공고별 프로파일 스킬 조회" desc={ Description }/>
      <SingleParamForm<InputModel, OutputModel>
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_am_adv/result_gi_skill" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default ResultGiSkill;
