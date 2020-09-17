const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
module.exports = {
  chainWebpack: config => {
    config.resolve.symlinks(true) // 修复热更新
  },
  configureWebpack: {
    plugins: [
      new UglifyJsPlugin()
    ]
  },
  devServer: {
    '/api': {
      target: 'localhost:8080',
      changeOrigin: true

    }
  }
}
