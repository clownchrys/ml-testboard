import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { Divider } from "antd";
import InfoComponent from "components/InfoComponent";
import NoParamForm from "components/FormModule/NoParamForm";
import TableComponent from "components/OutputModule/TableComponent";
import LoadingComponent from "components/LoadingComponent";
import { actions as menuActions } from "reducers/menu";
import { actions as tableActions } from "reducers/table";
import type { ColumnType2 } from "types/table";
import type { UserProfile } from "models/recom_adv/user_profile";

type OutputModel = UserProfile

const Description = `
  - 유저별 가능한 스토리 번호 및 속성 조회
`

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid", width: 150 },
  { title: "m_id", dataIndex: "m_id" },
  { title: "story_number", dataIndex: "story_number" },
  { title: "jk_latestjobtitle_code", dataIndex: "jk_latestjobtitle_code" },
  { title: "jk_jobtitle_code", dataIndex: "jk_jobtitle_code" },
]

function UserProfile() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu("/recom_adv/user_profile"))
    dispatch(tableActions.resetDataSource())
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="Adv 추천" functionName="유저 프로파일 조회" desc={ Description }/>
      <NoParamForm
        endpointApi={ "/api/recom_adv/result_user_profile" }
        style={{ margin: "30px 0" }}
      />
      <Divider/>
      <TableComponent<OutputModel> columns={ columns }/>
    </>
}

export function getStaticProps() {
  return { props: {} }
}

export default UserProfile;
