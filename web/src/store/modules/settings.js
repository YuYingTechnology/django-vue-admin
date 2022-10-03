import defaultSettings from '@/settings'

const { showSettings, fixedHeader, sidebarLogo } = defaultSettings

const state = {
  showSettings: showSettings,
  fixedHeader: fixedHeader,
  sidebarLogo: sidebarLogo,
  height: document.documentElement.clientHeight - 155,
  width: document.documentElement.clientWidth
}

const mutations = {
  CHANGE_SETTING: (state, { key, value }) => {
    // eslint-disable-next-line no-prototype-builtins
    if (state.hasOwnProperty(key)) {
      state[key] = value
    }
  },
  SET_HEIGHT: (state, { key, value }) => {
    // eslint-disable-next-line no-prototype-builtins
    if (state.hasOwnProperty(key)) {
      state[key] = value
    }
  },
  SET_HEIGHT: (state, height) => {
    state.height = height
  },
  SET_WIDTH: (state, width) => {
    state.width = width
  },
}

const actions = {
  changeSetting({ commit }, data) {
    commit('CHANGE_SETTING', data)
  },
  setHeightWidth({ commit }, clientSize){
    commit('SET_HEIGHT', clientSize['height'])
    commit('SET_WIDTH', clientSize['width'])
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

