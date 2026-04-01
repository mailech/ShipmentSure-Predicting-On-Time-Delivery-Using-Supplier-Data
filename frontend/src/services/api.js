import axios from 'axios';

// Use environment variable if deployed on Render, otherwise default to local
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const pingBackend = async () => {
    try {
        await axios.get(`${API_URL}/ping`);
        console.log("Backend is awake!");
    } catch (error) {
        // Silent fail: The initial connection might fail if the server is off, 
        // but the request itself triggers the Render container to wake up.
        console.log("Ping sent. Backend is waking up...");
    }
};

export const predictDelivery = async (formData) => {
    try {
        const response = await axios.post(`${API_URL}/predict`, formData);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || "Error predicting delivery");
    }
};
