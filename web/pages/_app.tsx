import "antd/dist/antd.css";

import type { AppProps } from 'next/app'
import Head from "next/head";
import { Provider } from "react-redux";
import { createStore } from "redux";
import rootReducer from "reducers";
import MainLayout from "layouts";

/* To. 혹시나 나중에 이거 건드리게 되는 분께
 * 미안합니다...........
 **/

const store = createStore(rootReducer)

function App({ Component, pageProps }: AppProps) {
  return (
    <Provider store={ store }>
      <Head>
        <title>ML Testboard</title>
        <meta name="description" content="Jobkorea ML Testboard"/>
        <link rel="icon" href="/icon.png"/>
      </Head>
      <MainLayout>
        {/* @ts-ignore */}
        <Component { ...pageProps }/>
      </MainLayout>
    </Provider>
  )
}

export default App
