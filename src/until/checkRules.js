const rulesMessage = {
  unEmpty: 'Input cannot be empty.'
}
// 判断是否为空
function checkNull (rule, value, callback) {
  // console.log(value)
  if (value === '') {
    callback(new Error(rulesMessage.unEmpty))
  } else {
    callback()
  }
}

export {
  checkNull
}
