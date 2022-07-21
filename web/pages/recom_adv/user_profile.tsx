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
  - 유저별 프로파일 정보 조회
`

const columns: ColumnType2<OutputModel>[] = [
  { title: "#", dataIndex: "rowid", width: 150 },
  { title: "m_id", dataIndex: "m_id" },
  { title: "abn_bizjobtype_name", dataIndex: "abn_bizjobtype_name" },
  { title: "job_bizjobtype_name", dataIndex: "job_bizjobtype_name" },
  { title: "jk_jobtitle_name", dataIndex: "jk_jobtitle_name" },
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
      <InfoComponent projectName="JK Adv 추천" functionName="유저 프로파일 조회" desc={ Description }/>
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
