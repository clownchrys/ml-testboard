import React from "react";
import { useDispatch } from "react-redux";
import axios from "axios";
import { Form, Button, FormProps, Row, Col } from 'antd';
import { useForm } from "antd/lib/form/Form";
import { BaseFormProps } from "types/form";
import { actions as tableActions } from "reducers/table";

type NoParamFormProps<FieldModel, ApiReturnModel> = BaseFormProps<FieldModel, ApiReturnModel> & {}

function NoParamForm<FieldModel, ApiReturnModel>({ endpointApi, style }: NoParamFormProps<FieldModel, ApiReturnModel>) {
  const [form] = useForm();
  const dispatch = useDispatch();

  const onFinish: FormProps["onFinish"] = () => {
    dispatch(tableActions.setLoading(true));
    axios.post<ApiReturnModel[]>(endpointApi)
      .then(({ data }) => (data.length !== 0) ? dispatch(tableActions.setDataSource(data)) : alert("조건에 맞는 값이 없습니다"))
      .catch(( err ) => alert(err))
      .finally(() => dispatch(tableActions.setLoading(false)));
    // console.log(param);
  }

  return (
    <Form form={ form } onFinish={ onFinish } style={ style }>
      <Row gutter={ 24 } justify="end" align="middle">
        <Col><Button type="primary" htmlType="submit" style={{ width: 100 }}>Search</Button></Col>
      </Row>
    </Form>
  )
}

export default NoParamForm;