import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Calendar, MapPin, Trophy, Award } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const tanlovlar = [
  {
    title: "Sharq Taronalari",
    type: "Xalqaro",
    date: "25-30 Avgust, 2025",
    place: "Samarqand",
    status: "Ro'yxat ochiq",
    desc: "An'anaviy musiqa va san'at festivali — dunyoning 60 dan ortiq mamlakatidan ishtirokchilar.",
  },
  {
    title: "Yangi Avlod",
    type: "Respublika",
    date: "12-15 Oktabr, 2025",
    place: "Toshkent",
    status: "Ro'yxat ochiq",
    desc: "Yosh ijrochilar uchun respublika ko'rik tanlovi. Yoshi 12-25 oraliqdagi ishtirokchilar uchun.",
  },
  {
    title: "Maqom Ustalari",
    type: "Xalqaro",
    date: "Mart, 2026",
    place: "Buxoro",
    status: "Tez orada",
    desc: "Shashmaqom san'atining yetuk ijrochilarini aniqlash bo'yicha xalqaro tanlov.",
  },
];

const goliblar = [
  { rank: 1, name: "Diyora Aliyeva", direction: "Tanbur", year: "2024", region: "Toshkent" },
  { rank: 2, name: "Jasur Karimov", direction: "Vokal", year: "2024", region: "Andijon" },
  { rank: 3, name: "Madina Yusupova", direction: "Dutor", year: "2024", region: "Samarqand" },
  { rank: 1, name: "Behruz Saidov", direction: "Rubob", year: "2023", region: "Buxoro" },
  { rank: 2, name: "Lola Tursunova", direction: "Vokal", year: "2023", region: "Farg'ona" },
];

const Tanlovlar = () => {
  return (
    <PageLayout
      eyebrow="03 — Ko'rik tanlovlari"
      title={<>Iste'dodlar <span className="italic text-accent">maydoni</span>.</>}
      description="Respublika va xalqaro ko'rik tanlovlar, g'oliblar reytingi va yutuqlar e'lon doskasi."
    >
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
        {tanlovlar.map((t, i) => (
          <article
            key={t.title}
            className="ornament-card p-7 flex flex-col animate-fade-in-up"
            style={{ animationDelay: `${i * 0.08}s` }}
          >
            <Badge
              className={`self-start mb-4 uppercase text-[10px] tracking-widest ${
                t.type === "Xalqaro"
                  ? "bg-pomegranate text-pomegranate-foreground hover:bg-pomegranate/90"
                  : "bg-ceramic text-ceramic-foreground hover:bg-ceramic/90"
              }`}
            >
              {t.type}
            </Badge>
            <h3 className="font-display text-2xl text-foreground mb-3 leading-tight">{t.title}</h3>
            <p className="text-sm text-muted-foreground mb-5 flex-1 leading-relaxed">{t.desc}</p>
            <div className="space-y-2 text-sm border-t border-border/50 pt-4 mb-5">
              <div className="flex items-center gap-2 text-foreground/80">
                <Calendar className="w-4 h-4 text-accent" /> {t.date}
              </div>
              <div className="flex items-center gap-2 text-foreground/80">
                <MapPin className="w-4 h-4 text-accent" /> {t.place}
              </div>
            </div>
            <Button variant="default" size="default" className="w-full">
              {t.status}
            </Button>
          </article>
        ))}
      </div>

      <div className="suzani-divider max-w-md mx-auto mb-12" />

      <div className="flex items-end justify-between flex-wrap gap-4 mb-10">
        <div>
          <h2 className="font-display text-4xl lg:text-5xl text-foreground mb-3">
            G'oliblar <span className="italic text-accent">reytingi</span>
          </h2>
          <p className="text-muted-foreground">Mingtalik ro'yxati — har 3 o'quv yili davomida.</p>
        </div>
        <div className="flex items-center gap-2 text-gold">
          <Trophy className="w-5 h-5" />
          <span className="text-sm uppercase tracking-widest">Top istedodlar</span>
        </div>
      </div>

      <div className="ornament-card overflow-hidden">
        <div className="grid grid-cols-12 gap-4 px-6 py-4 border-b border-border/50 text-xs uppercase tracking-widest text-muted-foreground bg-muted/40">
          <div className="col-span-1">#</div>
          <div className="col-span-4">Ism</div>
          <div className="col-span-3">Yo'nalish</div>
          <div className="col-span-2">Hudud</div>
          <div className="col-span-2 text-right">Yil</div>
        </div>
        {goliblar.map((g, i) => (
          <div
            key={`${g.name}-${g.year}`}
            className="grid grid-cols-12 gap-4 px-6 py-5 border-b border-border/30 last:border-0 hover:bg-muted/30 transition-smooth items-center animate-fade-in"
            style={{ animationDelay: `${i * 0.04}s` }}
          >
            <div className="col-span-1">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                g.rank === 1 ? 'bg-gold text-gold-foreground' : g.rank === 2 ? 'bg-muted text-foreground' : 'bg-pomegranate/20 text-pomegranate'
              }`}>
                {g.rank}
              </div>
            </div>
            <div className="col-span-4 font-display text-lg text-foreground flex items-center gap-2">
              {g.rank === 1 && <Award className="w-4 h-4 text-gold" />}
              {g.name}
            </div>
            <div className="col-span-3 text-sm text-muted-foreground">{g.direction}</div>
            <div className="col-span-2 text-sm text-muted-foreground">{g.region}</div>
            <div className="col-span-2 text-right text-sm text-accent font-semibold">{g.year}</div>
          </div>
        ))}
      </div>
    </PageLayout>
  );
};

export default Tanlovlar;
