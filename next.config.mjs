const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:7010/api/:path*'
      },
      {
        source: '/static/:path*',
        destination: 'http://localhost:7010/static/:path*'
      }
    ];
  }
};

export default nextConfig;
