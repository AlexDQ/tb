
import { Base64 } from 'js-base64'

/**
 * @description 后端传参 加密函数
 * @param {str} String
 */
export const compileStr = function (str) {
  if (str === null) {
    return null
  }
  return Base64.encode(str).split('').reverse().join('')
}

/**
 * @description 后端传参 解密函数
 * @param {data} Array 数据
 * @param {fields} Array 字段
 */
export const uncompileStr = function (data, fields) {
  for (let i of data.values()) {
    for (let j of fields.values()) {
      if (i[j] !== null) {
        i[j] = Base64.decode(i[j].split('').reverse().join(''))
      }
    }
  }
  return data
}
