import "antd/dist/antd.css";
import type { AppProps } from 'next/app'
import Head from "next/head";
import { Provider } from "react-redux";
import { createStore } from "redux";
import rootReducer from "reducers";
import MainLayout from "layouts";

const store = createStore(rootReducer)

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Provider store={ store }>
      <Head>
        <title>ML Testboard</title>
        <meta name="description" content="Jobkorea ML Testboard"/>
        <link rel="icon" href="/icon.png"/>
      </Head>

      <MainLayout>
        <Component {...pageProps}/>
      </MainLayout>

    </Provider>
  )
}
export default MyApp
