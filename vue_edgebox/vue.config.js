const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const webpack = require('webpack')
module.exports = {
  lintOnSave: false,
  publicPath: './',
  // chainWebpack: config => {
  //   config.resolve.symlinks(true) // 修复热更新
  // },
  configureWebpack: {
    plugins: [
      new UglifyJsPlugin({
        uglifyOptions: {
          compress: {
            // warnings: false,
            drop_console: true,
            drop_debugger: false,
            pure_funcs: ['console.log'] // 移除console
          }
        },
        sourceMap: false,
        parallel: true
      }),
      // new webpack.ProvidePlugin({
      //     jQuery: 'jquery',
      //     $: 'jquery'
      // })
    ]
  },
  devServer: {
    open:true,
    disableHostCheck:true,
    proxy: {
      '/apis': {
        target: 'http://127.0.0.1:8002/',
        changeOrigin: true,
        pathRewrite: {
          // '^/apis': ''
        }
      }
    }
  }
}
