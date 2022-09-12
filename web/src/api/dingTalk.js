import request from '@/utils/request'

export function dingTalkLogin(data) {
  return request({
    url: '/dingtalk/login/',
    method: 'post',
    data
  })
}
