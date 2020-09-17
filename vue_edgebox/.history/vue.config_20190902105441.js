const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
module.exports = {
  chainWebpack: config => {
    config.resolve.symlinks(true) // 修复热更新
  },
  configureWebpack: {
    plugins: [
      new UglifyJsPlugin({
        uglifyOptions: {
          compress: {
            warnings: false,
            drop_console: true,
            drop_debugger: false,
            pure_funcs: ['console.log'] // 移除console
          }
        },
        sourceMap: false,
        parallel: true
      })
    ]
  },
  devServer: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
      pathRewrite: {
        '^/api': ''
      }
    }
  }
}
