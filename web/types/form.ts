import React from "react";

export type Field<Model> = {
  param: keyof Model,
  label: string,
  placeholder: string,
  required: boolean,
  message?: string,
  inputCls: "Input" | "InputNumber",
  inputStyle?: React.CSSProperties,
}

export type BaseFormProps<FieldModel, ApiReturnModel> = {
  endpointApi: string,
  style?: React.CSSProperties
}
