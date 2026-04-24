import { PageLayout } from "@/components/layout/PageLayout";
import { Progress } from "@/components/ui/progress";
import { TrendingUp, Clock, Award, Target } from "lucide-react";

const yonalishlar = [
  { name: "Tanbur ijrochiligi", percent: 92, color: "gold" },
  { name: "Solfedjio", percent: 78, color: "accent" },
  { name: "Maqom nazariyasi", percent: 65, color: "pomegranate" },
  { name: "Vokal", percent: 42, color: "ceramic" },
];

const haftaMashqlari = [
  { day: "Du", hours: 2.5 },
  { day: "Se", hours: 3.2 },
  { day: "Ch", hours: 1.8 },
  { day: "Pa", hours: 4.1 },
  { day: "Ju", hours: 2.9 },
  { day: "Sh", hours: 3.5 },
  { day: "Ya", hours: 2.0 },
];

const max = Math.max(...haftaMashqlari.map((d) => d.hours));

const Statistika = () => {
  return (
    <PageLayout
      eyebrow="07 — Statistik tahlil"
      title={<>O'sish <span className="italic text-accent">ko'zgusi</span>.</>}
      description="Mashq vaqti, test natijalari, kuchli yo'nalishlar — barchasi raqamlarda."
    >
      <div className="grid md:grid-cols-4 gap-5 mb-12">
        {[
          { icon: Clock, label: "Jami mashq", value: "142s 30d" },
          { icon: TrendingUp, label: "Bu hafta", value: "+18%" },
          { icon: Target, label: "O'rtacha ball", value: "84%" },
          { icon: Award, label: "Reyting", value: "#127" },
        ].map((s, i) => {
          const Icon = s.icon;
          return (
            <div key={s.label} className="ornament-card p-6 animate-fade-in-up" style={{ animationDelay: `${i * 0.08}s` }}>
              <Icon className="w-5 h-5 text-accent mb-4" />
              <div className="font-display text-3xl text-foreground mb-1">{s.value}</div>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">{s.label}</div>
            </div>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* HAFTA MASHQI */}
        <div className="ornament-card p-7">
          <h3 className="font-display text-2xl text-foreground mb-1">Haftalik mashq</h3>
          <p className="text-sm text-muted-foreground mb-8">Kunlik mashq vaqti (soat)</p>
          <div className="flex items-end gap-3 h-48">
            {haftaMashqlari.map((d, i) => (
              <div key={d.day} className="flex-1 flex flex-col items-center gap-2">
                <div className="text-xs font-semibold text-accent">{d.hours}</div>
                <div
                  className="w-full bg-gradient-gold rounded-t-sm animate-fade-in-up"
                  style={{
                    height: `${(d.hours / max) * 100}%`,
                    animationDelay: `${i * 0.05}s`,
                  }}
                />
                <div className="text-xs uppercase tracking-widest text-muted-foreground">{d.day}</div>
              </div>
            ))}
          </div>
        </div>

        {/* YO'NALISHLAR */}
        <div className="ornament-card p-7">
          <h3 className="font-display text-2xl text-foreground mb-1">Kuchli yo'nalishlar</h3>
          <p className="text-sm text-muted-foreground mb-8">Sohalar bo'yicha o'zlashtirish</p>
          <div className="space-y-6">
            {yonalishlar.map((y, i) => (
              <div key={y.name} className="animate-fade-in-up" style={{ animationDelay: `${i * 0.08}s` }}>
                <div className="flex justify-between items-baseline mb-2">
                  <span className="text-foreground/90">{y.name}</span>
                  <span className="font-display text-xl text-accent">{y.percent}%</span>
                </div>
                <Progress value={y.percent} className="h-2" />
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="ornament-card p-7 mt-6 bg-primary text-primary-foreground border-primary">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="text-xs uppercase tracking-[0.3em] text-gold mb-2">Tavsiya</div>
            <h4 className="font-display text-2xl mb-2">Maqom nazariyasini chuqurlashtiring</h4>
            <p className="text-primary-foreground/70 text-sm max-w-xl">
              Sizning tanbur ko'rsatkichlaringiz a'lo, ammo nazariy bilim yanada yuqori natijalarga olib keladi.
            </p>
          </div>
        </div>
      </div>
    </PageLayout>
  );
};

export default Statistika;
