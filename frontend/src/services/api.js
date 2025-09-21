const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  getHeaders(includeAuth = false) {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (includeAuth) {
      const token = localStorage.getItem('access_token');
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async handleResponse(response) {
    const data = await response.json();

    if (!response.ok) {
      // Handle backend error format
      let errorMessage = 'An error occurred';

      if (data.message) {
        errorMessage = data.message;
      } else if (data.detail) {
        errorMessage = data.detail;
      }

      // Add authentication context for better error handling
      if (response.status === 401) {
        errorMessage = 'Could not validate credentials';
      }

      throw new Error(errorMessage);
    }

    // Handle backend success format
    if (data.success === false) {
      throw new Error(data.message || 'Request failed');
    }

    return data;
  }

  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(credentials),
    });

    const data = await this.handleResponse(response);
    // Extract the actual user data from the wrapped response
    return data.data || data;
  }

  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(userData),
    });

    const data = await this.handleResponse(response);
    // Extract the actual user data from the wrapped response
    return data.data || data;
  }

  async getCurrentUser() {
    const response = await fetch(`${API_BASE_URL}/user/`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    // Extract the actual user data from the wrapped response
    return data.data || data;
  }

  setAuthToken(token) {
    localStorage.setItem('access_token', token);
  }

  removeAuthToken() {
    localStorage.removeItem('access_token');
  }

  getAuthToken() {
    return localStorage.getItem('access_token');
  }

  // Topic API methods
  async getTopics() {
    const response = await fetch(`${API_BASE_URL}/topics/`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async getTopic(topicId) {
    const response = await fetch(`${API_BASE_URL}/topics/${topicId}`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async createTopic(topicData) {
    const response = await fetch(`${API_BASE_URL}/topics/`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: JSON.stringify(topicData),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async updateTopic(topicId, topicData) {
    const response = await fetch(`${API_BASE_URL}/topics/${topicId}`, {
      method: 'PATCH',
      headers: this.getHeaders(true),
      body: JSON.stringify(topicData),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async deleteTopic(topicId) {
    const response = await fetch(`${API_BASE_URL}/topics/${topicId}`, {
      method: 'DELETE',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async getTopicEdges(topicId) {
    const response = await fetch(`${API_BASE_URL}/topics/${topicId}/edges`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async createTopicEdge(sourceTopicId, targetTopicId, relationType = 'related') {
    const response = await fetch(`${API_BASE_URL}/topics/topic-edges`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: JSON.stringify({
        source: sourceTopicId,
        target: targetTopicId,
        relation_type: relationType
      }),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async deleteTopicEdge(sourceTopicId, targetTopicId) {
    const response = await fetch(`${API_BASE_URL}/topics/topic-edges/${sourceTopicId}/${targetTopicId}`, {
      method: 'DELETE',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  // Note API methods
  async getNotesByTopic(topicId) {
    const response = await fetch(`${API_BASE_URL}/notes/${topicId}`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async getNote(noteId) {
    const response = await fetch(`${API_BASE_URL}/notes/single/${noteId}`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async createNote(noteData) {
    const response = await fetch(`${API_BASE_URL}/notes/`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: JSON.stringify(noteData),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async updateNote(noteId, noteData) {
    const response = await fetch(`${API_BASE_URL}/notes/${noteId}`, {
      method: 'PATCH',
      headers: this.getHeaders(true),
      body: JSON.stringify(noteData),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async deleteNote(noteId) {
    const response = await fetch(`${API_BASE_URL}/notes/${noteId}`, {
      method: 'DELETE',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  // Tag API methods
  async getTags() {
    const response = await fetch(`${API_BASE_URL}/tags/`, {
      method: 'GET',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async createTag(tagData) {
    const response = await fetch(`${API_BASE_URL}/tags/`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: JSON.stringify(tagData),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async updateTag(tagId, tagData) {
    const response = await fetch(`${API_BASE_URL}/tags/${tagId}`, {
      method: 'PATCH',
      headers: this.getHeaders(true),
      body: JSON.stringify(tagData),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }

  async deleteTag(tagId) {
    const response = await fetch(`${API_BASE_URL}/tags/${tagId}`, {
      method: 'DELETE',
      headers: this.getHeaders(true),
    });

    const data = await this.handleResponse(response);
    return data.data || data;
  }
}

export const apiService = new ApiService();