import { PageLayout } from "@/components/layout/PageLayout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ShoppingCart, Heart, Star, Filter, Search, Truck, Shield, Package, Plus, Minus } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

import dutorImg from "@/assets/market-dutor.jpg";
import tanburImg from "@/assets/market-tanbur.jpg";
import rubobImg from "@/assets/market-rubob.jpg";
import torlarImg from "@/assets/market-torlar.jpg";
import doiraImg from "@/assets/market-doira.jpg";
import gilofImg from "@/assets/market-gilof.jpg";

interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  oldPrice?: number;
  rating: number;
  reviews: number;
  image: string;
  badge?: "Yangi" | "Chegirma" | "Top";
  inStock: boolean;
}

const products: Product[] = [
  { id: "1", name: "Dutor — Andijon ustaxonasi", category: "Cholg'u", price: 2400000, oldPrice: 2800000, rating: 4.9, reviews: 124, image: dutorImg, badge: "Chegirma", inStock: true },
  { id: "2", name: "Tanbur — klassik shakl", category: "Cholg'u", price: 3200000, rating: 5.0, reviews: 87, image: tanburImg, badge: "Top", inStock: true },
  { id: "3", name: "Rubob — Farg'ona uslubi", category: "Cholg'u", price: 2750000, rating: 4.8, reviews: 56, image: rubobImg, badge: "Yangi", inStock: true },
  { id: "4", name: "Tor to'plami va sozlash", category: "Aksessuar", price: 185000, rating: 4.7, reviews: 312, image: torlarImg, inStock: true },
  { id: "5", name: "Doira — qo'lda ishlangan", category: "Cholg'u", price: 850000, rating: 4.9, reviews: 98, image: doiraImg, badge: "Top", inStock: true },
  { id: "6", name: "G'ilof (suzani naqsh)", category: "Aksessuar", price: 420000, oldPrice: 520000, rating: 4.6, reviews: 73, image: gilofImg, badge: "Chegirma", inStock: true },
];

const categories = ["Barchasi", "Cholg'u", "Aksessuar"];

const formatPrice = (n: number) =>
  n.toLocaleString("uz-UZ").replace(/,/g, " ") + " so'm";

const ProductCard = ({ p, i, onAdd, onLike, liked }: {
  p: Product;
  i: number;
  onAdd: (p: Product) => void;
  onLike: (id: string) => void;
  liked: boolean;
}) => {
  const badgeStyle =
    p.badge === "Chegirma"
      ? "bg-pomegranate text-pomegranate-foreground"
      : p.badge === "Top"
      ? "bg-gold text-gold-foreground"
      : "bg-accent text-accent-foreground";

  return (
    <article
      className="ornament-card overflow-hidden group flex flex-col animate-fade-in-up hover:-translate-y-2 transition-elegant"
      style={{ animationDelay: `${i * 0.08}s` }}
    >
      <div className="relative aspect-square overflow-hidden bg-ceramic/40">
        <img
          src={p.image}
          alt={p.name}
          loading="lazy"
          width={800}
          height={800}
          className="w-full h-full object-cover group-hover:scale-110 transition-elegant duration-700"
        />
        {p.badge && (
          <Badge className={cn("absolute top-3 left-3 text-[10px] uppercase tracking-widest font-bold", badgeStyle)}>
            {p.badge}
          </Badge>
        )}
        <button
          onClick={() => onLike(p.id)}
          aria-label="Sevimlilarga qo'shish"
          className={cn(
            "absolute top-3 right-3 w-10 h-10 rounded-full flex items-center justify-center shadow-soft transition-elegant hover:scale-110",
            liked ? "bg-pomegranate text-pomegranate-foreground" : "bg-background/90 text-foreground hover:bg-background"
          )}
        >
          <Heart className={cn("w-4 h-4", liked && "fill-current")} />
        </button>

        {/* Quick add overlay */}
        <div className="absolute inset-x-3 bottom-3 opacity-0 translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-elegant">
          <Button
            onClick={() => onAdd(p)}
            variant="hero"
            size="sm"
            className="w-full"
          >
            <ShoppingCart className="w-4 h-4" /> Savatga qo'shish
          </Button>
        </div>
      </div>

      <div className="p-5 flex-1 flex flex-col">
        <div className="text-[10px] uppercase tracking-[0.2em] text-accent mb-2">{p.category}</div>
        <h3 className="font-display text-lg text-foreground mb-2 leading-tight line-clamp-2 flex-1">
          {p.name}
        </h3>

        <div className="flex items-center gap-2 mb-3">
          <div className="flex items-center gap-0.5">
            {[...Array(5)].map((_, k) => (
              <Star
                key={k}
                className={cn(
                  "w-3.5 h-3.5",
                  k < Math.floor(p.rating) ? "fill-gold text-gold" : "text-muted-foreground/30"
                )}
              />
            ))}
          </div>
          <span className="text-xs text-muted-foreground">
            {p.rating} ({p.reviews})
          </span>
        </div>

        <div className="flex items-end justify-between gap-3 pt-3 border-t border-border/40">
          <div>
            {p.oldPrice && (
              <div className="text-xs text-muted-foreground line-through">
                {formatPrice(p.oldPrice)}
              </div>
            )}
            <div className="font-display text-xl text-foreground font-bold tabular-nums">
              {formatPrice(p.price)}
            </div>
          </div>
        </div>
      </div>
    </article>
  );
};

const Market = () => {
  const [activeCat, setActiveCat] = useState("Barchasi");
  const [search, setSearch] = useState("");
  const [cart, setCart] = useState<Record<string, number>>({});
  const [liked, setLiked] = useState<Set<string>>(new Set());
  const [showCart, setShowCart] = useState(false);

  const filtered = products.filter((p) => {
    const catOk = activeCat === "Barchasi" || p.category === activeCat;
    const searchOk = p.name.toLowerCase().includes(search.toLowerCase());
    return catOk && searchOk;
  });

  const cartCount = Object.values(cart).reduce((s, n) => s + n, 0);
  const cartTotal = Object.entries(cart).reduce((sum, [id, qty]) => {
    const p = products.find((x) => x.id === id);
    return sum + (p ? p.price * qty : 0);
  }, 0);

  const addToCart = (p: Product) => {
    setCart((c) => ({ ...c, [p.id]: (c[p.id] || 0) + 1 }));
    toast.success(`${p.name} savatga qo'shildi`);
  };

  const updateQty = (id: string, delta: number) => {
    setCart((c) => {
      const next = { ...c };
      const newQty = (next[id] || 0) + delta;
      if (newQty <= 0) delete next[id];
      else next[id] = newQty;
      return next;
    });
  };

  const toggleLike = (id: string) => {
    setLiked((l) => {
      const n = new Set(l);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });
  };

  return (
    <PageLayout
      eyebrow="09 — Market"
      title={<>Cholg'u <span className="italic text-accent">do'koni</span>.</>}
      description="Dutor, tanbur, rubob va boshqa milliy cholg'u asboblari, torlar, g'iloflar va aksessuarlar. To'g'ridan-to'g'ri ustalardan."
    >
      {/* Trust badges */}
      <div className="grid grid-cols-3 gap-4 mb-10 animate-fade-in-up">
        {[
          { icon: Truck, label: "Bepul yetkazib berish", sub: "300 000 so'mdan boshlab" },
          { icon: Shield, label: "Sifat kafolati", sub: "Tasdiqlangan ustalar" },
          { icon: Package, label: "14 kun qaytarish", sub: "Hech qanday savol yo'q" },
        ].map((b, i) => (
          <div
            key={b.label}
            className="flex items-center gap-3 p-4 rounded-md bg-muted/40 border border-border/40 hover:border-accent/40 transition-smooth"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className="w-11 h-11 rounded-full bg-gold/20 flex items-center justify-center shrink-0">
              <b.icon className="w-5 h-5 text-accent" />
            </div>
            <div className="hidden sm:block">
              <div className="text-sm font-semibold text-foreground">{b.label}</div>
              <div className="text-xs text-muted-foreground">{b.sub}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Filter bar */}
      <div className="flex flex-col lg:flex-row gap-4 items-stretch lg:items-center justify-between mb-10">
        <div className="flex gap-2 flex-wrap">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setActiveCat(c)}
              className={cn(
                "px-5 py-2.5 text-xs uppercase tracking-widest rounded-full border transition-smooth font-semibold hover:scale-105",
                activeCat === c
                  ? "bg-primary text-primary-foreground border-primary shadow-soft"
                  : "border-border text-foreground/70 hover:bg-muted hover:border-accent/40"
              )}
            >
              <Filter className="w-3 h-3 inline mr-1.5" />
              {c}
            </button>
          ))}
        </div>

        <div className="relative flex-1 lg:max-w-xs">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Mahsulot qidirish..."
            className="w-full pl-11 pr-4 py-2.5 rounded-full bg-muted/50 border border-border focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 text-sm transition-smooth"
          />
        </div>
      </div>

      {/* Products grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground">
          Hech narsa topilmadi. Boshqa so'z bilan urinib ko'ring.
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((p, i) => (
            <ProductCard
              key={p.id}
              p={p}
              i={i}
              onAdd={addToCart}
              onLike={toggleLike}
              liked={liked.has(p.id)}
            />
          ))}
        </div>
      )}

      {/* Floating cart */}
      {cartCount > 0 && (
        <button
          onClick={() => setShowCart(true)}
          className="fixed bottom-28 right-6 z-40 flex items-center gap-3 px-5 py-3.5 rounded-full bg-pomegranate text-pomegranate-foreground shadow-elegant hover:scale-105 transition-elegant animate-scale-in"
        >
          <ShoppingCart className="w-5 h-5" />
          <span className="font-bold tabular-nums">{cartCount}</span>
          <span className="text-sm hidden sm:inline">savatda</span>
        </button>
      )}

      {/* Cart drawer */}
      {showCart && (
        <div
          className="fixed inset-0 z-50 bg-foreground/40 animate-fade-in"
          onClick={() => setShowCart(false)}
        >
          <div
            className="absolute right-0 top-0 bottom-0 w-full max-w-md bg-background shadow-elegant animate-slide-in-right flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-border flex items-center justify-between">
              <h3 className="font-display text-2xl">Savatcha</h3>
              <button
                onClick={() => setShowCart(false)}
                className="text-muted-foreground hover:text-foreground"
              >
                ✕
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {Object.entries(cart).map(([id, qty]) => {
                const p = products.find((x) => x.id === id);
                if (!p) return null;
                return (
                  <div key={id} className="flex gap-4 items-center pb-4 border-b border-border/40">
                    <img src={p.image} alt={p.name} className="w-16 h-16 rounded-md object-cover" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-semibold truncate">{p.name}</div>
                      <div className="text-xs text-muted-foreground">{formatPrice(p.price)}</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => updateQty(id, -1)}
                        className="w-7 h-7 rounded-full bg-muted hover:bg-accent hover:text-accent-foreground flex items-center justify-center transition-smooth"
                      >
                        <Minus className="w-3 h-3" />
                      </button>
                      <span className="w-6 text-center text-sm font-bold tabular-nums">{qty}</span>
                      <button
                        onClick={() => updateQty(id, 1)}
                        className="w-7 h-7 rounded-full bg-muted hover:bg-accent hover:text-accent-foreground flex items-center justify-center transition-smooth"
                      >
                        <Plus className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="p-6 border-t border-border space-y-4">
              <div className="flex justify-between items-baseline">
                <span className="text-muted-foreground">Jami:</span>
                <span className="font-display text-2xl font-bold tabular-nums">
                  {formatPrice(cartTotal)}
                </span>
              </div>
              <Button variant="hero" size="lg" className="w-full" onClick={() => toast.success("Buyurtma qabul qilindi!")}>
                Buyurtma berish
              </Button>
            </div>
          </div>
        </div>
      )}
    </PageLayout>
  );
};

export default Market;
