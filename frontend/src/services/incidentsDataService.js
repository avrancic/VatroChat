import http from "@/http-common";

class IncidentsDataService {
  getAll() {
    return http.get("/api/incidents");
  }

  create(data) {
    return http.post("/api/incidents", data);
  }

  update(id, data) {
    return http.put(`/api/incidents/${id}`, data);
  }

  delete(id) {
    return http.delete(`/api/incidents/${id}`);
  }

  getWorkers() {
    return http.get(`/api/incidents/workers`);
  }
}

export default new IncidentsDataService();