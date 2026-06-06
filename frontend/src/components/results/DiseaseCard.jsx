/**
 * DiseaseCard.jsx — Displays Stage 2 (disease detection) results.
 * Shows disease name, severity badge, confidence, causes, prevention & treatment.
 */

import { useState } from 'react'
import {
  ShieldCheck, ShieldAlert, AlertTriangle, ChevronDown, ChevronUp,
  Bug, Syringe, ShieldPlus, FlaskConical
} from 'lucide-react'
import ConfidenceBar from '../ui/ConfidenceBar.jsx'
import clsx from 'clsx'

const SEVERITY_CONFIG = {
  none:             { label: 'Healthy',       bg: 'bg-leaf-50',   border: 'border-l-leaf-400',  badge: 'bg-leaf-100 text-leaf-700 border-leaf-200',   icon: ShieldCheck,  iconColor: 'text-leaf-500' },
  mild:             { label: 'Mild',          bg: 'bg-amber-50',  border: 'border-l-amber-400', badge: 'bg-amber-100 text-amber-700 border-amber-200', icon: AlertTriangle, iconColor: 'text-amber-500' },
  'mild-moderate':  { label: 'Mild–Moderate', bg: 'bg-orange-50', border: 'border-l-orange-400',badge: 'bg-orange-100 text-orange-700 border-orange-200',icon: AlertTriangle,iconColor: 'text-orange-500' },
  moderate:         { label: 'Moderate',      bg: 'bg-orange-50', border: 'border-l-orange-500',badge: 'bg-orange-100 text-orange-700 border-orange-200',icon: ShieldAlert,  iconColor: 'text-orange-500' },
  'moderate-severe':{ label: 'Mod–Severe',    bg: 'bg-red-50',    border: 'border-l-red-400',   badge: 'bg-red-100 text-red-700 border-red-200',       icon: ShieldAlert,  iconColor: 'text-red-500' },
  severe:           { label: 'Severe',        bg: 'bg-red-50',    border: 'border-l-red-500',   badge: 'bg-red-100 text-red-700 border-red-200',       icon: ShieldAlert,  iconColor: 'text-red-600' },
  unknown:          { label: 'Unknown',       bg: 'bg-stone-50',  border: 'border-l-stone-300', badge: 'bg-stone-100 text-stone-600 border-stone-200', icon: Bug,          iconColor: 'text-stone-400' },
}

function InfoSection({ icon: Icon, iconColor, title, items, variant = 'list' }) {
  if (!items?.length) return null
  return (
    <div>
      <p className={clsx('text-xs font-semibold uppercase tracking-wide mb-2.5 flex items-center gap-1.5', iconColor)}>
        <Icon className="w-3.5 h-3.5" />
        {title}
      </p>
      <ul className="space-y-1.5">
        {items.map((item, i) => (
          <li key={i} className="flex items-start gap-2.5 text-sm text-stone-600">
            <span className={clsx('flex-shrink-0 mt-0.5 font-bold', iconColor)}>›</span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default function DiseaseCard({ disease }) {
  const [expanded, setExpanded] = useState(true)

  if (!disease) return null

  const cfg = SEVERITY_CONFIG[disease.severity] ?? SEVERITY_CONFIG.unknown
  const Icon = cfg.icon

  return (
    <div className={clsx('card border-l-4 animate-fade-up space-y-5', cfg.border)}
         style={{ animationDelay: '0.1s' }}>

      {/* ── Header ── */}
      <div className="flex items-start gap-4">
        <div className={clsx('w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0', cfg.bg)}>
          <Icon className={clsx('w-6 h-6', cfg.iconColor)} />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-xl font-display font-bold text-stone-800">
              {disease.detected ? disease.name : '✅ Healthy Plant'}
            </h3>
            <span className={clsx('text-xs font-semibold px-2.5 py-1 rounded-full border', cfg.badge)}>
              {cfg.label}
            </span>
          </div>

          {disease.pathogen && disease.pathogen !== 'None detected' && (
            <p className="text-xs text-stone-400 mt-1 flex items-center gap-1">
              <FlaskConical className="w-3 h-3" />
              {disease.pathogen}
            </p>
          )}
        </div>
      </div>

      {/* ── Confidence bar ── */}
      <ConfidenceBar
        value={disease.confidence}
        label={disease.detected ? 'Disease Confidence' : 'Healthy Confidence'}
      />

      {/* ── Description ── */}
      <p className="text-stone-600 text-sm leading-relaxed">{disease.description}</p>

      {/* ── Healthy message ── */}
      {!disease.detected && (
        <div className="flex items-center gap-3 bg-leaf-50 border border-leaf-100 rounded-xl px-4 py-3.5">
          <ShieldCheck className="w-5 h-5 text-leaf-500 flex-shrink-0" />
          <div>
            <p className="text-sm font-semibold text-leaf-700">No disease detected</p>
            <p className="text-xs text-leaf-500 mt-0.5">
              Your plant looks healthy! Keep up with regular care practices.
            </p>
          </div>
        </div>
      )}

      {/* ── Detailed sections (disease only) ── */}
      {disease.detected && (
        <>
          <button
            onClick={() => setExpanded(v => !v)}
            className="flex items-center gap-2 text-sm font-medium text-stone-500
                       hover:text-stone-700 transition-colors w-full pt-1 border-t border-stone-100"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            {expanded ? 'Hide details' : 'Show causes, prevention & treatment'}
          </button>

          {expanded && (
            <div className="space-y-5 animate-fade-up">

              {/* Causes */}
              {disease.causes?.length > 0 && (
                <div className="bg-red-50 border border-red-100 rounded-xl p-4">
                  <InfoSection
                    icon={Bug}
                    iconColor="text-red-600"
                    title="Causes"
                    items={disease.causes}
                  />
                </div>
              )}

              {/* Prevention */}
              {disease.prevention?.length > 0 && (
                <div className="bg-amber-50 border border-amber-100 rounded-xl p-4">
                  <InfoSection
                    icon={ShieldPlus}
                    iconColor="text-amber-600"
                    title="Prevention"
                    items={disease.prevention}
                  />
                </div>
              )}

              {/* Treatment */}
              {disease.treatment?.length > 0 && (
                <div className="bg-leaf-50 border border-leaf-100 rounded-xl p-4">
                  <InfoSection
                    icon={Syringe}
                    iconColor="text-leaf-600"
                    title="Treatment & Remedies"
                    items={disease.treatment}
                  />
                </div>
              )}
            </div>
          )}
        </>
      )}

      {/* ── Prevention tips even for healthy plants ── */}
      {!disease.detected && disease.prevention?.length > 0 && (
        <div className="bg-leaf-50 border border-leaf-100 rounded-xl p-4">
          <InfoSection
            icon={ShieldPlus}
            iconColor="text-leaf-600"
            title="Maintenance Tips"
            items={disease.prevention}
          />
        </div>
      )}
    </div>
  )
}
