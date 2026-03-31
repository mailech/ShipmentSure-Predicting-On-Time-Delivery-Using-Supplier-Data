import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const predictDelivery = async (formData) => {
    try {
        const response = await axios.post(`${API_URL}/predict`, formData);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || "Error predicting delivery");
    }
};
