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

export function createUser(data) {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: '/users/' + id + '/',
    method: 'patch',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: '/users/' + id + '/',
    method: 'delete'
  })
}

export function getWechatList(params) {
  return request({
    url: '/wechat/',
    method: 'get',
    params
  })
}

export function updateWechat(id, data) {
  return request({
    url: '/wechat/' + id + '/',
    method: 'patch',
    data
  })
}

export function deleteWechat(id) {
  return request({
    url: '/wechat/' + id + '/',
    method: 'delete'
  })
}

export function getFeiShuList(params) {
  return request({
    url: '/feishu/',
    method: 'get',
    params
  })
}

export function updateFeiShu(id, data) {
  return request({
    url: '/feishu/' + id + '/',
    method: 'patch',
    data
  })
}

export function deleteFeiShu(id) {
  return request({
    url: '/feishu/' + id + '/',
    method: 'delete'
  })
}

export function getDingtalkList(params) {
  return request({
    url: '/dingtalk/',
    method: 'get',
    params
  })
}

export function updateDingtalk(id, data) {
  return request({
    url: '/dingtalk/' + id + '/',
    method: 'patch',
    data
  })
}

export function deleteDingtalk(id) {
  return request({
    url: '/dingtalk/' + id + '/',
    method: 'delete'
  })
}

export function getGroupsList(params) {
  return request({
    url: '/groups/',
    method: 'get',
    params
  })
}