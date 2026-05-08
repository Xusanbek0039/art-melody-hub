import { Layout } from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import {
  Music,
  Hammer,
  Trophy,
  BookOpen,
  User,
  Bot,
  BarChart3,
  Film,
  ArrowRight,
  Sparkles,
  PlayCircle,
} from "lucide-react";
import heroImg from "@/assets/hero-instruments.jpg";

const sections = [
  {
    icon: Music,
    title: "Notalar kutubxonasi",
    desc: "Klassik va xalq kuylari, har oyda yangilanadigan asarlar to'plami. PDF yuklab oling, audio bilan eshitib o'rganing.",
    to: "/notalar",
    color: "gold",
  },
  {
    icon: Hammer,
    title: "Instrument ustalari",
    desc: "Tanbur, dutor, rubob ustalari ro'yxati, jihozlar va bog'lanish ma'lumotlari.",
    to: "/ustalar",
    color: "pomegranate",
  },
  {
    icon: Trophy,
    title: "Ko'rik tanlovlari",
    desc: "Respublika va xalqaro tanlovlar nizomi, manzili, g'oliblar reytingi.",
    to: "/tanlovlar",
    color: "gold",
  },
  {
    icon: BookOpen,
    title: "Musiqa nazariyasi",
    desc: "Solfedjio va nazariya testlari, daraja bo'yicha mashqlar, ballik natijalar.",
    to: "/nazariya",
    color: "ceramic",
  },
  {
    icon: User,
    title: "O'quvchi profili",
    desc: "Yutuqlaringizni qayd eting, yo'nalishingizni tanlang, tanlovlarda qatnashing.",
    to: "/profil",
    color: "gold",
  },
  {
    icon: Bot,
    title: "AI yordamchi",
    desc: "Metronom, intonatsiya tahlili, savol-javob — sizning shaxsiy ustozingiz.",
    to: "/ai",
    color: "pomegranate",
  },
  {
    icon: BarChart3,
    title: "Statistik tahlil",
    desc: "Mashq vaqti, test natijalari, kuchli yo'nalishlar — barchasi bir joyda.",
    to: "/statistika",
    color: "ceramic",
  },
  {
    icon: Film,
    title: "ART Reels",
    desc: "Qisqa ijrolar, mini darslar, yangi treklar va nazariya layfhaklari.",
    to: "/reels",
    color: "gold",
  },
];

const stats = [
  { value: "12k+", label: "Foydalanuvchilar" },
  { value: "850+", label: "Notalar to'plami" },
  { value: "120+", label: "Tan olingan ustalar" },
  { value: "45", label: "Yillik tanlovlar" },
];

const Index = () => {
  return (
    <Layout>
      {/* HERO */}
      <section className="relative overflow-hidden bg-gradient-hero">
        <div className="absolute inset-0 opacity-[0.04] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(circle at 25% 25%, hsl(var(--accent)) 1px, transparent 1px), radial-gradient(circle at 75% 75%, hsl(var(--gold)) 1px, transparent 1px)`,
            backgroundSize: '60px 60px',
          }}
        />
        <div className="container mx-auto px-6 lg:px-12 pt-16 lg:pt-24 pb-20 lg:pb-32 grid lg:grid-cols-2 gap-12 lg:gap-16 items-center relative">
          <div className="animate-fade-in-up">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-gold/15 border border-gold/30 rounded-full text-xs uppercase tracking-widest text-foreground/80 mb-8">
              <Sparkles className="w-3 h-3 text-accent" />
              Milliy san'atning raqamli maskan
            </div>
            <h1 className="font-display text-5xl lg:text-7xl xl:text-8xl leading-[0.95] text-foreground mb-8">
              Madaniyat —<br />
              <span className="italic text-accent">millat</span> ko'zgusi.
            </h1>
            <p className="text-lg lg:text-xl text-muted-foreground mb-10 max-w-[55ch] leading-relaxed">
              O'zbek musiqa va san'at merosini zamonaviy raqamli platforma orqali o'rganing.
              Notalar, ustozlar, tanlovlar va AI yordamchi — barchasi bir joyda.
            </p>
            <div className="flex flex-wrap gap-4">
              <Button asChild variant="hero" size="xl">
                <Link to="/royxat">
                  Bepul boshlash <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="xl">
                <Link to="/reels">
                  <PlayCircle className="w-4 h-4" /> ART Reels
                </Link>
              </Button>
            </div>
          </div>

          <div className="relative animate-scale-in">
            <div className="absolute -top-6 -left-6 w-32 h-32 border-2 border-gold/40 rounded-sm" />
            <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-accent/10 rounded-sm" />
            <div className="relative overflow-hidden rounded-sm shadow-elegant">
              <img
                src={heroImg}
                alt="O'zbek milliy cholg'u asboblari — tanbur va dutor suzani naqshlari fonida"
                width={1536}
                height={1024}
                className="w-full h-auto object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-primary/30 to-transparent" />
            </div>
          </div>
        </div>
      </section>

      {/* SUZANI DIVIDER */}
      <div className="container mx-auto px-12">
        <div className="suzani-divider" />
      </div>

      {/* STATS */}
      <section className="container mx-auto px-6 lg:px-12 py-16">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((s, i) => (
            <div
              key={s.label}
              className="text-center animate-fade-in-up"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div className="font-display text-5xl lg:text-6xl text-accent mb-2 tabular-nums">
                {s.value}
              </div>
              <div className="text-sm uppercase tracking-widest text-muted-foreground">
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* SECTIONS GRID */}
      <section className="container mx-auto px-6 lg:px-12 py-20">
        <div className="max-w-3xl mb-16">
          <div className="text-xs uppercase tracking-[0.3em] text-accent mb-4">
            Platforma bo'limlari
          </div>
          <h2 className="font-display text-4xl lg:text-6xl text-foreground mb-6 leading-[1.05]">
            Sakkiz yo'nalish, bitta maqsad — <span className="italic text-accent">san'at</span>.
          </h2>
          <p className="text-lg text-muted-foreground leading-relaxed">
            Har bir bo'lim alohida e'tibor bilan ishlab chiqilgan. Yosh musiqachidan
            tajribali ustozgacha — har kim o'ziga keraklisini topadi.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {sections.map((section, i) => {
            const Icon = section.icon;
            return (
              <Link
                key={section.title}
                to={section.to}
                className="ornament-card p-7 group animate-fade-in-up flex flex-col"
                style={{ animationDelay: `${i * 0.06}s` }}
              >
                <div
                  className={`w-14 h-14 rounded-md flex items-center justify-center mb-5 transition-smooth group-hover:scale-110 ${
                    section.color === "gold"
                      ? "bg-gold text-gold-foreground"
                      : section.color === "pomegranate"
                      ? "bg-pomegranate text-pomegranate-foreground"
                      : "bg-ceramic text-ceramic-foreground"
                  }`}
                >
                  <Icon className="w-7 h-7" strokeWidth={2} />
                </div>
                <h3 className="font-display text-xl text-foreground mb-3 font-bold">
                  {section.title}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed flex-1">
                  {section.desc}
                </p>
                <div className="mt-5 flex items-center gap-2 text-xs uppercase tracking-widest text-accent font-bold group-hover:gap-3 transition-smooth">
                  Kirish <ArrowRight className="w-3 h-3" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* AI FEATURE CALLOUT */}
      <section className="container mx-auto px-6 lg:px-12 py-20">
        <div className="bg-primary text-primary-foreground rounded-sm overflow-hidden grid md:grid-cols-2 shadow-elegant">
          <div className="p-10 lg:p-16 flex flex-col justify-center">
            <div className="text-xs uppercase tracking-[0.3em] text-gold mb-4">
              Eng kuchli xususiyat
            </div>
            <h3 className="font-display text-4xl lg:text-5xl mb-6 leading-tight">
              AI yordamchi — sizning shaxsiy <span className="italic text-gold">ustozingiz</span>.
            </h3>
            <p className="text-primary-foreground/75 text-lg mb-8 leading-relaxed">
              Metronom vazifasini bajaradi, intonatsiya va ritm xatolarini aniqlaydi,
              musiqaga oid har qanday savolingizga javob beradi.
            </p>
            <div>
              <Button asChild variant="hero" size="lg">
                <Link to="/ai">AI bilan suhbat <ArrowRight className="w-4 h-4" /></Link>
              </Button>
            </div>
          </div>
          <div className="relative bg-gradient-pomegranate p-10 lg:p-16 flex items-center justify-center min-h-[300px]">
            <div className="absolute inset-0 opacity-20"
              style={{
                backgroundImage: `radial-gradient(circle at center, hsl(var(--gold)) 1px, transparent 1px)`,
                backgroundSize: '24px 24px',
              }}
            />
            <Bot className="w-40 h-40 text-gold relative z-10" strokeWidth={1.2} />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-6 lg:px-12 py-24 text-center">
        <h2 className="font-display text-4xl lg:text-6xl text-foreground mb-6 max-w-3xl mx-auto leading-tight">
          Bugun boshlang. <span className="italic text-accent">Ertaga g'olib bo'ling.</span>
        </h2>
        <p className="text-lg text-muted-foreground mb-10 max-w-2xl mx-auto">
          Ro'yxatdan o'tish bepul. Email yoki telefon orqali bir daqiqada qo'shiling.
        </p>
        <Button asChild variant="hero" size="xl">
          <Link to="/royxat">Ro'yxatdan o'tish <ArrowRight className="w-4 h-4" /></Link>
        </Button>
      </section>
    </Layout>
  );
};

export default Index;
