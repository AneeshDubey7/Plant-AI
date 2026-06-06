/**
 * PlantCard.jsx — Displays Stage 1 (species identification) results.
 * Shows plant name, scientific name, confidence, description, uses, facts, etc.
 */

import { useState } from 'react'
import { Leaf, ChevronDown, ChevronUp, MapPin, Sun, Sparkles } from 'lucide-react'
import ConfidenceBar from '../ui/ConfidenceBar.jsx'

export default function PlantCard({ plant }) {
  const [expanded, setExpanded] = useState(false)

  if (!plant) return null

  return (
    <div className="card border-l-4 border-l-leaf-400 animate-fade-up space-y-5">
      {/* Header */}
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl bg-leaf-100 flex items-center justify-center flex-shrink-0">
          <Leaf className="w-6 h-6 text-leaf-600" />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-xl font-display font-bold text-stone-800">{plant.name}</h3>
            <span className="badge-healthy">Identified</span>
          </div>
          <p className="text-stone-400 text-sm italic mt-0.5">{plant.scientific_name}</p>
          {plant.family && (
            <p className="text-xs text-stone-400 mt-0.5">Family: {plant.family}</p>
          )}
        </div>
      </div>

      {/* Confidence bar */}
      <ConfidenceBar value={plant.confidence} label="Species Confidence" />

      {/* Description */}
      <p className="text-stone-600 text-sm leading-relaxed">{plant.description}</p>

      {/* Quick facts row */}
      <div className="grid grid-cols-2 gap-3">
        <div className="flex items-center gap-2 bg-stone-50 rounded-lg px-3 py-2.5">
          <MapPin className="w-4 h-4 text-soil-500 flex-shrink-0" />
          <div>
            <p className="text-[10px] text-stone-400 uppercase tracking-wide">Origin</p>
            <p className="text-xs font-medium text-stone-700 truncate">{plant.origin}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 bg-stone-50 rounded-lg px-3 py-2.5">
          <Sun className="w-4 h-4 text-amber-500 flex-shrink-0" />
          <div>
            <p className="text-[10px] text-stone-400 uppercase tracking-wide">Season</p>
            <p className="text-xs font-medium text-stone-700 truncate">{plant.season}</p>
          </div>
        </div>
      </div>

      {/* Uses */}
      {plant.uses?.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-stone-500 uppercase tracking-wide mb-2">Uses</p>
          <ul className="space-y-1.5">
            {plant.uses.map((use, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-stone-600">
                <span className="text-leaf-400 mt-0.5 flex-shrink-0">•</span>
                {use}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Expandable: growing conditions + facts */}
      <button
        onClick={() => setExpanded(v => !v)}
        className="flex items-center gap-2 text-sm font-medium text-leaf-600 
                   hover:text-leaf-700 transition-colors w-full pt-1 border-t border-stone-100"
      >
        {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        {expanded ? 'Show less' : 'Growing conditions & interesting facts'}
      </button>

      {expanded && (
        <div className="space-y-4 animate-fade-up">
          {/* Growing conditions */}
          <div className="bg-leaf-50 border border-leaf-100 rounded-xl p-4">
            <p className="text-xs font-semibold text-leaf-700 uppercase tracking-wide mb-2">
              🌱 Growing Conditions
            </p>
            <p className="text-sm text-stone-600 leading-relaxed">{plant.growing_conditions}</p>
          </div>

          {/* Interesting facts */}
          {plant.interesting_facts?.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-stone-500 uppercase tracking-wide mb-2 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                Interesting Facts
              </p>
              <ul className="space-y-2">
                {plant.interesting_facts.map((fact, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-stone-600 
                                         bg-amber-50 border border-amber-100 rounded-lg px-3 py-2">
                    <span className="text-amber-400 flex-shrink-0 font-bold">{i + 1}.</span>
                    {fact}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
