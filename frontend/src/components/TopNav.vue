<script setup>
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();

const currentUser = authStore.getIme + " " + authStore.getPrezime;

</script>

<template>
  <nav class="navbar navbar-expand-lg bg-white navbar-light sticky-top p-0">
    <a href="/" class="navbar-brand d-flex align-items-center px-4 px-lg-5">
      <h2 class="m-0 text-primary">VatroChat</h2>
    </a>
    <button type="button" class="navbar-toggler me-4" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <div class="navbar-nav ms-auto p-4 p-lg-0">
        <router-link class="nav-item nav-link" to="/">Home</router-link>
        <router-link v-if="authStore.isAdmin" class="nav-item nav-link" to="/users">Korisnici</router-link>
        <router-link class="nav-item nav-link" to="/login" @click="authStore.clearUser">Logout</router-link>
      </div>
    </div>
  </nav>
</template>

<style>
.bg-light {
  background-color: #f0f0f0 !important;
}

.btn {
  font-weight: 500;
  transition: .5s;
}

.btn.btn-primary {
  color: #FFFFFF;
}

.btn-sm-square {
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  font-weight: normal;
}

.navbar .dropdown-toggle::after {
  border: none;
  content: "\f107";
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  vertical-align: middle;
}

.navbar-light .navbar-nav .nav-link {
  margin-right: 30px;
  padding: 25px 0;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 500;
  text-transform: uppercase;
  outline: none;
}

.navbar-light .navbar-nav .nav-link:hover,
.navbar-light .navbar-nav .nav-link.active {
  color: blue;
}

@media (max-width: 991.98px) {
  .navbar-light .navbar-nav .nav-link {
    margin-right: 0;
    padding: 10px 0;
  }

  .navbar-light .navbar-nav {
    border-top: 1px solid #EEEEEE;
  }
}

.navbar-light .navbar-brand,
.navbar-light a.btn {
  height: 75px;
}

.navbar-light .navbar-nav .nav-link {
  color: black;
  font-weight: 500;
}

.navbar-light.sticky-top {
  top: -100px;
  transition: .5s;
}

@media (min-width: 992px) {
  .navbar .nav-item .dropdown-menu {
    display: block;
    border: none;
    margin-top: 0;
    top: 150%;
    opacity: 0;
    visibility: hidden;
    transition: .5s;
  }

  .navbar .nav-item:hover .dropdown-menu {
    top: 100%;
    visibility: visible;
    transition: .5s;
    opacity: 1;
  }
}
</style>