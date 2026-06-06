/**
 * ConfidenceBar.jsx — Animated horizontal confidence/progress bar.
 * Color shifts from red → yellow → green based on confidence value.
 */

import clsx from 'clsx'

function getBarColor(value) {
  if (value >= 0.80) return 'bg-leaf-500'
  if (value >= 0.60) return 'bg-amber-400'
  if (value >= 0.40) return 'bg-orange-400'
  return 'bg-red-400'
}

function getTextColor(value) {
  if (value >= 0.80) return 'text-leaf-700'
  if (value >= 0.60) return 'text-amber-700'
  if (value >= 0.40) return 'text-orange-700'
  return 'text-red-600'
}

function getLabel(value) {
  if (value >= 0.90) return 'Very High'
  if (value >= 0.75) return 'High'
  if (value >= 0.55) return 'Moderate'
  if (value >= 0.40) return 'Low'
  return 'Very Low'
}

export default function ConfidenceBar({ value, label = 'Confidence', showLabel = true }) {
  const pct = Math.round(value * 100)

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-xs">
        <span className="text-stone-500 font-medium">{label}</span>
        <span className={clsx('font-bold tabular-nums', getTextColor(value))}>
          {pct}%
          {showLabel && (
            <span className="font-normal text-stone-400 ml-1">· {getLabel(value)}</span>
          )}
        </span>
      </div>

      {/* Track */}
      <div className="h-2.5 bg-stone-100 rounded-full overflow-hidden">
        {/* Fill — width set via inline style so Tailwind JIT doesn't purge dynamic classes */}
        <div
          className={clsx('h-full rounded-full transition-all duration-700 ease-out', getBarColor(value))}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
