/**
 * Header.jsx — Top navigation bar with logo, tagline, and history toggle.
 */

import { Leaf, History } from 'lucide-react'

export default function Header({ historyCount, onToggleHistory }) {
  return (
    <header className="bg-white border-b border-stone-100 shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 max-w-6xl h-16 flex items-center justify-between">

        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 bg-leaf-600 rounded-xl flex items-center justify-center shadow-sm">
            <Leaf className="w-5 h-5 text-white" strokeWidth={2.5} />
          </div>
          <div>
            <span className="font-display font-bold text-stone-800 text-lg leading-none">PlantAI</span>
            <p className="text-xs text-stone-400 leading-none mt-0.5">Disease Detection</p>
          </div>
        </div>

        {/* Nav */}
        <nav className="hidden md:flex items-center gap-6 text-sm text-stone-500">
          <a href="#" className="hover:text-leaf-600 transition-colors">How it works</a>
          <a href="#" className="hover:text-leaf-600 transition-colors">Supported Plants</a>
          <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer"
             className="hover:text-leaf-600 transition-colors">API Docs</a>
        </nav>

        {/* History toggle */}
        <button
          onClick={onToggleHistory}
          className="relative flex items-center gap-2 text-sm text-stone-600 hover:text-leaf-600 
                     bg-stone-50 hover:bg-leaf-50 border border-stone-200 hover:border-leaf-200
                     px-3 py-2 rounded-lg transition-all duration-200"
        >
          <History className="w-4 h-4" />
          <span className="hidden sm:inline">History</span>
          {historyCount > 0 && (
            <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-leaf-500 text-white
                             text-[10px] font-bold rounded-full flex items-center justify-center">
              {historyCount > 9 ? '9+' : historyCount}
            </span>
          )}
        </button>
      </div>
    </header>
  )
}
