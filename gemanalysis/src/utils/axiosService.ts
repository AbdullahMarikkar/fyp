import axios from "axios";
import { getAccessToken } from "./cookieService";
import { timeout } from "./constants";

const axiosInstance = axios.create({
  // baseURL: process.env.BACKEND_URL,
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(
  async (config) => {
    const modifiedConfig = config;
    modifiedConfig.headers.Authorization = `Bearer ${getAccessToken()}`;
    // modifiedConfig.headers.Refresh = `Refresh ${getRefreshToken()}`;
    modifiedConfig.timeout = timeout;
    modifiedConfig.withCredentials = true;
    return modifiedConfig;
  },
  async (error) => {
    return await Promise.reject(error);
  }
);

// axiosInstance.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   async (error) => {
//     const originalRequest = error.config;
//     if (error?.response?.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true;
//       const tokenResponse = await refreshAccessToken();
//       if (tokenResponse.refreshToken) {
//         setRefreshTokenToCookie(tokenResponse.refreshToken);
//       }
//       if (tokenResponse.accessToken) {
//         setAccessTokenToCookie(tokenResponse.accessToken);
//         originalRequest.headers.Authorization = `Bearer ${getAccessToken()}`;
//         return await axiosInstance(originalRequest);
//       }
//     }
//     // }else {
//     //   location.href = 'http://localhost:3000/login'
//     // }
//     return await Promise.reject(error);
//   }
// );

export default axiosInstance;
