import type { Config } from 'next'

const config: Config = {
  reactStrictMode: true,
  images: {
    domains: ['modasr.top', 'localhost'],
  },
  i18n: {
    locales: ['en', 'fa'],
    defaultLocale: 'en',
  },
}

export default config
