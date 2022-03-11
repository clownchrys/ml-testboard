import React, { PropsWithChildren, ReactNode } from "react";
import { Layout } from "antd";
import FooterLayout from "layouts/FooterLayout";
import HeaderLayout from "./HeaderLayout";

function ContentLayout({ children }: PropsWithChildren<ReactNode>) {
  return <Layout className="site-layout" style={ { height: "100vh", overflowY: "auto" } }>
    {/*<HeaderLayout/>*/}
    <Layout.Content>
      <div style={{ margin: 30 }}>
        { children }
      </div>
      <FooterLayout/>
    </Layout.Content>
  </Layout>
}

export default ContentLayout;