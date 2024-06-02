import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // State
  const name = ref(null);
  const surname = ref(null);
  const is_admin = ref(false);
  const token = ref(null);

  // Getters
  const getName = computed(() => name.value);
  const getSurname = computed(() => surname.value);
  const isLoggedIn = computed(() => token.value !== null);
  const getToken = computed(() => token.value);
  const isAdmin = computed(() => is_admin.value);

  // Actions
  const setUser = (data) => {
    name.value = data.name;
    surname.value = data.surname;
    is_admin.value = data.is_admin;
    token.value = data.token;
  };

  const clearUser = () => {
    is_admin.value = false;
    token.value = null;
  };

  // Persist state (if using pinia-plugin-persist)
  return {
    name,
    surname,
    is_admin,
    token,
    getName,
    getSurname,
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