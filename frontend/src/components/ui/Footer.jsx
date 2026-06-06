/**
 * Footer.jsx — Minimal footer with attribution and links.
 */

import { Leaf, Github, ExternalLink } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-white border-t border-stone-100 mt-16">
      <div className="container mx-auto px-4 max-w-6xl py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">

          <div className="flex items-center gap-2 text-stone-500 text-sm">
            <Leaf className="w-4 h-4 text-leaf-500" />
            <span>PlantAI — Powered by EfficientNet-B3 + PlantVillage Dataset</span>
          </div>

          <div className="flex items-center gap-5 text-sm text-stone-400">
            <a href="https://github.com/spMohanty/PlantVillage-Dataset"
               target="_blank" rel="noreferrer"
               className="hover:text-leaf-600 transition-colors flex items-center gap-1">
              <ExternalLink className="w-3.5 h-3.5" />
              Dataset
            </a>
            <a href="http://localhost:8000/docs"
               target="_blank" rel="noreferrer"
               className="hover:text-leaf-600 transition-colors flex items-center gap-1">
              <ExternalLink className="w-3.5 h-3.5" />
              API Docs
            </a>
            <a href="https://github.com"
               target="_blank" rel="noreferrer"
               className="hover:text-leaf-600 transition-colors flex items-center gap-1">
              <Github className="w-3.5 h-3.5" />
              GitHub
            </a>
          </div>
        </div>

        <p className="text-center text-xs text-stone-300 mt-6">
          For educational and research purposes. Not a substitute for professional agricultural advice.
        </p>
      </div>
    </footer>
  )
}
