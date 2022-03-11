import React, { useEffect } from "react";
import { Card } from "antd";
import { useDispatch } from "react-redux";
import { actions } from "../reducers/menu";
import { useRouter } from "next/router";
import LoadingComponent from "../components/LoadingComponent";

const homeContainer: React.CSSProperties = {
  padding: "0 0.5rem",
  display: "flex",
  flexDirection: "column",
  justifyContent: "flex-start",
  alignItems: "center",
  minHeight: "50vh",
}

function Home() {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(actions.setMenu("/"))
  }, [ dispatch ])

  return (router.isFallback)
    ? <LoadingComponent desc="페이지를 생성하는 중입니다..."/>
    : <div style={ homeContainer }>
      <main style={ { display: "flex", flexDirection: "column", gap: 50 } }>
        <h1 style={ { textDecoration: "none", margin: 50, lineHeight: 1.15, fontSize: "4rem" } }>
          Welcome to <span style={ { color: "#0070f3" } }>ML Testboard</span>
        </h1>

        <div>
          <Card title="How to use" style={ { borderRadius: 10 } }>내용1</Card>
        </div>

        <div>
          <Card title="FAQ" style={ { borderRadius: 10 } }>내용2</Card>
        </div>

      </main>
    </div>
}

export function getStaticProps() {
  return { props: {} }
}

export default Home
