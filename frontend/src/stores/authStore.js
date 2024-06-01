import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // State
  const ime = ref(null);
  const prezime = ref(null);
  const token = ref(null);
  const admin = ref(false);

  // Getters
  const getIme = computed(() => ime.value);
  const getPrezime = computed(() => prezime.value);
  const isLoggedIn = computed(() => token.value !== null);
  const getToken = computed(() => token.value);
  const isAdmin = computed(() => admin.value);

  // Actions
  const setUser = (data) => {
    ime.value = data.ime;
    prezime.value = data.prezime;
    token.value = data.token;
    admin.value = data.isAdmin;
  };

  const clearUser = () => {
    token.value = null;
    admin.value = false;
  };

  // Persist state (if using pinia-plugin-persist)
  return {
    ime,
    prezime,
    token,
    admin,
    getIme,
    getPrezime,
    isLoggedIn,
    getToken,
    isAdmin,
    setUser,
    clearUser,
  };
}, {
  persist: {
    storage: localStorage,
  },
});