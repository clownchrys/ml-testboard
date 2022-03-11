import React from "react";
import { Input, InputNumber } from "antd";

export type Field<Model> = {
  param: keyof Model,
  label: string,
  placeholder: string,
  required: boolean,
  message?: string,
  inputCls: "Input" | "InputNumber",
  inputStyle?: React.CSSProperties,
}

export type FieldValue<Model> = { [k in keyof Model]: string }

export type BaseFormProps<FieldModel, ApiReturnModel> = {
  fields: Field<FieldModel>[],
  endpointApi: string,
  style?: React.CSSProperties
}
