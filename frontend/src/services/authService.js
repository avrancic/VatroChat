import http from "@/http-common";

class AuthService {
  login(username, password) {
    return http.post('api/auth/login', {
      username: username,
      password: password
    })
      .then(response => {
        return response.data;
      });
  }
  logout() {
    return http.post('api/auth/logout', {})
      .then(response => {
        return response;
      });
  }
}

export default new AuthService();
