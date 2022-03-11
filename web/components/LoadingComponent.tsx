import { Spin } from "antd";
import React from "react";

export type LoadingComponentProps = {
  desc: string
  height?: number
  vMargin?: number
  isLoading?: boolean
}

function LoadingComponent({ desc, height, vMargin, isLoading }: LoadingComponentProps) {
  return <Spin
    tip={ desc ?? "" }
    style={ { width: "100%", height: height, margin: `${ vMargin ?? 0 }px auto` } }
    spinning={ isLoading ?? true }
  />
}

export default LoadingComponent;