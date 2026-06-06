/**
 * DemoNotice.jsx — Banner shown when API is in demo/mock mode (no trained models).
 */

import { useState, useEffect } from 'react'
import { Info, X } from 'lucide-react'
import { healthCheck } from '../../services/apiService.js'

export default function DemoNotice() {
  const [isDemoMode, setIsDemoMode] = useState(false)
  const [dismissed, setDismissed] = useState(false)

  useEffect(() => {
    healthCheck()
      .then(data => setIsDemoMode(data.status === 'demo_mode'))
      .catch(() => {}) // Silently fail — user will see upload errors anyway
  }, [])

  if (!isDemoMode || dismissed) return null

  return (
    <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 text-amber-800
                    rounded-xl px-4 py-3 mb-6 animate-fade-up">
      <Info className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
      <div className="flex-1 text-sm">
        <span className="font-semibold">Demo Mode</span>
        {' '}— Trained model files not found. Predictions are realistic mock data.
        To use real models, run the ML training scripts and place{' '}
        <code className="bg-amber-100 text-amber-900 px-1 rounded text-xs">
          *.onnx
        </code>{' '}
        files in <code className="bg-amber-100 text-amber-900 px-1 rounded text-xs">backend/models/</code>.
      </div>
      <button onClick={() => setDismissed(true)} className="text-amber-400 hover:text-amber-600 flex-shrink-0">
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}
