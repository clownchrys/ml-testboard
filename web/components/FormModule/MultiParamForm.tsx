import React from 'react';
import axios from "axios";
import { Form, Input, Button, Space, FormProps, Row, Col, InputNumber } from 'antd';
import { useForm } from "antd/lib/form/Form";
import { MinusCircleOutlined, PlusOutlined} from '@ant-design/icons';
import type { FormListProps } from "antd/lib/form/FormList";
import type { BaseFormProps, FieldDesc } from "types/form";
import { useDispatch } from "react-redux";
import { actions as tableActions } from "reducers/table";
import { makeInputComponent } from "../../common/components";

type MultiParamFormProps<FieldModel, ApiReturnModel> = BaseFormProps<FieldModel, ApiReturnModel> & {
  fields: FieldDesc<FieldModel>[],
  nCols: number,
}

function MultiParamForm<FieldModel, ApiReturnModel>({ nCols, fields, endpointApi, style }: MultiParamFormProps<FieldModel, ApiReturnModel>) {
  const [form] = useForm();
  const dispatch = useDispatch();

  const onFinish: FormProps["onFinish"] = ({ items }) => {
    dispatch(tableActions.setLoading(true));
    axios.post<ApiReturnModel[]>(endpointApi, items)
      .then(({ data }) => (data.length !== 0) ? dispatch(tableActions.setDataSource(data)) : alert("조건에 맞는 값이 없습니다"))
      .catch((err) => alert(err))
      .finally(() => dispatch(tableActions.setLoading(false)));
    // console.log(items);
  }

  const clearAll = () => {
    form.resetFields();
    dispatch(tableActions.resetDataSource());
  }

  const renderItem = (name: number) =>
    fields.map((fieldDesc, index) => {
      const { param, label, message, required } = fieldDesc;
      return (
        <Col key={ index } span={ 24 / nCols }>
          <Form.Item key={ index } name={ [ name, param as string ] } label={ label } rules={ [ { required, message } ] }>
            { makeInputComponent(fieldDesc) }
          </Form.Item>
        </Col>
      );
    })

  const renderItemList: FormListProps["children"] = (formList, { add, remove }) => (
    <div style={ { width: "fit-content", margin: "auto" } }>
      {
        formList.map(({ key, name, ...restField }) => (
          <div key={ key } style={{ display: "flex", flexDirection: "row", alignItems: "baseline", gap: 30 }}>
            <Row gutter={ [ 24, 8 ] } justify="space-between" align="middle">
              { renderItem(name) }
            </Row>
            <Space align="baseline">
              <Button danger type="primary" size="small" icon={<MinusCircleOutlined style={ { color: "white" } } onClick={ () => remove(name) }/>}/>
            </Space>
          </div>
        ))
      }
      <Form.Item style={{ padding: "4px 50px" }}>
        <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
          Add Item
        </Button>
      </Form.Item>
    </div>
  )

  return (
    <Form form={ form } onFinish={ onFinish } style={ style }>
      <Form.List name="items">
        { renderItemList }
      </Form.List>

      <Row gutter={ 24 } justify="end" align="middle">
        <Col><Button type="primary" htmlType="submit" style={{ width: 100 }}>Search</Button></Col>
        <Col><Button onClick={ clearAll } style={{ width: 100 }}>Clear</Button></Col>
      </Row>
    </Form>
  )
}

export default MultiParamForm;