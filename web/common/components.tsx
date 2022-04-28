import { FieldDesc } from "../types/form";
import { Input, InputNumber, Select } from "antd";
import React from "react";

export function makeInputComponent<FieldModel> (fieldDesc: FieldDesc<FieldModel>): JSX.Element {
  const { inputType, inputStyle, placeholder, selectOptions, selectDefaultValue } = fieldDesc

  switch (inputType) {
    case "Input":
      return <Input placeholder={ placeholder } style={ inputStyle }/>

    case "InputNumber":
      return <InputNumber placeholder={ placeholder } style={ inputStyle }/>

    case "Select":
      return <Select
        defaultValue={ selectDefaultValue }
        showSearch
        optionFilterProp="children"
        style={ inputStyle }
      >
        { selectOptions?.map(({ name, value }, index) =>
          <Select.Option key={ index } value={ value }>{ name }</Select.Option>
        ) }
      </Select>
  }
}
