import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MapPin, Edit2, Trophy, Music, GraduationCap, Plus } from "lucide-react";

const Profil = () => {
  return (
    <PageLayout
      eyebrow="05 — Foydalanuvchi profili"
      title={<>Mening <span className="italic text-accent">sahifam</span>.</>}
      description="Yo'nalishingiz, manzilingiz, qatnashgan tanlovlaringiz va yutuqlaringiz."
    >
      <div className="grid lg:grid-cols-3 gap-6">
        {/* PROFILE CARD */}
        <div className="ornament-card p-8 lg:col-span-1">
          <div className="w-24 h-24 rounded-full bg-gradient-gold mx-auto mb-5 flex items-center justify-center shadow-gold">
            <span className="font-display text-3xl text-primary">DA</span>
          </div>
          <h2 className="font-display text-2xl text-foreground text-center mb-1">Diyora Aliyeva</h2>
          <p className="text-sm text-accent text-center uppercase tracking-widest mb-6">Tanbur ijrochisi</p>

          <div className="space-y-3 text-sm border-t border-border/50 pt-5">
            <div className="flex items-center gap-2 text-foreground/80">
              <MapPin className="w-4 h-4 text-accent" /> Toshkent shahri
            </div>
            <div className="flex items-center gap-2 text-foreground/80">
              <GraduationCap className="w-4 h-4 text-accent" /> O'zbekiston Davlat Konservatoriyasi
            </div>
            <div className="flex items-center gap-2 text-foreground/80">
              <Music className="w-4 h-4 text-accent" /> Yo'nalish: Maqom va xalq cholg'usi
            </div>
          </div>

          <Button variant="outline" size="default" className="w-full mt-6">
            <Edit2 className="w-4 h-4" /> Tahrirlash
          </Button>
        </div>

        {/* STATS + ACHIEVEMENTS */}
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: "Tanlovlar", value: "8" },
              { label: "Yutuqlar", value: "5" },
              { label: "Mashq vaqti", value: "142s" },
            ].map((s) => (
              <div key={s.label} className="ornament-card p-6 text-center">
                <div className="font-display text-4xl text-accent mb-1">{s.value}</div>
                <div className="text-xs uppercase tracking-widest text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>

          {/* TANLOVLAR */}
          <div className="ornament-card p-7">
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-display text-2xl text-foreground">Qatnashgan tanlovlar</h3>
              <Button variant="ghost" size="sm"><Plus className="w-4 h-4" /> Qo'shish</Button>
            </div>
            <div className="space-y-3">
              {[
                { name: "Sharq Taronalari 2024", result: "Diplomant" },
                { name: "Yangi Avlod 2024", result: "I o'rin", gold: true },
                { name: "Maqom Ustalari 2023", result: "Ishtirokchi" },
              ].map((t) => (
                <div key={t.name} className="flex items-center justify-between py-3 border-b border-border/30 last:border-0">
                  <span className="text-foreground/90">{t.name}</span>
                  <Badge className={t.gold ? "bg-gold text-gold-foreground hover:bg-gold/90" : "bg-secondary text-secondary-foreground hover:bg-secondary/80"}>
                    {t.result}
                  </Badge>
                </div>
              ))}
            </div>
          </div>

          {/* YUTUQLAR */}
          <div className="ornament-card p-7">
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-display text-2xl text-foreground">Yutuqlar</h3>
              <Button variant="ghost" size="sm"><Plus className="w-4 h-4" /> Qo'shish</Button>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              {[
                "Yangi Avlod 2024 g'olibi",
                "Solfedjio testidan 92%",
                "100 soat mashq",
                "Konservatoriyaga qabul",
              ].map((y) => (
                <div key={y} className="flex items-center gap-3 p-3 bg-muted/40 rounded-sm">
                  <Trophy className="w-4 h-4 text-gold shrink-0" />
                  <span className="text-sm text-foreground/90">{y}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
};

export default Profil;
