/**
 * App.jsx — Root application component.
 * Wires together the upload zone, result panels, history sidebar, and header.
 */

import { useState } from 'react'
import Header from './components/ui/Header.jsx'
import Footer from './components/ui/Footer.jsx'
import UploadZone from './components/upload/UploadZone.jsx'
import ImagePreview from './components/upload/ImagePreview.jsx'
import LoadingState from './components/ui/LoadingState.jsx'
import PlantCard from './components/results/PlantCard.jsx'
import DiseaseCard from './components/results/DiseaseCard.jsx'
import HistoryPanel from './components/results/HistoryPanel.jsx'
import ErrorBanner from './components/ui/ErrorBanner.jsx'
import DemoNotice from './components/ui/DemoNotice.jsx'
import { usePrediction } from './hooks/usePrediction.js'

export default function App() {
  const {
    status, file, preview, result, error,
    history, isLoading, isSuccess, isError, hasFile,
    selectFile, predict, reset, clearHistory,
  } = usePrediction()

  const [showHistory, setShowHistory] = useState(false)

  return (
    <div className="min-h-screen bg-stone-50 bg-leaf-pattern flex flex-col">
      <Header
        historyCount={history.length}
        onToggleHistory={() => setShowHistory(v => !v)}
      />

      <main className="flex-1 container mx-auto px-4 py-8 max-w-6xl">
        <DemoNotice />

        {/* ── Hero text (only before upload) ── */}
        {!hasFile && !isSuccess && (
          <div className="text-center mb-10 animate-fade-up">
            <h1 className="text-4xl md:text-5xl font-display font-bold text-stone-800 mb-4 leading-tight">
              Diagnose Your Plants<br />
              <span className="text-leaf-600">with AI Precision</span>
            </h1>
            <p className="text-stone-500 text-lg max-w-xl mx-auto">
              Upload a leaf photo. Our two-stage deep learning pipeline identifies
              the plant species and detects any diseases — instantly.
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* ── Left / Main column ── */}
          <div className="lg:col-span-2 space-y-6">

            {/* Upload or Preview */}
            {!hasFile ? (
              <UploadZone onFileSelect={selectFile} />
            ) : (
              <ImagePreview
                preview={preview}
                fileName={file?.name}
                fileSize={file?.size}
                onReset={reset}
                onPredict={predict}
                isLoading={isLoading}
                hasResult={isSuccess}
              />
            )}

            {/* Error banner */}
            {isError && (
              <ErrorBanner message={error} onDismiss={() => reset()} />
            )}

            {/* Loading skeleton */}
            {isLoading && <LoadingState />}

            {/* Results */}
            {isSuccess && result && (
              <div className="space-y-5 animate-fade-up">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-display font-semibold text-stone-800">
                    Analysis Results
                  </h2>
                  <span className="text-xs text-stone-400 bg-stone-100 px-3 py-1 rounded-full">
                    Processed in {result.processing_time_ms}ms
                  </span>
                </div>
                <PlantCard plant={result.plant} />
                <DiseaseCard disease={result.disease} />
              </div>
            )}
          </div>

          {/* ── Right sidebar ── */}
          <div className="lg:col-span-1">
            <HistoryPanel
              history={history}
              onClear={clearHistory}
              isOpen={showHistory}
              onToggle={() => setShowHistory(v => !v)}
            />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
