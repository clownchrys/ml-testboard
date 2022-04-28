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
import type { ResultOfInterviewReviewInput, ResultOfInterviewReviewOutput } from "models/recom_content/result_of_interview_review";

type InputModel = ResultOfInterviewReviewInput
type OutputModel = ResultOfInterviewReviewOutput

const Description = `
설명이 없습니다
`

const fields: FieldDesc<InputModel>[] = [
  {
    param: "uid",
    label: "유저 아이디",
    required: true,
    message: "uid is required",
    placeholder: "유저 아이디",
    inputType: "Input",
  },
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid" },
  { title: "uid", dataIndex: "uid" },
  { title: "cont_no", dataIndex: "cont_no" },
  { title: "tag_type", dataIndex: "tag_type" },
  { title: "tag_name", dataIndex: "tag_name" },
  { title: "activity_count", dataIndex: "activity_count" },
  { title: "score", dataIndex: "score" },
  { title: "url", dataIndex: "url" },
  { title: "sort_idx", dataIndex: "sort_idx" },
]

function ResultOfInterviewReview() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_content/result_of_interview_review"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="컨텐츠 추천" functionName="면접후기 추천" desc={ Description }/>
      <SingleParamForm<InputModel, OutputModel>
        nCols={ 1 }
        fields={ fields }
        endpointApi={ "/api/recom_content/result_of_interview_review" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default ResultOfInterviewReview;
