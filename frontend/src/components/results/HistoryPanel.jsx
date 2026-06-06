/**
 * HistoryPanel.jsx — Sidebar showing previous predictions from this session.
 * Data is persisted to sessionStorage via usePrediction hook.
 */

import { Clock, Trash2, CheckCircle2, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react'
import clsx from 'clsx'

function formatTime(isoString) {
  const d = new Date(isoString)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function HistoryItem({ entry }) {
  return (
    <div className="flex items-center gap-3 p-3 rounded-xl border border-stone-100
                    hover:border-stone-200 hover:bg-stone-50 transition-all duration-150 group">
      {/* Thumbnail */}
      <div className="w-12 h-12 rounded-lg overflow-hidden bg-stone-100 flex-shrink-0">
        {entry.preview ? (
          <img
            src={entry.preview}
            alt={entry.plantName}
            className="w-full h-full object-cover"
            onError={e => { e.target.style.display = 'none' }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-stone-300 text-xl">🌿</div>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-1.5">
          {entry.isHealthy ? (
            <CheckCircle2 className="w-3.5 h-3.5 text-leaf-500 flex-shrink-0" />
          ) : (
            <AlertCircle className="w-3.5 h-3.5 text-orange-500 flex-shrink-0" />
          )}
          <p className="text-sm font-semibold text-stone-700 truncate">{entry.plantName}</p>
        </div>
        <p className={clsx(
          'text-xs truncate mt-0.5',
          entry.isHealthy ? 'text-leaf-500' : 'text-orange-500'
        )}>
          {entry.diseaseName}
        </p>
        <p className="text-xs text-stone-400 mt-0.5 flex items-center gap-1">
          <Clock className="w-2.5 h-2.5" />
          {formatTime(entry.timestamp)}
        </p>
      </div>
    </div>
  )
}

export default function HistoryPanel({ history, onClear, isOpen, onToggle }) {
  return (
    <div className="card h-fit">
      {/* Panel header */}
      <button
        onClick={onToggle}
        className="flex items-center justify-between w-full group"
      >
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-stone-100 flex items-center justify-center">
            <Clock className="w-4 h-4 text-stone-500" />
          </div>
          <div className="text-left">
            <p className="text-sm font-semibold text-stone-700">Recent Predictions</p>
            <p className="text-xs text-stone-400">{history.length} this session</p>
          </div>
        </div>
        {isOpen
          ? <ChevronUp className="w-4 h-4 text-stone-400" />
          : <ChevronDown className="w-4 h-4 text-stone-400" />
        }
      </button>

      {/* Collapsible body */}
      {isOpen && (
        <div className="mt-4 space-y-3 animate-fade-up">
          {history.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-3xl mb-2">🌱</p>
              <p className="text-sm text-stone-400">No predictions yet</p>
              <p className="text-xs text-stone-300 mt-1">Upload a plant image to get started</p>
            </div>
          ) : (
            <>
              <div className="space-y-2 max-h-[420px] overflow-y-auto pr-1">
                {history.map(entry => (
                  <HistoryItem key={entry.id} entry={entry} />
                ))}
              </div>

              <button
                onClick={onClear}
                className="flex items-center gap-1.5 text-xs text-stone-400 hover:text-red-500
                           transition-colors w-full justify-center pt-2 border-t border-stone-100"
              >
                <Trash2 className="w-3.5 h-3.5" />
                Clear history
              </button>
            </>
          )}
        </div>
      )}

      {/* Stats row (always visible) */}
      {history.length > 0 && (
        <div className="grid grid-cols-2 gap-2 mt-4 pt-4 border-t border-stone-100">
          <div className="bg-leaf-50 rounded-lg px-3 py-2 text-center">
            <p className="text-lg font-bold text-leaf-600">
              {history.filter(h => h.isHealthy).length}
            </p>
            <p className="text-[10px] text-leaf-500 font-medium uppercase tracking-wide">Healthy</p>
          </div>
          <div className="bg-orange-50 rounded-lg px-3 py-2 text-center">
            <p className="text-lg font-bold text-orange-500">
              {history.filter(h => !h.isHealthy).length}
            </p>
            <p className="text-[10px] text-orange-500 font-medium uppercase tracking-wide">Diseased</p>
          </div>
        </div>
      )}
    </div>
  )
}
