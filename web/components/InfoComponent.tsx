import React, { useState } from "react";
import { Breadcrumb, Button, Modal } from "antd";
import { InfoCircleOutlined } from "@ant-design/icons";

type Props = {
  projectName: string,
  functionName: string,
  desc: string
}

function InfoComponent({ projectName, functionName, desc }: Props) {
  const [ visible, setVisible ] = useState(false);

  const lines = desc.trim().split("\n").map((value, index) => {
    return <p key={ index } style={ { marginTop: 0, marginBottom: 0 } }>{ value.trim() }</p>;
  })

  return <div style={ { display: "flex", gap: 5, alignItems: "center" } }>
    <Breadcrumb>
      <Breadcrumb.Item>{ projectName }</Breadcrumb.Item>
      <Breadcrumb.Item>{ functionName }</Breadcrumb.Item>
    </Breadcrumb>
    <Button
      icon={ <InfoCircleOutlined/> }
      style={ { backgroundColor: "transparent", border: "none" } }
      onClick={ () => setVisible(true) }
    />
    <Modal
      title="세부사항"
      width={ "50%" }
      footer={ [] }
      onCancel={ () => setVisible(false)}
      visible={ visible }
    >
      { lines }
    </Modal>
  </div>
}

export default InfoComponent;