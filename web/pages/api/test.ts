import type { NextApiRequest, NextApiResponse } from 'next'

const { BACKEND_URI } = process.env;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const data = [
    { id: 1, value: "a" },
    { id: 2, value: "b" },
    { id: 3, value: "c" },
  ]
  console.log(BACKEND_URI);
  res.status(200).json(data);
}
