import http from "@/http-common";

class AuthService {
  login(username, password) {
    return http.post('api/user/login', {
      username: username,
      password: password
    })
      .then(response => {
        return response.data;
      });
  }
  logout() {
    return http.post('api/user/logout', {})
      .then(response => {
        return response;
      });
  }
}

export default new AuthService();