import React from "react";
import { Menu } from "antd";
import { Header } from "antd/lib/layout/layout";

function HeaderLayout() {
  return <div style={{ position: "sticky", top: 0, zIndex: 999, boxShadow: "rgb(10 10 10 / 30%) 0px 5px 20px 0px" }}>
    <Header className="header">
      <div className="logo"/>
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]}>
        <Menu.Item key="1">검증하기</Menu.Item>
        <Menu.Item key="2" disabled>미구현</Menu.Item>
        <Menu.Item key="3" disabled>미구현</Menu.Item>
      </Menu>
    </Header>
  </div>
}

export default HeaderLayout;