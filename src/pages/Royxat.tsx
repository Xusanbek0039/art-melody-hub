import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Music2, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

const yonalishlar = [
  "Tanbur", "Dutor", "Rubob", "G'ijjak", "Nay",
  "Doira", "Vokal", "Bastakorlik", "Nazariya"
];

const Royxat = () => {
  return (
    <div className="min-h-screen bg-gradient-hero flex items-center justify-center p-6 relative overflow-hidden py-12">
      <div className="absolute inset-0 opacity-[0.04] pointer-events-none"
        style={{
          backgroundImage: `radial-gradient(circle at 25% 25%, hsl(var(--accent)) 1px, transparent 1px), radial-gradient(circle at 75% 75%, hsl(var(--gold)) 1px, transparent 1px)`,
          backgroundSize: '60px 60px',
        }}
      />
      <Link to="/" className="absolute top-6 left-6 text-sm text-muted-foreground hover:text-foreground flex items-center gap-2 transition-smooth">
        <ArrowLeft className="w-4 h-4" /> Bosh sahifa
      </Link>

      <div className="w-full max-w-2xl ornament-card p-8 lg:p-12 relative bg-card/95 backdrop-blur animate-scale-in">
        <Link to="/" className="flex items-center gap-3 mb-8 justify-center">
          <div className="w-12 h-12 rounded-full bg-gradient-gold flex items-center justify-center shadow-gold">
            <Music2 className="w-5 h-5 text-primary" strokeWidth={2.5} />
          </div>
          <div className="flex flex-col leading-tight">
            <span className="font-display text-xl font-bold text-foreground">Madaniyat</span>
            <span className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Platformasi</span>
          </div>
        </Link>

        <div className="text-xs uppercase tracking-[0.3em] text-accent mb-2 text-center">Bizga qo'shiling</div>
        <h1 className="font-display text-3xl lg:text-4xl text-foreground mb-8 text-center">
          Ro'yxatdan <span className="italic text-accent">o'tish</span>
        </h1>

        <form className="space-y-5">
          <div className="grid sm:grid-cols-3 gap-4">
            <div>
              <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">Familiya *</Label>
              <Input placeholder="Familiyangiz" className="bg-background h-11" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">Ism *</Label>
              <Input placeholder="Ismingiz" className="bg-background h-11" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">Otasining ismi *</Label>
              <Input placeholder="Otangiz ismi" className="bg-background h-11" />
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">Email *</Label>
              <Input placeholder="email@misol.uz" type="email" className="bg-background h-11" />
            </div>
            <div>
              <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">Telefon *</Label>
              <Input placeholder="+998 90 123 45 67" type="tel" className="bg-background h-11" />
            </div>
          </div>

          <div>
            <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">
              Manzil / Ta'lim muassasasi *
            </Label>
            <Input placeholder="Masalan: O'zbekiston Davlat Konservatoriyasi" className="bg-background h-11" />
            <p className="text-xs text-muted-foreground mt-1.5">Oliy ta'lim, professional ta'lim yoki BMSM aniq ko'rsating</p>
          </div>

          <div>
            <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-3 block">
              Yo'nalishingizni tanlang *
            </Label>
            <div className="flex flex-wrap gap-2">
              {yonalishlar.map((y) => (
                <button
                  key={y}
                  type="button"
                  className="px-4 py-2 text-sm border border-border rounded-sm hover:border-accent hover:bg-accent/10 transition-smooth"
                >
                  {y}
                </button>
              ))}
            </div>
          </div>

          <div>
            <Label className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">Parol *</Label>
            <Input placeholder="Kuchli parol kiriting" type="password" className="bg-background h-11" />
          </div>

          <Button variant="hero" size="lg" className="w-full">SMS kod olish</Button>
        </form>

        <div className="suzani-divider my-6 opacity-60" />

        <p className="text-sm text-center text-muted-foreground">
          Hisobingiz bormi?{" "}
          <Link to="/kirish" className="text-accent font-semibold hover:underline">
            Kirish
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Royxat;
