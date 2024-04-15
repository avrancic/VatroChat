import http from "@/http-common";

class AdminSettingsEmployeesDataService {
  getAll() {
    return http.get("/api/employees");
  }

  get(id) {
    return http.get(`/api/employees/${id}`);
  }

  create(data) {
    return http.post("/api/employees", data);
  }

  update(id, data) {
    return http.put(`/api/employees/${id}`, data);
  }

  delete(id) {
    return http.delete(`/api/employees/${id}`);
  }

  deleteAll() {
    return http.delete(`/api/employees`);
  }

  getTypes() {
    return http.get(`/api/employees_types`);
  }
}

export default new AdminSettingsEmployeesDataService();
