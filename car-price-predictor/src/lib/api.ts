import axios from 'axios';
import { CarData, PredictionResponse } from '@/types/car';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';

export const predictCarPrice = async (carData: CarData[]): Promise<PredictionResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, carData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error predicting car price:', error);
    throw new Error('Failed to predict car price');
  }
};

export const predictSingleCarPrice = async (carData: CarData): Promise<PredictionResponse> => {
  return predictCarPrice([carData]);
};
