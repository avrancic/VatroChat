import http from "@/http-common";
import auth from '@/services/AuthHeaderService';

class AdminSettingsUsersDataService {
  getAll() {
    return http.get("/api/users", { headers: auth() });
  }

  create(data) {
    return http.post("/api/users", data, { headers: auth() });
  }

  update(id, data) {
    return http.put(`/api/users/${id}`, data, { headers: auth() });
  }

  delete(id) {
    return http.delete(`/api/users/${id}`, { headers: auth() });
  }
}

export default new AdminSettingsUsersDataService();