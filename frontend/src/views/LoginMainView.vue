<template>
    <section class="ftco-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-7 col-lg-5">
            <div class="login-wrap p-4 p-md-5">
              <div class="icon d-flex align-items-center justify-content-center">
                <span class="fa fa-user-o"></span>
              </div>
              <h3 class="text-center mb-4">Sign In</h3>
              <Form class="login-form" @submit="handleLogin" :validation-schema="schema">
                <div class="form-group">
                  <Field name="username" type="text" class="form-control rounded-left" placeholder="Username" />
                  <ErrorMessage name="username" class="error-feedback" />
                </div>
                <br>
                <div class="form-group">
                  <Field name="password" type="password" class="form-control rounded-left" placeholder="Password" />
                  <ErrorMessage name="password" class="error-feedback" />
                </div>
                <br>
                <div class="form-group">
                  <button class="form-control btn btn-primary rounded submit px-3" :disabled="loading">
                    <span v-show="loading" class="spinner-border spinner-border-sm"></span>
                    <span>Login</span>
                  </button>
                </div>
                <div class="form-group">
                  <div v-if="message" class="alert alert-danger" role="alert">
                    {{ message }}
                  </div>
                </div>
              </Form>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import { Form, Field, ErrorMessage } from "vee-validate";
  import * as yup from "yup";
  
  export default {
    components: {
      Form,
      Field,
      ErrorMessage,
    },
    data() {
      const schema = yup.object().shape({
        username: yup.string().required("Username is required!"),
        password: yup.string().required("Password is required!"),
      });
  
      return {
        login: {
          email: "",
          password: ""
        },
        loading: false,
        message: "",
        schema,
      };
    },
    computed: {
      loggedIn() {
        return this.$store.state.auth.status.loggedIn;
      },
    },
    created() {
      if (this.loggedIn) {
        this.$router.push("/");
      }
    },
    methods: {
      handleLogin(user) {
        this.loading = true;
  
        this.$store.dispatch("auth/login", user).then(
          () => {
            this.$router.push("/");
          },
          (error) => {
            this.loading = false;
            this.message =
              (error.response &&
                error.response.data &&
                error.response.data.message) ||
              error.message ||
              error.toString();
          }
        );
      },
    },
  };
  </script>
  
  <style scoped>
  label {
    display: block;
    margin-top: 10px;
  }
  
  .error-feedback {
    color: red;
  }
  </style>