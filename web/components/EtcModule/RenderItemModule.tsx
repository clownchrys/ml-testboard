import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Form, Button, FormProps, Row, Col, Menu, MenuProps, Empty, Divider } from 'antd';
import { useForm } from "antd/lib/form/Form";
import { FileSearchOutlined } from "@ant-design/icons";

import { RootState } from "reducers";
import { actions as renderActions } from "reducers/render";
import { makeInputComponent } from "common/components";
import { FieldDesc } from "types/form";

type RenderItemModuleProps<FieldModel> = {
  fields: FieldDesc<FieldModel>[],
  style?: React.CSSProperties,
}

function RenderItemModule<FieldModel, ApiReturnModel>({ fields, style }: RenderItemModuleProps<FieldModel>) {
  const [form] = useForm();
  const dispatch = useDispatch();
  const renderState = useSelector(( state: RootState ) => state.render)

  const nCols = 1
  const { itemType, currentItemIds, itemIds, renderUrl } = renderState

  const formFields = fields.map((fieldDesc, index) => {
    const { param, label, required, message } = fieldDesc;
    return (
      <Col key={ index } span={ 24 / nCols } style={ { flexGrow: 1 } }>
        <Form.Item name={ param as string } label={ label } rules={ [ { required, message } ] }>
          { makeInputComponent(fieldDesc) }
        </Form.Item>
      </Col>
    )
  })

  const onFinish: FormProps<{itemType: string, itemIds: string}>["onFinish"] = (param) => {
    dispatch(renderActions.setState({
      renderUrl: undefined,
      currentItemIds: undefined,
      itemType: param.itemType,
      itemIds: param.itemIds
        .split(",")
        .map((value) => value.trim())
        .filter((value) => /^\d+$/.test(value))
    }))
  }

  const clearAll = () => {
    form.resetFields()
    dispatch(renderActions.initState())
  }

  const items: MenuProps['items'] = itemIds?.map((itemId) => ({
    key: itemId,
    label: itemId,
    // style: { paddingLeft: 20, paddingRight: 30 },
    icon: <FileSearchOutlined style={{ fontSize: 17 }} />,
  }))
  const helpMsg = ( items?.length == undefined || items?.length == 0 )
    ? "아이템 타입과 번호를 입력해주세요"
    : "상단 탭의 아이템 번호를 클릭해주세요"

  let url;
  // let itemTypeName = "없음";
  const onClick: MenuProps["onClick"] = (menuInfo) => {
    switch (itemType) {
      case "gno":
        // itemTypeName = "공고";
        url = `https://www.jobkorea.co.kr/Recruit/GI_Read/${menuInfo.key}`; break;
      case "rno":
        // itemTypeName = "이력서";
        // url = `https://www.jobkorea.co.kr/Corp/Person/Find/Resume/View?type=c&rNo=${menuInfo.key}`; break;
        url = `https://stg3-www.jobkorea.co.kr/Corp/Person/Find/Resume/View?rNo=${menuInfo.key}`; break;
      default:
        // itemTypeName = "없음";
        alert("Invalid itemType assigned"); return;
    }
    dispatch(renderActions.setState({
      renderUrl: url,
      currentItemIds: [ menuInfo.key ]
    }))
    // window.open(url, "_blank", "location=0,toolbar=0,menubar=0")
  }

  return <>

    <Form form={ form } onFinish={ onFinish } style={ style }>
      <Row gutter={ [ 24, 8 ] } justify="space-between" align="middle">
        { formFields }
      </Row>
      <Row gutter={ 24 } justify="end" align="middle">
        <Col><Button type="primary" htmlType="submit" style={{ width: 100 }}>입력</Button></Col>
        <Col><Button onClick={ clearAll } style={{ width: 100 }}>초기화</Button></Col>
      </Row>
    </Form>
    <Divider/>

    <Menu
      onClick={onClick}
      selectedKeys={currentItemIds}
      mode="horizontal"
      items={items}
    />

    {/*<Empty description={helpMsg} style={{ margin: "50px 0" }}/>*/}

    {
      (renderUrl == undefined)
        ? <Empty description={helpMsg} style={{ margin: "50px 0" }}/>
        : <>
          {
            (itemType == "gno") &&
              <iframe src={renderUrl} style={{ width: "100%", height: "100vh", border: "none" }} />
          }
          {
            (itemType == "rno") &&
              <Empty
                  description={"이력서는 인라인으로 열 수 없습니다 (issue: CORS)"}
                  style={{ margin: "50px 0" }}
              >
                  <Button
                      type="primary"
                      size="large"
                      onClick={ () => window.open(renderUrl, "_blank", "location=0,toolbar=0,menubar=0") }
                      style={{ marginTop: 20 }}
                  >
                      새 창으로 열기
                  </Button>
              </Empty>
          }
        </>

    }
    </>
}

export default RenderItemModule;
