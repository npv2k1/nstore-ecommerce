const { i18n } = require('./next-i18next.config');
/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  swcMinify: true,
  i18n,
  images: {
    domains: [
      'pickbazarlaravel.s3.ap-southeast-1.amazonaws.com',
      'lh3.googleusercontent.com',
      'firebasestorage.googleapis.com',
      'localhost',
      'server',
      '127.0.0.1',
    ],
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // hotreload for docker
  // webpackDevMiddleware: (config) => {
  //   config.watchOptions = {
  //     poll: 1000,
  //     aggregateTimeout: 300,
  //   };
  //   return config;
  // },
};

module.exports = nextConfig;
