import { defineStore } from 'pinia';

export const useAuthStore = defineStore("auth", {
  state: () => ({
    ime: null,
    prezime: null,
    token: null,
    admin: false
  }),
  getters: {
    getIme: (state) => state.ime,
    getPrezime: (state) => state.prezime,
    isLoggedIn: (state) => state.token != null,
    getToken: (state) => state.token,
    isAdmin: (state) => state.admin
  },
  actions: {
    setUser(data) {
      this.ime = data.ime;
      this.prezime = data.prezime;
      this.token = data.token;
      this.admin = data.isAdmin;
    },
    clearUser() {
      this.token = null;
      this.admin = false;
    },
  },
  persist: {
    storage: localStorage,
  },
});