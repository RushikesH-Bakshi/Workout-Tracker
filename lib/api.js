const request = async (path, { method = 'GET', body, ...options } = {}) => {
  const headers = { 'Content-Type': 'application/json' };
  const response = await fetch(path, {
    method,
    headers,
    credentials: 'include',
    body: body ? JSON.stringify(body) : undefined,
    ...options,
  });

  if (response.status === 204) {
    return null;
  }

  const json = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(json?.message || 'Request failed');
  }

  return json;
};

export const getProfile = () => request('/api/profile');
export const login = (body) => request('/api/login', { method: 'POST', body });
export const signup = (body) => request('/api/signin', { method: 'POST', body });
export const logout = () => request('/api/logout');
export const getWorkouts = (page = 1) => request(`/api/workouts?page=${page}`);
export const getWorkout = (id) => request(`/api/workouts/${id}`);
export const createWorkout = (body) => request('/api/workouts', { method: 'POST', body });
export const updateWorkout = (id, body) => request(`/api/workouts/${id}`, { method: 'PUT', body });
export const deleteWorkout = (id) => request(`/api/workouts/${id}`, { method: 'DELETE' });
