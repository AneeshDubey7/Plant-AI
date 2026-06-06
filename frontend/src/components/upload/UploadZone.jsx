/**
 * UploadZone.jsx — Drag-and-drop / click-to-browse image upload area.
 * Uses react-dropzone under the hood.
 */

import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, ImagePlus, Leaf } from 'lucide-react'
import clsx from 'clsx'

const ACCEPT = { 'image/jpeg': ['.jpg', '.jpeg'], 'image/png': ['.png'], 'image/webp': ['.webp'] }
const MAX_SIZE = 10 * 1024 * 1024   // 10 MB

const EXAMPLE_PLANTS = ['Tomato leaf', 'Apple leaf', 'Potato leaf', 'Corn leaf', 'Grape vine']

export default function UploadZone({ onFileSelect }) {
  const onDrop = useCallback((accepted) => {
    if (accepted.length > 0) onFileSelect(accepted[0])
  }, [onFileSelect])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: ACCEPT,
    maxSize: MAX_SIZE,
    maxFiles: 1,
    multiple: false,
  })

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        {...getRootProps()}
        className={clsx(
          'relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer',
          'transition-all duration-300 ease-in-out group',
          isDragActive && !isDragReject
            ? 'border-leaf-400 bg-leaf-50 scale-[1.01]'
            : isDragReject
            ? 'border-red-400 bg-red-50'
            : 'border-stone-200 bg-white hover:border-leaf-300 hover:bg-leaf-50/50'
        )}
      >
        <input {...getInputProps()} />

        {/* Animated icon */}
        <div className={clsx(
          'w-20 h-20 mx-auto mb-5 rounded-2xl flex items-center justify-center transition-all duration-300',
          isDragActive && !isDragReject
            ? 'bg-leaf-100 scale-110'
            : isDragReject
            ? 'bg-red-100'
            : 'bg-stone-100 group-hover:bg-leaf-100 group-hover:scale-105'
        )}>
          {isDragActive && !isDragReject ? (
            <Leaf className="w-10 h-10 text-leaf-500 animate-leaf-sway" />
          ) : isDragReject ? (
            <Upload className="w-10 h-10 text-red-400" />
          ) : (
            <ImagePlus className="w-10 h-10 text-stone-400 group-hover:text-leaf-500 transition-colors" />
          )}
        </div>

        {/* Text */}
        {isDragActive && !isDragReject ? (
          <div>
            <p className="text-leaf-700 font-semibold text-lg">Drop it here!</p>
            <p className="text-leaf-500 text-sm mt-1">Release to analyse your plant</p>
          </div>
        ) : isDragReject ? (
          <div>
            <p className="text-red-600 font-semibold">Invalid file</p>
            <p className="text-red-400 text-sm mt-1">Please use JPEG, PNG, or WebP under 10 MB</p>
          </div>
        ) : (
          <div>
            <p className="text-stone-700 font-semibold text-lg">
              Drop your plant image here
            </p>
            <p className="text-stone-400 text-sm mt-1.5">
              or <span className="text-leaf-600 underline underline-offset-2">click to browse</span>
            </p>
            <p className="text-stone-300 text-xs mt-3">
              JPEG · PNG · WebP &nbsp;·&nbsp; Max 10 MB
            </p>
          </div>
        )}

        {/* Decorative corner leaves */}
        <span className="absolute top-3 left-3 text-stone-200 text-xl select-none">🌿</span>
        <span className="absolute bottom-3 right-3 text-stone-200 text-xl select-none">🍃</span>
      </div>

      {/* Example chips */}
      <div className="flex flex-wrap gap-2 justify-center">
        <span className="text-xs text-stone-400 self-center">Try with:</span>
        {EXAMPLE_PLANTS.map(plant => (
          <span
            key={plant}
            className="text-xs bg-white border border-stone-200 text-stone-500
                       px-3 py-1.5 rounded-full hover:border-leaf-300 hover:text-leaf-600
                       transition-colors cursor-default"
          >
            {plant}
          </span>
        ))}
      </div>
    </div>
  )
}
