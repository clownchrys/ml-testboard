import { useRouter } from "next/router";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { Divider } from "antd";

import InfoComponent from "components/InfoComponent";
import RenderItemModule from "components/EtcModule/RenderItemModule";
import LoadingComponent from "components/LoadingComponent";
import { actions as menuActions } from "reducers/menu";
import { FieldDesc } from "types/form";

type InputModel = {
  itemType: string,
  itemIds: number,
}

const Description = `
  - 공고 또는 이력서 번호를 통해 페이지 조회
  
  ** Test Ids
  gno: 40612809, 40612810, 40612811,
  rno: 20770686
`
const payload = "/common/show_item"

const fields: FieldDesc<InputModel>[] = [
  {
    param: "itemType",
    label: "아이템 타입",
    required: true,
    message: "공고 또는 이력서를 선택해주세요",
    placeholder: "",
    inputType: "Radio",
    availableOpt: [
      {name: "공고", value: "gno"},
      {name: "이력서", value: "rno"},
    ],
  },
  {
    param: "itemIds",
    label: "아이템 번호",
    required: true,
    message: "선택한 아이템의 번호를 입력해주세요",
    placeholder: "예) 100001,100002,100003 100004 100005 (콤마 또는 공백으로 분할된 숫자)",
    inputType: "Input",
  }
]

function RenderItem() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(menuActions.setMenu(payload))
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <>
      <InfoComponent projectName="공통" functionName="공고 또는 이력서 조회" desc={ Description }/>
      <RenderItemModule fields={ fields } style={{ margin: "30px 0" }}/>
      <Divider/>
    </>
}

export default RenderItem;