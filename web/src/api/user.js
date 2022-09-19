import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login/',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/info/',
    method: 'get',
    params: {}
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}


export function getUserList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}
