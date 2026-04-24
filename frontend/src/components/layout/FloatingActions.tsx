import { Link } from "react-router-dom";
import { Search, Plus, Bot, X, ShoppingBag } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const quickActions = [
  { to: "/notalar", label: "Notalar qidirish", icon: Search, color: "bg-gold text-gold-foreground" },
  { to: "/market", label: "Market", icon: ShoppingBag, color: "bg-ceramic text-ceramic-foreground" },
  { to: "/ai", label: "AI yordamchi", icon: Bot, color: "bg-pomegranate text-pomegranate-foreground" },
];

export const FloatingActions = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end gap-3">
      {open && (
        <div className="flex flex-col items-end gap-3 animate-fade-in-up">
          {quickActions.map((a) => {
            const Icon = a.icon;
            return (
              <Link
                key={a.to}
                to={a.to}
                onClick={() => setOpen(false)}
                className="flex items-center gap-3 group"
              >
                <span className="px-3 py-1.5 rounded-sm bg-foreground text-background text-xs font-semibold uppercase tracking-wider shadow-warm opacity-0 group-hover:opacity-100 transition-smooth">
                  {a.label}
                </span>
                <span className={cn(
                  "w-12 h-12 rounded-full flex items-center justify-center shadow-warm hover:scale-110 transition-smooth",
                  a.color
                )}>
                  <Icon className="w-5 h-5" />
                </span>
              </Link>
            );
          })}
        </div>
      )}

      <button
        onClick={() => setOpen(!open)}
        aria-label={open ? "Yopish" : "Tezkor harakatlar"}
        className={cn(
          "w-16 h-16 rounded-full flex items-center justify-center shadow-elegant transition-smooth",
          "bg-gradient-gold text-primary hover:scale-110 active:scale-95",
          open && "rotate-45"
        )}
      >
        {open ? <X className="w-7 h-7" strokeWidth={2.5} /> : <Plus className="w-7 h-7" strokeWidth={2.5} />}
      </button>
    </div>
  );
};
