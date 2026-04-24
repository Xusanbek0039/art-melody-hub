import { PageLayout } from "@/components/layout/PageLayout";
import { Heart, MessageCircle, Share2, Play, Pause, Volume2, VolumeX, Music2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useRef, useState } from "react";
import { cn } from "@/lib/utils";

type ReelType = "video" | "audio";

interface Reel {
  title: string;
  author: string;
  category: string;
  duration: string;
  likes: string;
  color: "gold" | "pomegranate" | "ceramic";
  type: ReelType;
  src: string;
  poster?: string;
}

// Open sample media (CC-licensed sample sources)
const reels: Reel[] = [
  {
    title: "Tanbur — Munojot fragmenti",
    author: "Diyora A.",
    category: "Ijro",
    duration: "0:30",
    likes: "2.4k",
    color: "gold",
    type: "video",
    src: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
  },
  {
    title: "1 daqiqada akkord tuzilishi",
    author: "Ustoz Akbar",
    category: "Mini dars",
    duration: "1:00",
    likes: "5.1k",
    color: "pomegranate",
    type: "video",
    src: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
  },
  {
    title: "Tanovar — yangi cover (audio)",
    author: "Jasur K.",
    category: "Audio trek",
    duration: "0:58",
    likes: "8.7k",
    color: "ceramic",
    type: "audio",
    src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
  },
  {
    title: "Ritmni 3 oson usulda ushlash",
    author: "Madina Y.",
    category: "Layfhak",
    duration: "0:38",
    likes: "3.2k",
    color: "gold",
    type: "video",
    src: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
  },
  {
    title: "Dutor sozi — kalit pozitsiyalar",
    author: "Ustoz Jamshid",
    category: "Mini dars",
    duration: "0:52",
    likes: "4.5k",
    color: "pomegranate",
    type: "audio",
    src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
  },
  {
    title: "Kelinoyim — zamonaviy ijrosi",
    author: "Lola T.",
    category: "Ijro",
    duration: "0:60",
    likes: "9.3k",
    color: "ceramic",
    type: "video",
    src: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
  },
  {
    title: "Maqom kirish darsi",
    author: "Konservatoriya",
    category: "Mini dars",
    duration: "1:12",
    likes: "6.8k",
    color: "gold",
    type: "audio",
    src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
  },
  {
    title: "Doira ritmlari",
    author: "Sardor M.",
    category: "Layfhak",
    duration: "0:42",
    likes: "4.1k",
    color: "pomegranate",
    type: "video",
    src: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
  },
];

const categories = ["Barchasi", "Ijro", "Mini dars", "Audio trek", "Layfhak"];

const ReelCard = ({ r, i }: { r: Reel; i: number }) => {
  const mediaRef = useRef<HTMLVideoElement | HTMLAudioElement | null>(null);
  const [playing, setPlaying] = useState(false);
  const [muted, setMuted] = useState(true);
  const [progress, setProgress] = useState(0);

  const togglePlay = () => {
    const m = mediaRef.current;
    if (!m) return;
    if (playing) {
      m.pause();
      setPlaying(false);
    } else {
      m.play().catch(() => {});
      setPlaying(true);
    }
  };

  const toggleMute = (e: React.MouseEvent) => {
    e.stopPropagation();
    const m = mediaRef.current;
    if (!m) return;
    m.muted = !muted;
    setMuted(!muted);
  };

  const onTime = () => {
    const m = mediaRef.current;
    if (!m || !m.duration) return;
    setProgress((m.currentTime / m.duration) * 100);
  };

  const gradientClass =
    r.color === "gold"
      ? "bg-gradient-gold"
      : r.color === "pomegranate"
      ? "bg-gradient-pomegranate"
      : "bg-ceramic";

  return (
    <article
      className="ornament-card overflow-hidden group cursor-pointer animate-fade-in-up flex flex-col hover:-translate-y-1 transition-elegant"
      style={{ animationDelay: `${i * 0.06}s` }}
      onClick={togglePlay}
    >
      <div className={cn("relative aspect-[9/14] flex items-center justify-center overflow-hidden", gradientClass)}>
        {r.type === "video" ? (
          <video
            ref={mediaRef as React.RefObject<HTMLVideoElement>}
            src={r.src}
            muted={muted}
            playsInline
            loop
            onTimeUpdate={onTime}
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <>
            {/* Audio visualizer placeholder */}
            <audio
              ref={mediaRef as React.RefObject<HTMLAudioElement>}
              src={r.src}
              muted={muted}
              loop
              onTimeUpdate={onTime}
            />
            <div className="absolute inset-0 opacity-15"
              style={{
                backgroundImage: `radial-gradient(circle at 25% 25%, white 1px, transparent 1px), radial-gradient(circle at 75% 75%, white 1px, transparent 1px)`,
                backgroundSize: '30px 30px',
              }}
            />
            {/* Animated bars when playing */}
            <div className="relative z-10 flex items-end gap-1.5 h-24">
              {[...Array(7)].map((_, k) => (
                <span
                  key={k}
                  className={cn(
                    "w-2 rounded-full bg-primary/80",
                    playing ? "animate-pulse" : ""
                  )}
                  style={{
                    height: `${20 + (k % 3) * 25}%`,
                    animationDelay: `${k * 0.12}s`,
                    animationDuration: `${0.6 + (k % 3) * 0.2}s`,
                  }}
                />
              ))}
            </div>
            <Music2 className="absolute bottom-6 left-6 w-6 h-6 text-primary/60" />
          </>
        )}

        {/* Hover/Play overlay */}
        <div className="absolute inset-0 bg-primary/0 group-hover:bg-primary/15 transition-smooth flex items-center justify-center">
          <div
            className={cn(
              "w-16 h-16 rounded-full bg-background/95 flex items-center justify-center shadow-elegant transition-elegant",
              playing
                ? "opacity-0 scale-50"
                : "opacity-90 group-hover:opacity-100 scale-100 group-hover:scale-110"
            )}
          >
            {playing ? (
              <Pause className="w-6 h-6 text-accent" fill="currentColor" />
            ) : (
              <Play className="w-6 h-6 text-accent ml-1" fill="currentColor" />
            )}
          </div>
        </div>

        {/* Top badges */}
        <Badge className="absolute top-3 right-3 bg-primary/85 text-primary-foreground hover:bg-primary text-[10px] z-10">
          {r.duration}
        </Badge>
        <Badge className="absolute top-3 left-3 bg-background/90 text-foreground hover:bg-background text-[10px] uppercase tracking-widest z-10">
          {r.category}
        </Badge>

        {/* Mute toggle */}
        <button
          onClick={toggleMute}
          aria-label={muted ? "Ovozni yoqish" : "Ovozni o'chirish"}
          className="absolute bottom-3 right-3 z-10 w-9 h-9 rounded-full bg-background/90 hover:bg-background flex items-center justify-center shadow-soft transition-smooth hover:scale-110"
        >
          {muted ? <VolumeX className="w-4 h-4 text-foreground" /> : <Volume2 className="w-4 h-4 text-accent" />}
        </button>

        {/* Progress bar */}
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-background/30 z-10">
          <div
            className="h-full bg-accent transition-all duration-150"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="p-4 flex-1 flex flex-col">
        <h3 className="font-display text-base text-foreground mb-1 leading-tight line-clamp-2">{r.title}</h3>
        <p className="text-xs text-muted-foreground mb-3">{r.author}</p>
        <div className="flex items-center justify-between text-xs text-muted-foreground mt-auto pt-3 border-t border-border/40">
          <span className="flex items-center gap-1.5 hover:text-accent transition-smooth">
            <Heart className="w-3.5 h-3.5" /> {r.likes}
          </span>
          <span className="flex items-center gap-1.5 hover:text-accent transition-smooth">
            <MessageCircle className="w-3.5 h-3.5" />
          </span>
          <span className="flex items-center gap-1.5 hover:text-accent transition-smooth">
            <Share2 className="w-3.5 h-3.5" />
          </span>
        </div>
      </div>
    </article>
  );
};

const ART = () => {
  const [activeCat, setActiveCat] = useState("Barchasi");
  const filtered = activeCat === "Barchasi" ? reels : reels.filter((r) => r.category === activeCat);

  return (
    <PageLayout
      eyebrow="08 — ART Reels"
      title={<>Qisqa <span className="italic text-accent">ijrolar</span> va audiolar.</>}
      description="10–60 soniyalik video ijrolar, audio treklar, mini darslar va nazariya layfhaklari. Kartani bosing — ijro boshlanadi."
    >
      <div className="flex gap-3 flex-wrap mb-10">
        {categories.map((c) => (
          <button
            key={c}
            onClick={() => setActiveCat(c)}
            className={cn(
              "px-5 py-2 text-xs uppercase tracking-widest rounded-full border transition-smooth hover:scale-105",
              activeCat === c
                ? "bg-primary text-primary-foreground border-primary shadow-soft"
                : "border-border text-foreground/70 hover:bg-muted hover:border-accent/40"
            )}
          >
            {c}
          </button>
        ))}
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        {filtered.map((r, i) => (
          <ReelCard key={r.title} r={r} i={i} />
        ))}
      </div>
    </PageLayout>
  );
};

export default ART;
