import React, { useRef, useState } from "react";
import { Form, Button, FormProps, Row, Col, Menu, MenuProps, Empty, Divider, Table, Tooltip } from 'antd';
import { EyeFilled, EyeInvisibleOutlined, FileSearchOutlined, } from "@ant-design/icons";
import { useForm } from "antd/lib/form/Form";
import axios from "axios"

import { makeInputComponent } from "common/components";
import { FieldDesc } from "types/form";
import { ColumnsType } from "antd/es/table";
import type { TableRowSelection } from 'antd/es/table/interface';

type Props<FieldModel> = {
  inputFields: FieldDesc<FieldModel>[],
  endpointApi: string,
  style?: React.CSSProperties,
}

type ModuleState = {
  dbType?: string,
  profileType?: string,
  keyColName?: string,
  keyColValue?: string[],
  currentMenuKeys?: string[],
  currentProfileData?: { [key: string]: any }[],
  hiddenRowKeys?: React.Key[],
  visibleHiddenRows?: boolean,
}

type DataType = {
  key: React.Key,
  value: any,
}

function ItemProfileModule<FieldModel, ApiReturnModel>({ inputFields, endpointApi, style }: Props<FieldModel>) {
  const [ form ] = useForm();
  const [ moduleState, setModuleState ] = useState<ModuleState>({})
  //const keyIndex = useRef(0);

  // 입력 부분 Form
  const formFields = inputFields.map((fieldDesc, index) => {
    const nCols = 1
    const { param, label, required, message } = fieldDesc;
    return (
      <Col key={ index } span={ 24 / nCols } style={ { flexGrow: 1 } }>
        <Form.Item name={ param as string } label={ label } rules={ [ { required, message } ] }>
          { makeInputComponent(fieldDesc) }
        </Form.Item>
      </Col>
    )
  })

  // Form 제출 로직
  const submitForm: FormProps<{ dbType: string, profileType: string, keyColName: string, keyColValue: string }>["onFinish"] = (param) => {
    const {
      dbType: newDbType,
      profileType: newProfileType,
      keyColName: newKeyColName,
      keyColValue: newKeyColValue
    } = param
    const {
      dbType: oldDbType,
      profileType: oldProfileType,
      hiddenRowKeys: oldHiddenRowKeys,
      visibleHiddenRows: oldVisibleHiddenRows
    } = moduleState

    const isRenewHiddenConfig: boolean = (newDbType != oldDbType) || (newProfileType != oldProfileType)

    setModuleState({
      dbType: newDbType,
      profileType: newProfileType,
      keyColName: newKeyColName,
      keyColValue: newKeyColValue
        .split(/,|\s/)
        .map((value) => value.trim())
        .filter((value) => /^\d+$/.test(value)),
      currentProfileData: [],
      currentMenuKeys: [],
      hiddenRowKeys: isRenewHiddenConfig ? []: oldHiddenRowKeys,
      visibleHiddenRows: isRenewHiddenConfig ? false : oldVisibleHiddenRows,
    })
  }

  // Form 초기화 로직
  const clearAll = () => {
    form.resetFields()
    setModuleState({})
  }

  // 메뉴 아이템
  const menuItems: MenuProps["items"] = moduleState.keyColValue?.map((itemId, index) => ({
    key: itemId,
    label: itemId,
    icon: <FileSearchOutlined style={{ fontSize: 17 }} />,
  }))

  // 메뉴 클릭 로직
  const onMenuClick: MenuProps["onClick"] = (menuInfo) => {
    const { dbType, profileType, keyColName } = moduleState
    const data = {
      dbType,
      profileType,
      keyColName: keyColName,
      keyColValue: menuInfo.key
    }

    console.log(endpointApi, data)

    axios.post<ModuleState["currentProfileData"]>(endpointApi, data)
      .then(({ data }) => {
        setModuleState({ ...moduleState, currentMenuKeys: [ menuInfo.key ], currentProfileData: data })
      })
      .catch((reason) => alert(reason.message))
  }

  // Empty 컴포넌트 관련
  let helpMsg: string = ""
  let isEmpty: boolean = true

  if (menuItems == undefined || menuItems?.length == 0) {
    helpMsg = "프로파일 및 아이템 타입과 번호를 입력해주세요"
  } else if (moduleState.currentMenuKeys == undefined || moduleState.currentMenuKeys?.length == 0) {
    helpMsg = "상단 탭의 아이템 번호를 클릭해주세요"
  } else if (moduleState.currentProfileData == undefined || moduleState.currentProfileData?.length == 0) {
    helpMsg = "해당하는 프로파일 데이터가 존재하지 않습니다"
  } else {
    isEmpty = false;
  }

  // 테이블 Props
  const columns: ColumnsType<DataType> = [
    { title: "key", dataIndex: "key", width: "15%" },
    { title: "value", dataIndex: "value", width: "80%", ellipsis: true },
  ]
  const dataSource = moduleState.currentProfileData?.flatMap((value, i) =>
    Object.entries(value)
      .filter(([ k, v ]) => moduleState.visibleHiddenRows || !(moduleState.hiddenRowKeys || []).includes(k))
      .map<DataType>(([ k, v ], j) => ({ key: k, value: v }))
  )
  const rowSelection: TableRowSelection<DataType> = {
    selectedRowKeys: moduleState.hiddenRowKeys,
    selections: [ Table.SELECTION_ALL, Table.SELECTION_INVERT, Table.SELECTION_NONE ],
    onChange: (selectedRowKeys) => setModuleState({ ...moduleState, hiddenRowKeys: selectedRowKeys }),
  }

  return <>
    <Form form={ form } onFinish={ submitForm } style={ style }>
      <Row gutter={ [ 24, 8 ] } justify="space-between" align="middle">
        { formFields }
      </Row>
      <Row gutter={ 24 } justify="end" align="middle">
        <Col><Button type="primary" htmlType="submit" style={ { width: 100 } }>입력</Button></Col>
        <Col><Button onClick={ clearAll } style={ { width: 100 } }>초기화</Button></Col>
      </Row>
    </Form>

    <Divider/>

    <Menu
      items={ menuItems }
      mode="horizontal"
      selectedKeys={ moduleState.currentMenuKeys }
      onClick={ onMenuClick }
    />

    {
      isEmpty
      ? <Empty description={ helpMsg } style={ { margin: "50px 0" } }/>
      :
        <>
          <Row gutter={ 24 } justify="end" align="middle">
            <Col>
              { `${moduleState.dbType}.${moduleState.profileType} (${moduleState.keyColName})` }
            </Col>
            <Tooltip title={ `숨겨진 행: ${ moduleState.hiddenRowKeys?.length || 0 }` } placement="left">
              <Button
                type="link"
                size="large"
                icon={
                  moduleState.visibleHiddenRows
                    ? <EyeFilled style={ { fontSize: 25 } }/>
                    : <EyeInvisibleOutlined style={ { fontSize: 25 } }/>
                }
                style={ { borderStyle: "hidden", marginRight: 10 } }
                onClick={ () => setModuleState({ ...moduleState, visibleHiddenRows: !moduleState.visibleHiddenRows }) }
              />
            </Tooltip>
          </Row>
          <Table
            style={ { width: "100%" } }
            dataSource={ dataSource }
            columns={ columns }
            rowSelection={ moduleState.visibleHiddenRows ? rowSelection : undefined }
            pagination={ false }
          />
        </>
    }
  </>
}

export default ItemProfileModule;
