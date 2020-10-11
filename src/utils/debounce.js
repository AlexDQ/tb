/**
 * @file debounce.js
 * @author cy
 * @createTime 2019-01-18 10:10:07
 * @description 防抖
 * @param {Function} func - 事件
 * @param {Number} wait - 时间间隔
 * @param {Boolean} immediate - 是否立即执行
 * @example tabClick:debounce(function (args) {},500,true)
 */
export const debounce = function (func, wait, immediate) {
  let timeout, result

  let debounced = function () {
    let args = arguments

    if (timeout) clearTimeout(timeout)
    if (immediate) {
      let callNow = !timeout
      timeout = setTimeout(() => {
        timeout = null
      }, wait)
      if (callNow) result = func.apply(this, args)
    } else {
      timeout = setTimeout(() => {
        func.apply(this, args)
      }, wait)
    }
    return result
  }

  debounced.cancel = function () {
    clearTimeout(timeout)
    timeout = null
  }

  return debounced
}
