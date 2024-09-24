// const isProd = process.env.NODE_ENV === 'production';
module.exports = {
  reactStrictMode: true,
  // output: 'export',
  // distDir: isProd ? 'dist' : '.next',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:3000/api/:path*',
      },
    ];
  },
};
