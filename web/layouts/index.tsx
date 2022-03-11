import React, { ReactNode } from "react";
import { Layout } from "antd";
import SidebarLayout from "./SidebarLayout";
import ContentLayout from "./ContentLayout";

export default function MainLayout({ children }: React.PropsWithChildren<ReactNode>) {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Layout hasSider>
        <SidebarLayout/>
        <ContentLayout>

          { children }

        </ContentLayout>
      </Layout>
    </Layout>
  )
}
