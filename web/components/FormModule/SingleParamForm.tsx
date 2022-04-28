import React from "react";
import axios from "axios";
import { Form, Button, FormProps, Row, Col} from 'antd';
import { useForm } from "antd/lib/form/Form";
import { BaseFormProps, FieldDesc } from "types/form";
import { actions as tableActions } from "reducers/table";
import { useDispatch } from "react-redux";
import { makeInputComponent } from "common/components";

type SingleParamFormProps<FieldModel, ApiReturnModel> = BaseFormProps<FieldModel, ApiReturnModel> & {
  fields: FieldDesc<FieldModel>[],
  nCols: number,
}

function SingleParamForm<FieldModel, ApiReturnModel>({ nCols, fields, endpointApi, style }: SingleParamFormProps<FieldModel, ApiReturnModel>) {
  const [form] = useForm();
  const dispatch = useDispatch();

  const onFinish: FormProps["onFinish"] = (param) => {
    dispatch(tableActions.setLoading(true));
    axios.post<ApiReturnModel[]>(endpointApi, param)
      .then(({ data }) => (data.length !== 0) ? dispatch(tableActions.setDataSource(data)) : alert("조건에 맞는 값이 없습니다"))
      .catch(( err ) => alert(err))
      .finally(() => dispatch(tableActions.setLoading(false)));
    // console.log(param);
  }

  const clearAll = () => {
    form.resetFields();
    dispatch(tableActions.resetDataSource());
  }

  const formFields = fields.map((fieldDesc, index) => {
    const { param, label, required, message} = fieldDesc;
    return (
      <Col key={ index } span={ 24 / nCols } style={ { flexGrow: 1 } }>
        <Form.Item name={ param as string } label={ label } rules={ [ { required, message } ] }>
          { makeInputComponent(fieldDesc) }
        </Form.Item>
      </Col>
    );
  })

  return (
    <Form form={ form } onFinish={ onFinish } style={ style }>
      <Row gutter={ [ 24, 8 ] } justify="space-between" align="middle">
        { formFields }
      </Row>

      <Row gutter={ 24 } justify="end" align="middle">
        <Col><Button type="primary" htmlType="submit" style={{ width: 100 }}>Search</Button></Col>
        <Col><Button onClick={ clearAll } style={{ width: 100 }}>Clear</Button></Col>
      </Row>
    </Form>
  )
}

export default SingleParamForm;