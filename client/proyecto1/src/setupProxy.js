const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/habitaciones',
    createProxyMiddleware({
      target: 'http://localhost:3001', // La URL de tu servidor
      changeOrigin: true,
    })
  );
};
