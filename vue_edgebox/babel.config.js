const plugins = [];
if (['production', 'prod'].includes(process.env.NODE_ENV)) {
 plugins.push("transform-remove-console")
}
module.exports = {
  presets: [
    '@vue/app'
  ],
  plugins: plugins,
  sourceType: 'unambiguous' //解决新的webpack无法同时使用import和module.exports问题
}