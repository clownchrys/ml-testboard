import axios, { AxiosRequestConfig } from "axios";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { slug } = req.query;
  const path = (slug as Array<string>).join("/");

  const config: AxiosRequestConfig = {
    method: "POST",
    url: `/${ path }`,
    baseURL: process.env.BACKEND_URI,
    data: req.body,
  }
  const data = await axios.request(config).then(resp => resp.data);
  res.status(200).json(data);
}
