import { useEffect, useState } from "react";
import { Divider } from "antd";
import TableComponent from "components/OutputModule/TableComponent";
import MultiParamForm from "components/FormModule/MultiParamForm";
import InfoComponent from "components/InfoComponent";
import { useDispatch } from "react-redux";
import { actions as menuActions } from "reducers/menu";
import type { ResultByGnoInput, ResultByGnoOutput } from "models/recom_renewal/result_by_gno";
import type { Field } from "types/form";
import type { ColumnType2 } from "types/table";
import { actions as tableActions } from "../../reducers/table";
import { useRouter } from "next/router";
import LoadingComponent from "../../components/LoadingComponent";

type InputModel = ResultByGnoInput
type OutputModel = ResultByGnoOutput

const Description = `
  - 공고별 추천 공고 검증
  - 공고유사도 Threshold: 0.9
  - 추천 스코어 산술식: avg( similarity + (1 - similarity) * weight )
  `

const fields: Field<InputModel>[] = [
  {
    param: "gno",
    label: "공고 번호",
    placeholder: "공고 번호",
    required: true,
    message: "gno is required",
    inputCls: "InputNumber",
    inputStyle: { width: "200px" }
  },
  {
    param: "actvt_code",
    label: "액티비티 코드",
    placeholder: "액티비티 코드",
    required: true,
    message: "actvt_code is required",
    inputCls: "InputNumber",
    inputStyle: { width: "200px" }
  },
]

const columns: ColumnType2<OutputModel>[] = [
  { title: "rowid", dataIndex: "rowid", width: 150 },
  { title: "kind", dataIndex: "kind" },
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

function TestByGno() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_renewal/result_by_gno"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="추천 구조개선" functionName="공고별 검증" desc={ Description }/>
      <MultiParamForm<InputModel, OutputModel>
        nCols={ 2 }
        fields={ fields }
        endpointApi={ "/api/recom_renewal/result_by_gno" }
        style={{ margin: "30px 0", minWidth: "50%" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default TestByGno;
