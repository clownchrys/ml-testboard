import React from "react";
import { Input, InputNumber, Radio, Select } from "antd";
import { FieldDesc } from "types/form";

export function makeInputComponent<FieldModel> (fieldDesc: FieldDesc<FieldModel>): JSX.Element {
  const { inputType, inputStyle, placeholder, availableOpt, defaultValue } = fieldDesc

  switch (inputType) {
    case "Input":
      return <Input placeholder={ placeholder } style={ inputStyle }/>

    case "InputNumber":
      return <InputNumber placeholder={ placeholder } style={ inputStyle }/>

    case "Select":
      return <Select
        defaultValue={ defaultValue }
        showSearch
        optionFilterProp="children"
        style={ inputStyle }
      >
        { availableOpt?.map(({ name, value }, index) =>
          <Select.Option key={ index } value={ value }>{ name }</Select.Option>
        ) }
      </Select>

    case "Radio":
      return <Radio.Group
        defaultValue={ defaultValue }
        style={ inputStyle }
      >
        { availableOpt?.map(({ name, value }, index) =>
          <Radio.Button key={ index } value={ value }>{ name }</Radio.Button>
        ) }
      </Radio.Group>
  }
}
