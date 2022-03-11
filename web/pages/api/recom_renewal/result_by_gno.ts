import axios, { AxiosRequestConfig } from "axios";
import type { NextApiRequest, NextApiResponse } from "types/api";
import type { ResultByGnoInput, ResultByGnoOutput } from "models/recom_renewal/result_by_gno";

const data: ResultByGnoOutput[] = [
  {
    rowid: 1,
    kind: "UserHistory",
    gno: 37578883,
    actvt_code: "클릭",
    is_include: "O",
    dt: "2022-03-06 18:10:46.633",
    score: undefined,
    TITLE: "병원 원무행정사무원(접수 및 수납) 모집",
    BZT_1: "의료 / 서비스업",
    BZT_2: "사무·원무·코디 / 콜센터·아웃소싱·기타",
    LOCAL_1: "전북전지역",
    LOCAL_2: "전주시 덕진구 / 전주시 완산구",
    IS_PAID: "X",
    URL: "https://www.jobkorea.co.kr/Recruit/GI_Read/37578883"
  },
  {
    rowid: 2,
    kind: "Recommend",
    gno: 37105647,
    actvt_code: undefined,
    is_include: undefined,
    dt: undefined,
    score: 0.9876,
    TITLE: "[J.ESTINA]제이에스티나 주얼리 롯데백화점 창원점 정직원 채용",
    BZT_1: "생산·제조 / 영업·고객상담 / 판매·유통업",
    BZT_2: "섬유·의류·패션 / 판매·서빙·매장관리 / 백화점·유통·도소매",
    LOCAL_1: "경남전지역 / 전북전지역",
    LOCAL_2: "창원시 성산구 / 전주시 완산구",
    IS_PAID: "X",
    URL: "https://www.jobkorea.co.kr/Recruit/GI_Read/37105647"
  },
  {
    rowid: 3,
    kind: "Recommend",
    gno: 37105647,
    actvt_code: undefined,
    is_include: undefined,
    dt: undefined,
    score: 0.1,
    TITLE: "[J.ESTINA]제이에스티나 주얼리 롯데백화점 창원점 정직원 채용",
    BZT_1: "생산·제조 / 영업·고객상담 / 판매·유통업",
    BZT_2: "섬유·의류·패션 / 판매·서빙·매장관리 / 백화점·유통·도소매",
    LOCAL_1: "경남전지역 / 전북전지역",
    LOCAL_2: "창원시 성산구 / 전주시 완산구",
    IS_PAID: "X",
    URL: "https://www.jobkorea.co.kr/Recruit/GI_Read/37105647"
  }
]

type InputType = ResultByGnoInput[]
type OutputType = ResultByGnoOutput[]

export default async function handler(
  req: NextApiRequest<InputType>,
  res: NextApiResponse<OutputType>
) {
  const config: AxiosRequestConfig<InputType> = {
    method: "POST",
    url: "/recom_renewal/result_by_gno",
    baseURL: process.env.BACKEND_URI,
    data: req.body,
  }
  const data = await axios.request<OutputType>(config).then(resp => resp.data);
  res.status(200).json(data);
}
