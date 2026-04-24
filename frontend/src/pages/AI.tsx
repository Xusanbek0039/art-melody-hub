import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, Activity, MessageSquare, Sparkles, Play } from "lucide-react";
import { useState } from "react";

const features = [
  { icon: Activity, title: "Metronom", desc: "Aniq ritm uchun shaxsiy metronom — har qanday tezlikda." },
  { icon: MessageSquare, title: "Savol-javob", desc: "Musiqaga oid har qanday savolingizga tezkor javob." },
  { icon: Sparkles, title: "Xato tahlili", desc: "Intonatsiya va ritmingizdagi xatolarni aniqlaydi." },
];

const sampleQA = [
  { q: "Maqom nima?", a: "Maqom — Sharq xalqlari klassik musiqa shakli. O'zbekistonda Shashmaqom (olti maqom) eng mashhur shakli hisoblanadi: Buzruk, Rost, Navo, Dugoh, Segoh va Iroq." },
  { q: "Tanbur necha torli?", a: "An'anaviy o'zbek tanburi 3 torli (ba'zan 4 torli) bo'lib, jezdan yasalgan torlardan tashkil topadi. Asosiy ovoz beruvchi tor — birinchisi." },
];

const AI = () => {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Salom! Men Madaniyat AI yordamchisiman. Musiqa, nazariya, cholg'u asboblar — har qanday savolingizga javob beraman." },
  ]);
  const [input, setInput] = useState("");

  const send = () => {
    if (!input.trim()) return;
    setMessages([
      ...messages,
      { role: "user", text: input },
      { role: "ai", text: "(Demo javob) Bu funksiya backend ulangach to'liq ishlaydi. Hozircha frontend prototip." },
    ]);
    setInput("");
  };

  return (
    <PageLayout
      eyebrow="06 — AI yordamchi"
      title={<>Sizning <span className="italic text-accent">ustozingiz</span>.</>}
      description="Metronom, intonatsiya tahlili, savol-javob — barchasi bitta aqlli yordamchida."
    >
      <div className="grid md:grid-cols-3 gap-5 mb-12">
        {features.map((f, i) => {
          const Icon = f.icon;
          return (
            <div
              key={f.title}
              className="ornament-card p-6 animate-fade-in-up"
              style={{ animationDelay: `${i * 0.08}s` }}
            >
              <div className="w-11 h-11 rounded-sm bg-pomegranate/10 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-pomegranate" />
              </div>
              <h3 className="font-display text-xl text-foreground mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </div>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* CHAT */}
        <div className="lg:col-span-2 ornament-card flex flex-col h-[560px]">
          <div className="flex items-center gap-3 px-6 py-4 border-b border-border/50">
            <div className="w-9 h-9 rounded-full bg-gradient-pomegranate flex items-center justify-center">
              <Bot className="w-4 h-4 text-gold" />
            </div>
            <div>
              <div className="font-display text-foreground">Madaniyat AI</div>
              <div className="text-[10px] uppercase tracking-widest text-accent">Onlayn</div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`flex ${m.role === "user" ? "justify-end" : "justify-start"} animate-fade-in`}
              >
                <div
                  className={`max-w-[80%] px-4 py-3 rounded-sm ${
                    m.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-foreground"
                  }`}
                >
                  {m.text}
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-border/50 flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Savolingizni yozing..."
              className="bg-background"
            />
            <Button onClick={send} variant="default" size="icon"><Send className="w-4 h-4" /></Button>
          </div>
        </div>

        {/* METRONOME + EXAMPLES */}
        <div className="space-y-6">
          <div className="ornament-card p-7 text-center">
            <div className="text-xs uppercase tracking-widest text-muted-foreground mb-3">Metronom</div>
            <div className="font-display text-7xl text-accent mb-2 tabular-nums">120</div>
            <div className="text-xs uppercase tracking-widest text-muted-foreground mb-5">BPM</div>
            <Button variant="hero" size="default" className="w-full">
              <Play className="w-4 h-4" /> Boshlash
            </Button>
          </div>

          <div className="ornament-card p-6">
            <div className="text-xs uppercase tracking-widest text-accent mb-3">Mashhur savollar</div>
            <div className="space-y-2">
              {sampleQA.map((qa) => (
                <button
                  key={qa.q}
                  onClick={() => setMessages([...messages, { role: "user", text: qa.q }, { role: "ai", text: qa.a }])}
                  className="block w-full text-left text-sm text-foreground/80 hover:text-accent p-2 rounded-sm hover:bg-muted transition-smooth"
                >
                  → {qa.q}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
};

export default AI;
