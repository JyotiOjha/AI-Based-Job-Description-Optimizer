import axios from "axios";

// ✅ ADD THIS
const BASE_URL = "http://127.0.0.1:8000/api/v1/jd";

export const generateJD = async (data: any) => {
  const response = await axios.post(`${BASE_URL}/generate`, data);
  return response.data;
};

export const rescoreJD = async (data: any) => {
  const response = await axios.post(`${BASE_URL}/rescore`, data);
  return response.data;
};

export const getSkillGap = async (data: any) => {
  const response = await axios.post(`${BASE_URL}/skill-gap`, data);
  return response.data;
};