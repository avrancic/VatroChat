<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore.js';
import AuthService from '@/services/authService.js';

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');

const handleLogin = () => {
  AuthService.login(username.value, password.value)
    .then(response => {
      authStore.setUser(response);
      router.push({ path: '/' });
    })
    .catch(e => {
      console.log(e);
    });
};
</script>

<template>
   <div class="login-container">
      <div class="login">
         <div class="hover">Prijavite se na svoj račun</div>
         <div class="body">
            <form @submit.prevent="handleLogin">
               <div class="item">
                  <label>Korisničko ime</label>
                  <input v-model="username" type="text" class="form-control rounded-left" placeholder="Username" />
               </div>
               <div class="item">
                  <label>Lozinka</label>
                  <input v-model="password" type="password" class="form-control rounded-left" placeholder="Password" />
               </div>
               <div class="item">
                  <button>Prijavi me</button>
               </div>
            </form>
         </div>
      </div>
   </div>
</template>

<style scoped>
.login-container {
   background: #f5f5f5;
   display: flex;
   justify-content: center;
   align-items: center;
   height: 100%;
   height: 100dvh;
   width: 100%;
}

.login {
   width: 420px;
   flex-direction: column;
   background-color: #fff;
   box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.2);
   margin: 0 20px;
   z-index: 99999
}

.login .hover {
   padding: 20px;
   color: #fff;
   background: #2682D3;
   text-align: center;
   font-size: 20px
}

.login .body {
   padding: 30px
}

.login button {
   border-radius: 2px;
   border: 0;
   background-color: #2682D3;
   color: #FFF;
   padding: 6px 15px;
   font-size: 18px;
   line-height: 24px;
   cursor: pointer;
   transition-property: background-color;
   transition-duration: .2s;
   transition-timing-function: linear;
   padding: 10px;
   width: 100%;
   user-select: none;
   -webkit-tap-highlight-color: transparent
}

.login button:hover {
   background-color: #2475bd;
   box-shadow: none
}

.login button:focus {
   outline: none
}

.login button:active {
   box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.4)
}

.login .item {
   margin-bottom: 1rem
}

.login .item:last-child {
   margin-bottom: 0
}

.login label {
   font-family: Arial;
   color: #3c434a;
   display: block;
   font-weight: 600;
   font-size: 14px;
   margin-bottom: 10px
}

.login input {
   display: block;
   width: 100%;
   transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
   height: 46px;
   padding: 10px 16px;
   border-radius: 2px;
   border: 1px solid #ced4da;
   font-size: inherit
}

.login input:focus {
   color: #495057;
   background-color: #fff;
   border-color: #80bdff;
   outline: 0;
   box-shadow: 0 0 0 .2rem rgba(0, 123, 255, .25);
   background: #fff;
   border: 1px solid #e0e0e0;
   -webkit-box-shadow: none;
   box-shadow: none
}

.login input::-webkit-input-placeholder {
   color: #6c757d;
   opacity: 1
}

.login input::placeholder {
   color: #6c757d;
   opacity: 1
}

input:-webkit-autofill {
   -webkit-text-fill-color: black !important;
   font-size: 16px
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
   -webkit-box-shadow: 0 0 0 30px #fff inset !important
}

@media only screen and (max-device-width : 500px) {
   body {
      align-items: start;
      margin-top: 0
   }

   .login {
      margin: 0;
      width: 100%
   }
}

@media only screen and (max-device-width : 500px) {
   .login {
      margin: 0;
      width: 100%
   }
}
</style>