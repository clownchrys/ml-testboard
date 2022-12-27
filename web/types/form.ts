import React from "react";

export type FieldDesc<Model> = {
  param: keyof Model,
  label: string,
  placeholder: string,
  required: boolean,
  message?: string,
  inputType: "Input" | "InputNumber" | "Select" | "Radio",
  inputStyle?: React.CSSProperties,
  defaultValue?: any,
  availableOpt?: { name: string, value: any }[],
}

export type BaseFormProps<FieldModel, ApiReturnModel> = {
  endpointApi: string,
  style?: React.CSSProperties
}
