import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  if (
    token &&
    !config.url.includes("/auth/login") &&
    !config.url.includes("/auth/register") &&
    !config.url.includes("/auth/refresh")
  ) 
    {
      config.headers.Authorization = `Bearer ${token}`;
    }
  return config;
});

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      originalRequest.url.includes("/auth/refresh/")
    ) {
      localStorage.clear();
      window.location.href = "/";
      return Promise.reject(error);
    }

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh");

        if (!refreshToken) {
          throw new Error("No refresh token");
        }

        const res = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/refresh/`,
          { refresh: refreshToken }
        );

        const newAccess = res.data.access;

        localStorage.setItem("access", newAccess);

        originalRequest.headers.Authorization =
          `Bearer ${newAccess}`;

        return api(originalRequest);

      } catch (err) {
        localStorage.clear();
        window.location.href = "/";
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);


export default api;
