/**
 * LoadingState.jsx — Animated skeleton shown during model inference.
 * Two skeleton cards mirror the real PlantCard and DiseaseCard layout.
 */

import { Loader2 } from 'lucide-react'

function SkeletonLine({ w = 'w-full', h = 'h-4' }) {
  return <div className={`${w} ${h} rounded-lg shimmer`} />
}

function SkeletonCard({ title, rows = 4 }) {
  return (
    <div className="card animate-pulse">
      {/* Card header */}
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 rounded-xl shimmer" />
        <div className="space-y-2 flex-1">
          <SkeletonLine w="w-1/3" h="h-5" />
          <SkeletonLine w="w-1/2" h="h-3" />
        </div>
        <SkeletonLine w="w-16" h="h-7" />
      </div>
      {/* Progress bar placeholder */}
      <div className="mb-5">
        <div className="flex justify-between mb-1.5">
          <SkeletonLine w="w-20" h="h-3" />
          <SkeletonLine w="w-8" h="h-3" />
        </div>
        <div className="h-2.5 w-full rounded-full shimmer" />
      </div>
      {/* Body rows */}
      <div className="space-y-2.5">
        {Array.from({ length: rows }).map((_, i) => (
          <SkeletonLine key={i} w={i % 3 === 0 ? 'w-4/5' : 'w-full'} />
        ))}
      </div>
    </div>
  )
}

export default function LoadingState() {
  return (
    <div className="space-y-5">
      {/* Status indicator */}
      <div className="flex items-center gap-3 text-leaf-700 bg-leaf-50 border border-leaf-100 
                      rounded-xl px-4 py-3 animate-fade-up">
        <Loader2 className="w-5 h-5 animate-spin text-leaf-500" />
        <div>
          <p className="font-semibold text-sm">Analysing your plant…</p>
          <p className="text-xs text-leaf-500 mt-0.5">
            Running two-stage deep learning pipeline · Please wait
          </p>
        </div>
      </div>

      {/* Stage indicators */}
      <div className="grid grid-cols-2 gap-3 animate-fade-up" style={{ animationDelay: '0.1s' }}>
        {['🌿 Stage 1 — Species ID', '🔬 Stage 2 — Disease Detection'].map((label, i) => (
          <div key={i} className="flex items-center gap-2.5 bg-white border border-stone-100 
                                  rounded-xl px-4 py-3 shadow-sm">
            <div className="w-2 h-2 rounded-full bg-leaf-400 animate-pulse" />
            <span className="text-xs font-medium text-stone-600">{label}</span>
          </div>
        ))}
      </div>

      {/* Skeleton cards */}
      <SkeletonCard title="Plant Information" rows={4} />
      <SkeletonCard title="Disease Analysis" rows={5} />
    </div>
  )
}
