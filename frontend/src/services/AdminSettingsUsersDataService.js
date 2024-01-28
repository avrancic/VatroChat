import http from "@/http-common";
import auth from '@/services/AuthHeaderService';

class AdminSettingsUsersDataService {
  login() {
    return http.post("/user/login", { headers: auth() });
  }
}

export default new AdminSettingsUsersDataService();