import http from "@/http-common";

class AuthService {
  login(user) {
    return http
      .post('http://127.0.0.1:8000/user/login', {
        username: user.username,
        password: user.password
      })
      .then(response => {
        console.log(response);
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