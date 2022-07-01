import { MenuGroupType } from "./types/content";

const RecomRenewalMenu: MenuGroupType = {
  root: {
    path: "recom_renewal",
    name: "추천 구조개선"
  },
  children: [
    { path: "result_by_id", name: "유저별 검증" },
    { path: "result_by_gno", name: "공고별 검증" },
    { path: "get_users", name: "유저 목록 조회" },
    { path: "monitor_model_by_bz", name: "모델 결과 조회" },
    { path: "monitor_result_by_bz", name: "추천 결과 조회" },
  ]
}

const RecomContentMenu: MenuGroupType = {
  root: {
    path: "recom_content",
    name: "컨텐츠 추천"
  },
  children: [
    { path: "get_active_users", name: "Active 유저 조회" },
    { path: "get_passive_users", name: "Passive 유저 조회" },
    { path: "result_of_interview_review", name: "면접후기 추천" },
    { path: "result_of_job_interview", name: "직무 인터뷰 추천" },
    { path: "result_of_job_news", name: "취업뉴스 추천" },
    { path: "result_of_job_talk", name: "취업톡톡 추천" },
    { path: "result_of_passletter", name: "합격 자소서 추천" },
  ]
}

const RecomAdvMenu: MenuGroupType = {
  root: {
    path: "recom_adv",
    name: "JK Adv 추천"
  },
  children: [
    { path: "user_profile", name: "유저 프로파일 조회" },
    { path: "result_by_user_story", name: "유저별 스토리 결과 조회" },
  ]
}

const RecomAmAdvMenu: MenuGroupType = {
  root: {
    path: "recom_am_adv",
    name: "AM Adv 추천"
  },
  children: [
    { path: "user_profile", name: "유저 프로파일 조회" },
    { path: "result_by_user_story", name: "유저별 스토리 결과 조회" },
  ]
}

export default [
  RecomRenewalMenu,
  RecomContentMenu,
  RecomAdvMenu,
  RecomAmAdvMenu,
]
