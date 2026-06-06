/**
 * ErrorBanner.jsx — Dismissible error message banner.
 */

import { AlertTriangle, X } from 'lucide-react'

export function ErrorBanner({ message, onDismiss }) {
  return (
    <div className="flex items-start gap-3 bg-red-50 border border-red-200 text-red-800
                    rounded-xl px-4 py-3.5 animate-scale-in">
      <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-sm">Prediction Failed</p>
        <p className="text-xs text-red-600 mt-0.5 break-words">{message}</p>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-red-400 hover:text-red-600 transition-colors flex-shrink-0"
          aria-label="Dismiss error"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  )
}

export default ErrorBanner
