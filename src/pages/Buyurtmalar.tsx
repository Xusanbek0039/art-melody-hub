import { PageLayout } from "@/components/layout/PageLayout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Package, Clock, CheckCircle2, Truck, XCircle, ShoppingBag, ChevronRight } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Order, OrderStatus, formatPrice, formatDate, loadOrders } from "@/lib/orders";

const statusMeta: Record<OrderStatus, { color: string; icon: typeof Clock }> = {
  "Yangi": { color: "bg-accent/15 text-accent border-accent/40", icon: Clock },
  "Tasdiqlandi": { color: "bg-gold/20 text-gold-foreground border-gold/40", icon: CheckCircle2 },
  "Yo'lda": { color: "bg-pomegranate/15 text-pomegranate border-pomegranate/40", icon: Truck },
  "Yetkazildi": { color: "bg-emerald-500/15 text-emerald-600 border-emerald-500/40", icon: CheckCircle2 },
  "Bekor qilindi": { color: "bg-destructive/15 text-destructive border-destructive/40", icon: XCircle },
};

const Buyurtmalar = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);

  useEffect(() => {
    setOrders(loadOrders());
  }, []);

  return (
    <PageLayout
      eyebrow="10 — Mening buyurtmalarim"
      title={<>Buyurtmalar <span className="italic text-accent">tarixi</span>.</>}
      description="Barcha buyurtmalaringiz, ularning holati va yetkazib berish ma'lumotlari shu yerda."
    >
      {orders.length === 0 ? (
        <div className="text-center py-20 animate-fade-in-up">
          <div className="w-24 h-24 rounded-full bg-muted/50 flex items-center justify-center mx-auto mb-6">
            <ShoppingBag className="w-10 h-10 text-muted-foreground" />
          </div>
          <h3 className="font-display text-2xl mb-2">Hali buyurtmalar yo'q</h3>
          <p className="text-muted-foreground mb-6">Marketdan birinchi buyurtmangizni rasmiylashtiring.</p>
          <Button asChild variant="hero" size="lg">
            <Link to="/market">Marketga o'tish →</Link>
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((o, i) => {
            const meta = statusMeta[o.status];
            const Icon = meta.icon;
            const open = openId === o.id;
            return (
              <article
                key={o.id}
                className="ornament-card overflow-hidden animate-fade-in-up"
                style={{ animationDelay: `${i * 0.06}s` }}
              >
                <button
                  onClick={() => setOpenId(open ? null : o.id)}
                  className="w-full p-5 flex items-center gap-4 text-left hover:bg-muted/30 transition-smooth"
                >
                  <div className="w-12 h-12 rounded-full bg-gold/20 flex items-center justify-center shrink-0">
                    <Package className="w-5 h-5 text-accent" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-display text-lg font-bold text-foreground">{o.id}</span>
                      <Badge className={cn("text-[10px] uppercase tracking-widest border", meta.color)}>
                        <Icon className="w-3 h-3 mr-1" /> {o.status}
                      </Badge>
                    </div>
                    <div className="text-xs text-muted-foreground mt-0.5">
                      {formatDate(o.createdAt)} • {o.items.reduce((s, it) => s + it.qty, 0)} mahsulot
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="font-display text-lg font-bold text-accent tabular-nums">
                      {formatPrice(o.total)}
                    </div>
                    <ChevronRight className={cn("w-4 h-4 text-muted-foreground inline transition-smooth", open && "rotate-90")} />
                  </div>
                </button>

                {open && (
                  <div className="px-5 pb-5 border-t border-border/40 animate-fade-in">
                    <div className="grid sm:grid-cols-2 gap-4 pt-4">
                      <div>
                        <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-2">Yetkazib berish</div>
                        <div className="text-sm text-foreground font-semibold">{o.customer.name}</div>
                        <div className="text-sm text-muted-foreground">{o.customer.phone}</div>
                        <div className="text-sm text-muted-foreground">{o.customer.region}, {o.customer.address}</div>
                        {o.customer.notes && <div className="text-xs text-muted-foreground mt-1 italic">"{o.customer.notes}"</div>}
                      </div>
                      <div>
                        <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-2">To'lov</div>
                        <div className="text-sm text-foreground font-semibold capitalize">
                          {o.payment.method === "cash" ? "Naqd (yetkazib berishda)" : `Karta — ${o.payment.provider?.toUpperCase()}`}
                        </div>
                        <div className="text-xs text-muted-foreground mt-2">Mahsulotlar: <span className="tabular-nums">{formatPrice(o.subtotal)}</span></div>
                        <div className="text-xs text-muted-foreground">
                          Yetkazib berish: <span className="tabular-nums">{o.delivery === 0 ? "Bepul" : formatPrice(o.delivery)}</span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-border/40">
                      <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-2">Mahsulotlar</div>
                      <div className="space-y-2">
                        {o.items.map((it) => (
                          <div key={it.id} className="flex items-center gap-3">
                            <img src={it.image} alt={it.name} className="w-10 h-10 rounded object-cover" />
                            <div className="flex-1 text-sm text-foreground truncate">{it.name}</div>
                            <div className="text-xs text-muted-foreground tabular-nums">×{it.qty}</div>
                            <div className="text-sm font-semibold tabular-nums w-28 text-right">{formatPrice(it.price * it.qty)}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </article>
            );
          })}
        </div>
      )}
    </PageLayout>
  );
};

export default Buyurtmalar;
