import http from "@/http-common";

class CommentsDataService {
  getAll() {
    return http.get("/api/comments");
  }

  create(data) {
    return http.post("/api/comments", data);
  }

  update(id, data) {
    return http.put(`/api/comments/${id}`, data);
  }

  delete(id) {
    return http.delete(`/api/comments/${id}`);
  }

  getTypes() {
    return http.get(`/api/comments/types`);
  }
}

export default new CommentsDataService();