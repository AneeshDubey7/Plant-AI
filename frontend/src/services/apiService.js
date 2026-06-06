/**
 * apiService.js — Axios-based API client for Plant Disease Prediction System.
 * Handles prediction requests, error normalization, and request cancellation.
 */

import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const MAX_FILE_MB = Number(import.meta.env.VITE_MAX_FILE_SIZE_MB || 10)

// Create axios instance with defaults
const api = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  timeout: 60_000, // 60s — model inference can be slow on CPU
})

// Response interceptor — normalize error messages
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.error ||
      error.message ||
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  }
)

/**
 * Validate image file before uploading.
 * @param {File} file
 * @returns {{ valid: boolean, error?: string }}
 */
export function validateFile(file) {
  const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']

  if (!ALLOWED_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: `Invalid file type "${file.type}". Please upload a JPEG, PNG, or WebP image.`,
    }
  }

  if (file.size > MAX_FILE_MB * 1024 * 1024) {
    return {
      valid: false,
      error: `File too large (${(file.size / 1024 / 1024).toFixed(1)} MB). Maximum allowed: ${MAX_FILE_MB} MB.`,
    }
  }

  return { valid: true }
}

/**
 * Upload an image and get plant + disease predictions.
 * @param {File} file - Image file
 * @param {AbortSignal} [signal] - Optional abort signal for cancellation
 * @returns {Promise<PredictionResponse>}
 */
export async function predictPlantDisease(file, signal) {
  const formData = new FormData()
  formData.append('file', file)

  const { data } = await api.post('/predict', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    signal,
    onUploadProgress: (e) => {
      // Optional: could emit progress events here
      const pct = Math.round((e.loaded * 100) / (e.total || 1))
      console.debug(`Upload progress: ${pct}%`)
    },
  })

  return data
}

/**
 * Fetch detailed info for a plant by name.
 * @param {string} plantName
 * @returns {Promise<PlantInfoResponse>}
 */
export async function getPlantInfo(plantName) {
  const { data } = await api.get(`/plant-info/${encodeURIComponent(plantName)}`)
  return data
}

/**
 * List all supported plant species.
 * @returns {Promise<{ count: number, plants: string[] }>}
 */
export async function listPlants() {
  const { data } = await api.get('/plants')
  return data
}

/**
 * Health check.
 * @returns {Promise<HealthResponse>}
 */
export async function healthCheck() {
  const { data } = await api.get('/health')
  return data
}

export default api
