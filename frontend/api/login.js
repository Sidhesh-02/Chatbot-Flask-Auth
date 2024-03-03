import axios from "axios";
export const login = async (credentials) => {
    try {
      const { data } = await axios.post('http://127.0.0.1:5000/login', credentials, { withCredentials: true });
      return data;
    } catch (error) {
      throw error.response.data.msg || "An error occurred";
    }
  };