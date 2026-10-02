/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  images: {
    domains: ['modasr.top', 'localhost'],
  },
  allowedDevOrigins: ['3000-' + process.env.BASE44_PUBLIC_HOST_SUFFIX],
}

module.exports = config
