import http from "@/http-common";

class IncidentsDataService {
  getAll() {
    return http.get("/api/incidents");
  }

  get(id) {
    return http.get(`/api/incidents/${id}`);
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
    return http.get(`/api/workers`);
  }

  getComments(incident_id) {
    return http.get(`/api/incidents/${incident_id}/comments`);
  }

  createComment(incident_id, data) {
    return http.post(`/api/incidents/${incident_id}/comments`, data);
  }

  updateComment(incident_id, id, data) {
    return http.put(`/api/incidents/${incident_id}/comments/${id}`, data);
  }

  deleteComment(incident_id, id) {
    return http.delete(`/api/incidents/${incident_id}/comments/${id}`);
  }
}

export default new IncidentsDataService();