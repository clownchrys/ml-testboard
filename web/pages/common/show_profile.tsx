import { useRouter } from "next/router";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { Divider } from "antd";

import InfoComponent from "components/InfoComponent";
import LoadingComponent from "components/LoadingComponent";
import ItemProfileModule from "components/EtcModule/ItemProfileModule";
import { actions as menuActions } from "reducers/menu";
import { FieldDesc } from "types/form";

type InputModel = { dbType: string, profileType: string, itemType: string, itemIds: string, keyColName: string, keyColValue: string }

const Description = `
  - 원픽 프로파일 조회
  .
  - onepick_ml_recruit_profile (gno)
  - onepick_ml_user_profile (jk_lastestresume_no)
`
const payload = "/common/show_item"

const fields: FieldDesc<InputModel>[] = [
  {
    param: "dbType",
    label: "DB 타입",
    required: true,
    message: "조회할 데이터베이스를 선택해주세요",
    placeholder: "",
    inputType: "Select",
    availableOpt: [
      { name: "mldata", value: "mldata" },
      { name: "mldata_dev", value: "mldata_dev" },
      { name: "mldata_staging", value: "mldata_staging" },
      { name: "mlresult", value: "mlresult" },
      { name: "mlresult_dev", value: "mlresult_dev" },
      { name: "mlresult_staging", value: "mlresult_staging" },
    ],
    inputStyle: { width: "150px" }
  },
  {
    param: "profileType",
    label: "프로파일",
    required: true,
    message: "조회할 프로파일을 선택해주세요",
    placeholder: "",
    inputType: "Select",
    availableOpt: [
      { name: "onepick_ml_recruit_profile", value: "onepick_ml_recruit_profile" },
      { name: "onepick_ml_user_profile", value: "onepick_ml_user_profile" },
    ],
    inputStyle: { width: 250 }
  },
  {
    param: "keyColName",
    label: "키 컬럼명",
    required: true,
    message: "기준 컬럼의 이름을 입력해주세요",
    placeholder: "기준 컬럼의 이름을 입력해주세요",
    inputType: "Input",
    inputStyle: { width: 250 }
  },
  {
    param: "keyColValue",
    label: "키 컬럼값",
    required: true,
    message: "기준 컬럼의 값을 입력해주세요",
    placeholder: "기준 컬럼의 값을 입력해주세요",
    inputType: "Input",
  },
]

function ShowProfile() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu(payload))
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="공통" functionName="프로파일 조회" desc={ Description }/>
      <ItemProfileModule
        inputFields={ fields }
        endpointApi="/api/common/get_profile_data"
        style={{ margin: "30px 0" }}
      />
      <Divider/>
    </>
}

export default ShowProfile;