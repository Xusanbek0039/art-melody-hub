import { PageLayout } from "@/components/layout/PageLayout";
import { Heart, MessageCircle, Share2, Music2, Play } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const reels = [
  { title: "Tanbur — Munojot fragmenti", author: "Diyora A.", category: "Ijro", duration: "0:45", likes: "2.4k", color: "gold" },
  { title: "1 daqiqada akkord tuzilishi", author: "Ustoz Akbar", category: "Mini dars", duration: "1:00", likes: "5.1k", color: "pomegranate" },
  { title: "Tanovar — yangi cover", author: "Jasur K.", category: "Yangi trek", duration: "0:58", likes: "8.7k", color: "ceramic" },
  { title: "Ritmni 3 oson usulda ushlash", author: "Madina Y.", category: "Layfhak", duration: "0:38", likes: "3.2k", color: "gold" },
  { title: "Dutor sozi — kalit pozitsiyalar", author: "Ustoz Jamshid", category: "Mini dars", duration: "0:52", likes: "4.5k", color: "pomegranate" },
  { title: "Kelinoyim — zamonaviy ijrosi", author: "Lola T.", category: "Ijro", duration: "0:60", likes: "9.3k", color: "ceramic" },
];

const ART = () => {
  return (
    <PageLayout
      eyebrow="08 — ART Reels"
      title={<>Qisqa <span className="italic text-accent">ijrolar</span>.</>}
      description="10–60 soniyalik ijrolar, mini darslar, yangi treklar va nazariya layfhaklari."
    >
      <div className="flex gap-3 flex-wrap mb-10">
        {["Barchasi", "Ijro", "Mini dars", "Yangi trek", "Layfhak"].map((c, i) => (
          <button
            key={c}
            className={`px-5 py-2 text-xs uppercase tracking-widest rounded-full border transition-smooth ${
              i === 0
                ? "bg-primary text-primary-foreground border-primary"
                : "border-border text-foreground/70 hover:bg-muted hover:border-accent/40"
            }`}
          >
            {c}
          </button>
        ))}
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        {reels.map((r, i) => (
          <article
            key={r.title}
            className="ornament-card overflow-hidden group cursor-pointer animate-fade-in-up flex flex-col"
            style={{ animationDelay: `${i * 0.06}s` }}
          >
            {/* Video preview */}
            <div className={`relative aspect-[9/14] flex items-center justify-center overflow-hidden ${
              r.color === "gold" ? "bg-gradient-gold" :
              r.color === "pomegranate" ? "bg-gradient-pomegranate" :
              "bg-ceramic"
            }`}>
              <div className="absolute inset-0 opacity-15"
                style={{
                  backgroundImage: `radial-gradient(circle at 25% 25%, white 1px, transparent 1px), radial-gradient(circle at 75% 75%, white 1px, transparent 1px)`,
                  backgroundSize: '30px 30px',
                }}
              />
              <Music2 className="w-20 h-20 text-primary/30 group-hover:scale-110 transition-elegant" strokeWidth={1.2} />
              <div className="absolute inset-0 bg-primary/0 group-hover:bg-primary/20 transition-smooth flex items-center justify-center">
                <div className="w-16 h-16 rounded-full bg-background/95 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-smooth scale-75 group-hover:scale-100">
                  <Play className="w-6 h-6 text-accent ml-1" fill="currentColor" />
                </div>
              </div>
              <Badge className="absolute top-3 right-3 bg-primary/85 text-primary-foreground hover:bg-primary text-[10px]">
                {r.duration}
              </Badge>
              <Badge className="absolute top-3 left-3 bg-background/90 text-foreground hover:bg-background text-[10px] uppercase tracking-widest">
                {r.category}
              </Badge>
            </div>

            <div className="p-4 flex-1 flex flex-col">
              <h3 className="font-display text-base text-foreground mb-1 leading-tight line-clamp-2">{r.title}</h3>
              <p className="text-xs text-muted-foreground mb-3">{r.author}</p>
              <div className="flex items-center justify-between text-xs text-muted-foreground mt-auto pt-3 border-t border-border/40">
                <span className="flex items-center gap-1.5"><Heart className="w-3.5 h-3.5" /> {r.likes}</span>
                <span className="flex items-center gap-1.5"><MessageCircle className="w-3.5 h-3.5" /></span>
                <span className="flex items-center gap-1.5"><Share2 className="w-3.5 h-3.5" /></span>
              </div>
            </div>
          </article>
        ))}
      </div>
    </PageLayout>
  );
};

export default ART;
