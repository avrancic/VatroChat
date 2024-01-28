import { defineStore } from 'pinia';

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    authenticated: false
  }),
  getters: {
    isLoggedIn: (state) => state.authenticated,
  },
  actions: {
    setUser(token) {
      this.token = token;
      this.authenticated = true;
    },
    clearUser() {
      this.token = null;
      this.authenticated = false;
    },
  },
  persist: {
    storage: localStorage,
  },
});