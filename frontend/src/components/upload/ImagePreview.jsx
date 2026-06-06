/**
 * ImagePreview.jsx — Shows the selected image with file info, 
 * Analyse button, and option to reset/choose another file.
 */

import { RotateCcw, Scan, CheckCircle2, FileImage } from 'lucide-react'
import clsx from 'clsx'

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

export default function ImagePreview({
  preview, fileName, fileSize,
  onReset, onPredict, isLoading, hasResult,
}) {
  return (
    <div className="card animate-scale-in space-y-4">
      {/* Image display */}
      <div className="relative rounded-xl overflow-hidden bg-stone-100 aspect-video flex items-center justify-center">
        <img
          src={preview}
          alt="Uploaded plant"
          className="max-h-72 max-w-full object-contain"
        />
        {hasResult && (
          <div className="absolute top-3 right-3 flex items-center gap-1.5 bg-leaf-600/90 
                          text-white text-xs font-semibold px-2.5 py-1.5 rounded-full backdrop-blur-sm">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Analysed
          </div>
        )}
      </div>

      {/* File metadata */}
      <div className="flex items-center gap-2.5 text-sm text-stone-500 bg-stone-50 
                      rounded-lg px-3 py-2.5 border border-stone-100">
        <FileImage className="w-4 h-4 text-stone-400 flex-shrink-0" />
        <span className="truncate font-medium text-stone-700">{fileName}</span>
        {fileSize && (
          <span className="ml-auto flex-shrink-0 text-xs text-stone-400">
            {formatBytes(fileSize)}
          </span>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex gap-3">
        <button
          onClick={onReset}
          disabled={isLoading}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-stone-200
                     text-stone-600 hover:text-stone-900 hover:border-stone-300 hover:bg-stone-50
                     text-sm font-medium transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <RotateCcw className="w-4 h-4" />
          Change Image
        </button>

        <button
          onClick={onPredict}
          disabled={isLoading}
          className={clsx(
            'flex-1 flex items-center justify-center gap-2.5 px-6 py-2.5 rounded-xl',
            'font-semibold text-sm transition-all duration-200',
            isLoading
              ? 'bg-leaf-400 text-white cursor-not-allowed'
              : 'bg-leaf-600 hover:bg-leaf-700 text-white shadow-md hover:shadow-lg active:scale-95'
          )}
        >
          {isLoading ? (
            <>
              <span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
              Analysing…
            </>
          ) : (
            <>
              <Scan className="w-4 h-4" />
              {hasResult ? 'Re-Analyse' : 'Analyse Plant'}
            </>
          )}
        </button>
      </div>
    </div>
  )
}
