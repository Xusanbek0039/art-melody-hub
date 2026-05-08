import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2, ChevronRight, Trophy } from "lucide-react";

const darajalar = [
  { level: "Boshlang'ich", count: 45, completed: 32, color: "ceramic" },
  { level: "O'rta", count: 60, completed: 18, color: "gold" },
  { level: "Yuqori", count: 80, completed: 4, color: "pomegranate" },
];

const testlar = [
  { name: "Solfedjio asoslari", level: "Boshlang'ich", questions: 25, score: 92 },
  { name: "Notalar va belgilar", level: "Boshlang'ich", questions: 30, score: 88 },
  { name: "Intervallar", level: "O'rta", questions: 40, score: 76 },
  { name: "Akkordlar tuzilishi", level: "O'rta", questions: 35, score: null },
  { name: "Maqom shakllari", level: "Yuqori", questions: 50, score: null },
  { name: "Garmoniya tahlili", level: "Yuqori", questions: 45, score: null },
];

const Nazariya = () => {
  return (
    <PageLayout
      eyebrow="04 — Musiqa nazariyasi"
      title={<>Bilim <span className="italic text-accent">maydoni</span>.</>}
      description="Solfedjio va nazariya bo'yicha testlar. Abituriyentlar uchun ideal — qayta-qayta topshiring."
    >
      <div className="grid md:grid-cols-3 gap-5 mb-16">
        {darajalar.map((d, i) => (
          <div
            key={d.level}
            className="ornament-card p-7 animate-fade-in-up"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className="text-xs uppercase tracking-widest text-muted-foreground mb-2">Daraja {i + 1}</div>
            <h3 className="font-display text-3xl text-foreground mb-4">{d.level}</h3>
            <div className="flex items-baseline gap-2 mb-4">
              <span className="text-4xl font-display text-accent">{d.completed}</span>
              <span className="text-muted-foreground">/ {d.count} test bajarildi</span>
            </div>
            <Progress value={(d.completed / d.count) * 100} className="h-1.5" />
          </div>
        ))}
      </div>

      <h2 className="font-display text-3xl lg:text-4xl text-foreground mb-8">Mavjud testlar</h2>

      <div className="space-y-3">
        {testlar.map((t, i) => (
          <div
            key={t.name}
            className="ornament-card p-5 lg:p-6 flex items-center gap-4 group cursor-pointer animate-fade-in-up"
            style={{ animationDelay: `${i * 0.05}s` }}
          >
            <div className="w-12 h-12 rounded-sm bg-gold/15 flex items-center justify-center shrink-0">
              {t.score !== null ? (
                <CheckCircle2 className="w-5 h-5 text-accent" />
              ) : (
                <span className="font-display text-lg text-accent">{i + 1}</span>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-display text-xl text-foreground mb-1 truncate">{t.name}</div>
              <div className="flex items-center gap-3 text-xs uppercase tracking-widest text-muted-foreground">
                <span>{t.level}</span>
                <span className="w-1 h-1 rounded-full bg-muted-foreground/40" />
                <span>{t.questions} ta savol</span>
              </div>
            </div>
            {t.score !== null && (
              <div className="hidden sm:flex items-center gap-2 mr-2">
                <Trophy className="w-4 h-4 text-gold" />
                <span className="font-display text-2xl text-accent">{t.score}%</span>
              </div>
            )}
            <Button variant="outline" size="sm" className="shrink-0">
              {t.score !== null ? "Qayta" : "Boshlash"} <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        ))}
      </div>
    </PageLayout>
  );
};

export default Nazariya;
