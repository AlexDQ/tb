import axios from 'axios'
import { stringify } from 'qs'

const downloadMiddleware = (url, param) => {
  let form = document.createElement('form')
  form.method = 'POST'
  form.action = url
  document.body.appendChild(form)
  for (let key in param) {
    let input = document.createElement('input')
    input.type = 'hidden'
    input.name = key
    input.value = param[key]
    form.appendChild(input)
  }
  form.submit()
  document.body.removeChild(form)
}
const downloadOption = (url, param = {}, header = { 'Content-Type': 'application/json' }) => {
  axios({
    method: "POST",
    header: header,
    url: url,
    data: param,
    responseType: 'arraybuffer'
  }).then((res) =>{
    const content = res
    // console.info(content["headers"])
    const fileName = content["headers"]["content-disposition"].substring(content["headers"]["content-disposition"].indexOf("filename")+9, content["headers"]["content-disposition"].length-1)
    // console.info(fileName)
    const blob = new Blob([content.data],{"type" : content["headers"]["content-type"]})
    const elink = document.createElement('a')
    elink.download = fileName
    elink.style.display = 'none'
    elink.href = URL.createObjectURL(blob)
    document.body.appendChild(elink)
    elink.click()
    URL.revokeObjectURL(elink.href) // 释放URL 对象
    document.body.removeChild(elink)
  })
}

const download = {
  "post":downloadMiddleware,
  "option":downloadOption
}



export default download