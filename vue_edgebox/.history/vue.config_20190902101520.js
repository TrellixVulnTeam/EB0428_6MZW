module.exports = {
  chainWebpack: config => {
      config.resolve.symlinks(true)  // 修复热更新
  }
  devServer: {
    '/api': {
        target: 'localhost:8080',
        changeOrigin: true,

    }  
  }
}
