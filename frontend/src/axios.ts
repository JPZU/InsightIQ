import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:8000/api", 
});

instance.interceptors.request.use((config) => {
  const userLang = localStorage.getItem("userLang") || "en";
  config.headers["Accept-Language"] = userLang;
  return config;
});

export default instance;
