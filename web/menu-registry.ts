import { MenuGroupType } from "./types/content";

const RecomRenewalMenu: MenuGroupType = {
  root: {
    path: "recom_renewal",
    name: "추천 구조개선"
  },
  children: [
    { path: "result_by_id", name: "유저별 검증" },
    { path: "result_by_gno", name: "공고별 검증" },
  ]
}

const RecomContentsMenu: MenuGroupType = {
  root: {
    path: "recom_contents",
    name: "컨텐츠 추천"
  },
  children: [
    // { path: "result_by_id", name: "유저별 검증" },
    // { path: "result_by_gno", name: "공고별 검증" },
  ]
}

export default [
  RecomRenewalMenu,
  RecomContentsMenu
]
