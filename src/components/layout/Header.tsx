import { Link, useLocation } from "react-router-dom";
import { Music2, Menu, X } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const navItems = [
  { to: "/notalar", label: "Notalar" },
  { to: "/ustalar", label: "Ustalar" },
  { to: "/tanlovlar", label: "Tanlovlar" },
  { to: "/nazariya", label: "Nazariya" },
  { to: "/reels", label: "Reels" },
  { to: "/ai", label: "AI" },
];

export const Header = () => {
  const location = useLocation();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-background/85 backdrop-blur-md border-b border-border/50">
      <div className="container mx-auto px-6 lg:px-12 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-full bg-gradient-gold flex items-center justify-center shadow-gold group-hover:scale-105 transition-smooth">
            <Music2 className="w-5 h-5 text-primary" strokeWidth={2.5} />
          </div>
          <div className="flex flex-col leading-tight">
            <span className="font-display text-xl font-bold text-foreground">Madaniyat</span>
            <span className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Platformasi</span>
          </div>
        </Link>

        <nav className="hidden lg:flex items-center gap-1">
          {navItems.map((item) => {
            const active = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={cn(
                  "px-4 py-2.5 text-sm font-semibold uppercase tracking-wider rounded-md transition-smooth",
                  active
                    ? "text-accent-foreground bg-accent shadow-soft"
                    : "text-foreground/80 hover:text-foreground hover:bg-muted"
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="hidden lg:flex items-center gap-3">
          <Button asChild variant="outline" size="sm">
            <Link to="/kirish">Kirish</Link>
          </Button>
          <Button asChild variant="hero" size="sm">
            <Link to="/royxat">Ro'yxatdan o'tish</Link>
          </Button>
        </div>

        <button
          className="lg:hidden p-2 text-foreground"
          onClick={() => setOpen(!open)}
          aria-label="Menyu"
        >
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {open && (
        <div className="lg:hidden border-t border-border/50 bg-background animate-fade-in">
          <nav className="container mx-auto px-6 py-4 flex flex-col gap-1">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setOpen(false)}
                className="px-4 py-3 text-sm font-medium uppercase tracking-wider hover:bg-muted rounded-sm"
              >
                {item.label}
              </Link>
            ))}
            <div className="flex gap-3 mt-3 pt-3 border-t border-border/50">
              <Button asChild variant="outline" size="sm" className="flex-1">
                <Link to="/kirish" onClick={() => setOpen(false)}>Kirish</Link>
              </Button>
              <Button asChild variant="hero" size="sm" className="flex-1">
                <Link to="/royxat" onClick={() => setOpen(false)}>Ro'yxat</Link>
              </Button>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
};
