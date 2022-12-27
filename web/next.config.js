/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,

  async rewrites() {
    return [
      // {
      //   source: "/:path*",
      //   destination: "http://www.jobkorea.co.kr/:path*"
      // }
    ]
  }
}
