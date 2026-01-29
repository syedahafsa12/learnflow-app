/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  env: {
    GROQ_API_KEY: process.env.GROQ_API_KEY,
  },
}

module.exports = nextConfig
