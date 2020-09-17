// 成功的轻提示
function SuccessMessage (self, mes) {
  self.$message({
    type: 'success',
    message: mes
  })
}

// 错误的轻提示
function ErrorMessage (self, mes) {
  self.$message({
    type: 'error',
    message: mes
  })
}

// 警告的轻提示
function WarningMessage (self, mes) {
  self.$message({
    type: 'warning',
    message: mes
  })
}

// 取消的轻提示
function CancelMessage (self, mes) {
  self.$message({
    type: 'info',
    message: mes
  })
}

// 警告的弹框提示
function WarningAlert (self, mes, title) {
  return self.$confirm(mes, title, {
    cancelButtonText: '取消',
    confirmButtonText: '确定',
    // cancelButtonClass: 'cancelBtn',
    type: 'warning'
  })
}

// 错误的弹出框提示
function ErrorAlert (self, mes) {
  self.$alert(mes, 'Error', {
    confirmButtonText: 'Confirm',
    type: 'error'
  })
}

export default {
  SuccessMessage,
  ErrorMessage,
  WarningMessage,
  CancelMessage,
  WarningAlert,
  ErrorAlert
}
