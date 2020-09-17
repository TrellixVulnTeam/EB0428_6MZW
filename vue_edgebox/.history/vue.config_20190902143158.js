const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const Autoprefixer = require('autoprefixer')
const Pxtorem = require('postcss-pxtorem')
module.exports = {
  chainWebpack: config => {
    config.resolve.symlinks(true) // 修复热更新
  },
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
      })
    ]
  },
  // css: {
  //   loaderOptions: {
  //     postcss: {
  //       plugins: [
  //         new Autoprefixer({
  //           overrideBrowserslist: ['Android >= 4.0', 'iOS >= 7']
  //         }),
  //         new Pxtorem({
  //           rootValue: 37.5,
  //           propList: ['*']
  //         })
  //       ]
  //     }
  //   }
  // },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.42.244:8080',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  }
}
