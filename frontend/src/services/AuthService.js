import http from "@/http-common";

class AuthService {
  login(user) {
    return http
      .post('/api/auth/login', {
        username: user.username,
        password: user.password
      })
      .then(response => {
        if (response.data.token) {
          localStorage.setItem('jwl', response.data.token);
        }

        return response.data.token;
      });
  }
  logout() {
    localStorage.removeItem('jwl');
  }
}

export default new AuthService();