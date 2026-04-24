import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

interface CulturalLoaderProps {
  isLoading?: boolean;
  minDuration?: number;
}

export const CulturalLoader = ({ 
  isLoading = true, 
  minDuration = 2000 
}: CulturalLoaderProps) => {
  const [progress, setProgress] = useState(0);
  const [visible, setVisible] = useState(true);
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    if (!isLoading) return;

    const startTime = Date.now();
    
    // Progress animation
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + Math.random() * 15 + 5;
      });
    }, 200);

    // Check when to hide
    const checkComplete = setInterval(() => {
      const elapsed = Date.now() - startTime;
      if (elapsed >= minDuration && progress >= 100) {
        clearInterval(checkComplete);
        clearInterval(progressInterval);
        setFadeOut(true);
        setTimeout(() => setVisible(false), 500);
      }
    }, 100);

    return () => {
      clearInterval(progressInterval);
      clearInterval(checkComplete);
    };
  }, [isLoading, minDuration, progress]);

  if (!visible) return null;

  return (
    <div 
      className={cn(
        "fixed inset-0 z-[100] flex flex-col items-center justify-center",
        "bg-gradient-to-br from-[#FDF8F3] via-[#F5EDE4] to-[#EDE4D8]",
        "transition-opacity duration-500",
        fadeOut && "opacity-0 pointer-events-none"
      )}
    >
      {/* Suzani Pattern Background */}
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `
            radial-gradient(circle at 20% 30%, #B87333 2px, transparent 2px),
            radial-gradient(circle at 80% 70%, #C9A227 2px, transparent 2px),
            radial-gradient(circle at 50% 50%, #A0522D 1px, transparent 1px)
          `,
          backgroundSize: '80px 80px, 100px 100px, 60px 60px'
        }}
      />

      {/* Main Loader Container */}
      <div className="relative flex flex-col items-center">
        
        {/* Decorative Frame */}
        <div className="absolute -inset-8 border-2 border-[#C9A227]/20 rounded-lg" />
        <div className="absolute -inset-6 border border-[#B87333]/15 rounded-lg" />
        
        {/* Corner Ornaments */}
        <div className="absolute -top-6 -left-6 w-4 h-4 border-t-2 border-l-2 border-[#C9A227]" />
        <div className="absolute -top-6 -right-6 w-4 h-4 border-t-2 border-r-2 border-[#C9A227]" />
        <div className="absolute -bottom-6 -left-6 w-4 h-4 border-b-2 border-l-2 border-[#C9A227]" />
        <div className="absolute -bottom-6 -right-6 w-4 h-4 border-b-2 border-r-2 border-[#C9A227]" />

        {/* Central Icon */}
        <div className="relative mb-8">
          {/* Pulsing rings */}
          <div className="absolute inset-0 animate-ping opacity-20">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-[#C9A227] to-[#B87333]" />
          </div>
          <div className="absolute -inset-4 animate-pulse opacity-30">
            <div className="w-32 h-32 rounded-full border-2 border-[#C9A227]/50" />
          </div>
          
          {/* Main Icon Container */}
          <div className="relative w-24 h-24 rounded-full bg-gradient-to-br from-[#C9A227] via-[#D4AF37] to-[#B87333] flex items-center justify-center shadow-lg">
            <svg 
              viewBox="0 0 24 24" 
              className="w-12 h-12 text-white"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
            >
              {/* Tanbur/Dutor shape */}
              <path d="M8 4C8 4 6 6 6 9C6 12 8 14 8 16C8 18 6 20 6 20" />
              <path d="M16 4C16 4 18 6 18 9C18 12 16 14 16 16C16 18 18 20 18 20" />
              <line x1="8" y1="4" x2="16" y2="4" />
              <line x1="8" y1="20" x2="16" y2="20" />
              {/* Strings */}
              <line x1="10" y1="4" x2="10" y2="20" strokeWidth="0.5" />
              <line x1="12" y1="4" x2="12" y2="20" strokeWidth="0.5" />
              <line x1="14" y1="4" x2="14" y2="20" strokeWidth="0.5" />
            </svg>
          </div>
        </div>

        {/* Brand Name */}
        <h1 className="font-display text-3xl text-[#2D2A26] mb-2 tracking-tight">
          Madaniyat
        </h1>
        <p className="text-sm text-[#8B7355] uppercase tracking-[0.2em] mb-8">
          Milliy san'at platformasi
        </p>

        {/* Progress Bar */}
        <div className="w-64 h-1.5 bg-[#E8E0D5] rounded-full overflow-hidden mb-3">
          <div 
            className="h-full bg-gradient-to-r from-[#C9A227] to-[#B87333] rounded-full transition-all duration-300 ease-out"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
        
        {/* Progress Text */}
        <p className="text-xs text-[#8B7355] font-medium">
          {Math.round(Math.min(progress, 100))}% yuklanmoqda...
        </p>

        {/* Loading Messages */}
        <div className="mt-6 h-6">
          <p className="text-xs text-[#A09080] animate-pulse">
            {progress < 30 && "Notalar kutubxonasi tayyorlanmoqda..."}
            {progress >= 30 && progress < 60 && "Ustalar ma'lumotlari yuklanmoqda..."}
            {progress >= 60 && progress < 90 && "AI yordamchi faollashtirilmoqda..."}
            {progress >= 90 && "Platforma ishga tayyor!"}
          </p>
        </div>
      </div>

      {/* Bottom Decorative Pattern */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-2 opacity-30">
        <div className="w-8 h-px bg-[#C9A227]" />
        <div className="w-2 h-2 rotate-45 border border-[#C9A227]" />
        <div className="w-8 h-px bg-[#C9A227]" />
      </div>
    </div>
  );
};

export default CulturalLoader;
