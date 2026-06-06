/**
 * usePrediction.js — Custom React hook that manages the full prediction workflow.
 * Handles file selection, upload, inference, history, and error states.
 */

import { useState, useCallback, useRef } from 'react'
import { predictPlantDisease, validateFile } from '../services/apiService'

const MAX_HISTORY = 10

export function usePrediction() {
  const [state, setState] = useState({
    status: 'idle',        // idle | loading | success | error
    file: null,            // File object
    preview: null,         // Object URL for display
    result: null,          // PredictionResponse from API
    error: null,           // Error message string
    uploadProgress: 0,
  })

  const [history, setHistory] = useState(() => {
    try {
      return JSON.parse(sessionStorage.getItem('predictionHistory') || '[]')
    } catch {
      return []
    }
  })

  const abortRef = useRef(null)

  // ── File selection ─────────────────────────────────────────────────────────
  const selectFile = useCallback((file) => {
    // Clean up previous preview URL
    if (state.preview) URL.revokeObjectURL(state.preview)

    const validation = validateFile(file)
    if (!validation.valid) {
      setState(s => ({ ...s, status: 'error', error: validation.error }))
      return false
    }

    const preview = URL.createObjectURL(file)
    setState({
      status: 'idle',
      file,
      preview,
      result: null,
      error: null,
      uploadProgress: 0,
    })
    return true
  }, [state.preview])

  // ── Submit prediction ──────────────────────────────────────────────────────
  const predict = useCallback(async () => {
    if (!state.file) return

    // Cancel any in-flight request
    abortRef.current?.abort()
    abortRef.current = new AbortController()

    setState(s => ({ ...s, status: 'loading', error: null }))

    try {
      const result = await predictPlantDisease(state.file, abortRef.current.signal)

      setState(s => ({ ...s, status: 'success', result }))

      // Save to history
      const entry = {
        id: result.image_id,
        timestamp: new Date().toISOString(),
        preview: state.preview,
        fileName: state.file.name,
        plantName: result.plant.name,
        diseaseName: result.disease.name,
        isHealthy: !result.disease.detected,
      }

      setHistory(prev => {
        const updated = [entry, ...prev].slice(0, MAX_HISTORY)
        try { sessionStorage.setItem('predictionHistory', JSON.stringify(updated)) } catch {}
        return updated
      })

    } catch (err) {
      if (err.name === 'AbortError' || err.name === 'CanceledError') return
      setState(s => ({ ...s, status: 'error', error: err.message }))
    }
  }, [state.file, state.preview])

  // ── Reset ──────────────────────────────────────────────────────────────────
  const reset = useCallback(() => {
    abortRef.current?.abort()
    if (state.preview) URL.revokeObjectURL(state.preview)
    setState({ status: 'idle', file: null, preview: null, result: null, error: null, uploadProgress: 0 })
  }, [state.preview])

  const clearHistory = useCallback(() => {
    setHistory([])
    sessionStorage.removeItem('predictionHistory')
  }, [])

  return {
    ...state,
    history,
    selectFile,
    predict,
    reset,
    clearHistory,
    isLoading: state.status === 'loading',
    isSuccess: state.status === 'success',
    isError: state.status === 'error',
    hasFile: Boolean(state.file),
  }
}
