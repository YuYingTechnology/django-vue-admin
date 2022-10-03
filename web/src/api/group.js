import request from '@/utils/request'

export function getUserGroupList(params) {
    return request({
        url: '/groups/',
        method: 'get',
        params
    })
}

export function createUserGroup(data) {
    return request({
        url: '/groups/',
        method: 'post',
        data
    })
}

export function updateUserGroup(id, data) {
    return request({
        url: '/groups/' + id + '/',
        method: 'patch',
        data
    })
}
  
export function deleteUserGroup(id) {
    return request({
        url: '/groups/' + id + '/',
        method: 'delete'
    })
}