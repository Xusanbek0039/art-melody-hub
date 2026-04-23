import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Music2, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

const Kirish = () => {
  return (
    <div className="min-h-screen bg-gradient-hero flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute inset-0 opacity-[0.04] pointer-events-none"
        style={{
          backgroundImage: `radial-gradient(circle at 25% 25%, hsl(var(--accent)) 1px, transparent 1px), radial-gradient(circle at 75% 75%, hsl(var(--gold)) 1px, transparent 1px)`,
          backgroundSize: '60px 60px',
        }}
      />
      <Link to="/" className="absolute top-6 left-6 text-sm text-muted-foreground hover:text-foreground flex items-center gap-2 transition-smooth">
        <ArrowLeft className="w-4 h-4" /> Bosh sahifa
      </Link>

      <div className="w-full max-w-md ornament-card p-8 lg:p-10 relative bg-card/95 backdrop-blur animate-scale-in">
        <Link to="/" className="flex items-center gap-3 mb-8 justify-center">
          <div className="w-12 h-12 rounded-full bg-gradient-gold flex items-center justify-center shadow-gold">
            <Music2 className="w-5 h-5 text-primary" strokeWidth={2.5} />
          </div>
          <div className="flex flex-col leading-tight">
            <span className="font-display text-xl font-bold text-foreground">Madaniyat</span>
            <span className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Platformasi</span>
          </div>
        </Link>

        <div className="text-xs uppercase tracking-[0.3em] text-accent mb-2 text-center">Xush kelibsiz</div>
        <h1 className="font-display text-3xl text-foreground mb-8 text-center">
          Kirish
        </h1>

        <form className="space-y-5">
          <div>
            <Label htmlFor="email" className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">
              Email yoki telefon
            </Label>
            <Input id="email" placeholder="email@misol.uz" className="bg-background h-11" />
          </div>
          <div>
            <Label htmlFor="password" className="text-xs uppercase tracking-widest text-muted-foreground mb-2 block">
              Parol
            </Label>
            <Input id="password" type="password" placeholder="••••••••" className="bg-background h-11" />
          </div>

          <Button variant="hero" size="lg" className="w-full">Kirish</Button>
        </form>

        <div className="suzani-divider my-6 opacity-60" />

        <p className="text-sm text-center text-muted-foreground">
          Hisobingiz yo'qmi?{" "}
          <Link to="/royxat" className="text-accent font-semibold hover:underline">
            Ro'yxatdan o'ting
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Kirish;
