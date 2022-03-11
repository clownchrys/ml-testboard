import React, { useState } from "react";
import { useRouter } from "next/router";
import Image from "next/image";
import { Menu } from "antd";
import Sider from "antd/lib/layout/Sider";
import { DesktopOutlined, FileOutlined, PieChartOutlined, PushpinOutlined, HomeOutlined, ProjectOutlined } from "@ant-design/icons";
import { SelectInfo, SelectEventHandler } from "rc-menu/lib/interface";
import { useSelector } from "react-redux";
import { RootState } from "reducers";
import menuRegistry from "menu-registry";

const getMoreItems = (n: number, start: number = 50) => {
  const items = [];
  for (let i = start; i < n + start; i++) {
    items.push(<Menu.Item key={ "****" + i } icon={ <DesktopOutlined/> }>Option { i }</Menu.Item>)
  }
  return items;
}

const sidebarStyle = (collapsed: boolean): React.CSSProperties => ({
  overflowY: "auto",
  height: "100vh",
  boxShadow: collapsed ? undefined : "rgb(10 10 10 / 10%) 5px 0px 20px 4px",
})

const logoContainerStyle: React.CSSProperties = {
  display: "flex", justifyContent: "center", alignItems: "center",
  backgroundColor: "#fff", color: "rgba(0, 0, 0, 0.9)", fontSize: "16px",
  height: 64, width: "100%", position: "sticky", top: 0, zIndex: 999
}

const logoStyle = (collapsed: boolean): React.CSSProperties => ({
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  gap: 15,
  transform: !collapsed ? "translateX(-10px)" : undefined
})

function SidebarLayout() {
  const [ collapsed, setCollapsed ] = useState<boolean>(false);
  const content = useSelector(( state: RootState ) => state.menu.page)
  const router = useRouter();

  const onCollapse = (collapsed: boolean) => setCollapsed(collapsed);
  const onSelectMenu: SelectEventHandler = async ({ key, keyPath }: SelectInfo ) => {
    console.log({ type: "select", info: { key, keyPath } });
    await router.push(key);
  }
  const onDeselectMenu: SelectEventHandler = (info) => {
    console.log({ type: "deselect", info });
  }

  const renderedContentMenus = menuRegistry.map(({ root, children }) => (
    <Menu.SubMenu key={ root.path } icon={ <ProjectOutlined/> } title={ root.name }>
      { children.map(child => <Menu.Item key={ `/${ root.path }/${ child.path }` } icon={ <PushpinOutlined/> }>{ child.name }</Menu.Item>) }
    </Menu.SubMenu>
  ))

  return (
    <Sider theme="light" width={ 300 } style={ sidebarStyle(collapsed) } collapsed={ collapsed } onCollapse={ onCollapse } collapsible>
      <div style={ logoContainerStyle }>
        <div style={ logoStyle(collapsed) }>
          <Image src="/icon.png" alt="Jobkorea Logo" width={ 40 } height={ 40 }/>
          { collapsed ? null : <>ML Testboard</> }
        </div>
      </div>

      <Menu
        mode="vertical"
        defaultSelectedKeys={ [ content ] }
        selectedKeys={[ content ]}
        onSelect={ onSelectMenu }
        onDeselect={ onDeselectMenu }
        style={{ paddingBottom: 50 }}
      >
        <Menu.Item key={ "/" } icon={ <HomeOutlined/> }>{ "Home" }</Menu.Item>

        { renderedContentMenus }

        {/*<Menu.Item key={ 3 } icon={ <FileOutlined/> }>Files</Menu.Item>*/}
        {/*<Menu.Item key={ 4 } icon={ <PieChartOutlined/> }>Option 1</Menu.Item>*/}
        {/*<Menu.Item key={ 5 } icon={ <DesktopOutlined/> }>Option 2</Menu.Item>*/}

        {/*{ getMoreItems(20) }*/}

        {/*<Menu.Item key="999" icon={ <DesktopOutlined/> }>END</Menu.Item>*/}
      </Menu>
    </Sider>
  )
}

export default SidebarLayout;