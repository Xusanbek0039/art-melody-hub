import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Download, Play, Search, Music } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const notalar = [
  { title: "Munojot", composer: "Yunus Rajabiy", category: "Maqom", pages: 12, isNew: true },
  { title: "Bayot III", composer: "Xalq kuyi", category: "Xalq", pages: 6 },
  { title: "Ufor Iroq", composer: "Komiljon Otaniyozov", category: "Maqom", pages: 18, isNew: true },
  { title: "Tanovar", composer: "Xalq kuyi", category: "Xalq", pages: 4 },
  { title: "Segoh", composer: "Shashmaqom", category: "Klassik", pages: 24 },
  { title: "Kelinoyim", composer: "Xalq kuyi", category: "Xalq", pages: 8 },
  { title: "Dilxiroj", composer: "Mutavakkil Burhonov", category: "Klassik", pages: 14, isNew: true },
  { title: "Chorgoh", composer: "Shashmaqom", category: "Maqom", pages: 22 },
  { title: "Andijon polkasi", composer: "Xalq kuyi", category: "Xalq", pages: 5 },
];

const categories = ["Barchasi", "Maqom", "Klassik", "Xalq"];

const Notalar = () => {
  return (
    <PageLayout
      eyebrow="01 — Notalar kutubxonasi"
      title={<>Asarlar <span className="italic text-accent">to'plami</span>.</>}
      description="Yunus Rajabiy, Komiljon Otaniyozov va boshqa ustozlar asarlari. Har oyda yangilanadi."
    >
      <div className="flex flex-col lg:flex-row gap-4 mb-10">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input placeholder="Asar yoki bastakor nomi..." className="pl-11 h-12 bg-card" />
        </div>
        <div className="flex gap-2 flex-wrap">
          {categories.map((c, i) => (
            <Button
              key={c}
              variant={i === 0 ? "default" : "outline"}
              size="default"
              className="uppercase tracking-wider text-xs"
            >
              {c}
            </Button>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {notalar.map((nota, i) => (
          <article
            key={nota.title}
            className="ornament-card p-7 animate-fade-in-up"
            style={{ animationDelay: `${i * 0.05}s` }}
          >
            <div className="flex items-start justify-between mb-5">
              <div className="w-12 h-12 rounded-sm bg-gold/15 flex items-center justify-center">
                <Music className="w-5 h-5 text-accent" />
              </div>
              {nota.isNew && (
                <Badge className="bg-pomegranate text-pomegranate-foreground hover:bg-pomegranate/90 uppercase text-[10px] tracking-widest">
                  Yangi
                </Badge>
              )}
            </div>
            <h3 className="font-display text-2xl text-foreground mb-2 leading-tight">
              {nota.title}
            </h3>
            <p className="text-sm text-muted-foreground mb-1">{nota.composer}</p>
            <div className="flex items-center gap-3 text-xs uppercase tracking-widest text-muted-foreground mb-6">
              <span>{nota.category}</span>
              <span className="w-1 h-1 rounded-full bg-muted-foreground/40" />
              <span>{nota.pages} bet</span>
            </div>
            <div className="flex gap-2">
              <Button variant="default" size="sm" className="flex-1">
                <Download className="w-4 h-4" /> PDF
              </Button>
              <Button variant="outline" size="sm" className="flex-1">
                <Play className="w-4 h-4" /> Eshitish
              </Button>
            </div>
          </article>
        ))}
      </div>
    </PageLayout>
  );
};

export default Notalar;
