import { PageLayout } from "@/components/layout/PageLayout";
import { Button } from "@/components/ui/button";
import { Phone, MapPin, Star } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const ustalar = [
  {
    name: "Usta Akbar Rahimov",
    instrument: "Tanbur, Dutor",
    city: "Toshkent",
    phone: "+998 90 123 45 67",
    rating: 4.9,
    items: [
      { name: "Tanbur (yong'oq)", price: "8,500,000 so'm" },
      { name: "Dutor (tut)", price: "4,200,000 so'm" },
    ],
  },
  {
    name: "Usta Jamshid Yo'ldoshev",
    instrument: "Rubob, G'ijjak",
    city: "Samarqand",
    phone: "+998 91 234 56 78",
    rating: 5.0,
    items: [
      { name: "Rubob klassik", price: "6,800,000 so'm" },
      { name: "G'ijjak", price: "3,500,000 so'm" },
    ],
  },
  {
    name: "Usta Bekzod Aliyev",
    instrument: "Doira, Nog'ora",
    city: "Buxoro",
    phone: "+998 93 345 67 89",
    rating: 4.8,
    items: [
      { name: "Doira (echki)", price: "1,200,000 so'm" },
      { name: "Nog'ora", price: "950,000 so'm" },
    ],
  },
  {
    name: "Usta Sherzod Karimov",
    instrument: "Nay, Surnay",
    city: "Farg'ona",
    phone: "+998 94 456 78 90",
    rating: 4.7,
    items: [
      { name: "Nay (qamish)", price: "650,000 so'm" },
      { name: "Surnay", price: "1,400,000 so'm" },
    ],
  },
];

const jihozlar = [
  { name: "Tanbur gilofi", price: "320,000 so'm" },
  { name: "Dutor simlari (to'plam)", price: "85,000 so'm" },
  { name: "Rubob harragi", price: "120,000 so'm" },
  { name: "Tanbur kamertoni", price: "180,000 so'm" },
];

const Ustalar = () => {
  return (
    <PageLayout
      eyebrow="02 — Instrument ustalari"
      title={<>Cholg'u <span className="italic text-accent">ustalari</span>.</>}
      description="Tanbur, dutor, rubob, doira ustalari ro'yxati. To'g'ridan-to'g'ri bog'laning."
    >
      <div className="grid md:grid-cols-2 gap-6 mb-20">
        {ustalar.map((usta, i) => (
          <article
            key={usta.name}
            className="ornament-card p-7 animate-fade-in-up"
            style={{ animationDelay: `${i * 0.08}s` }}
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="font-display text-2xl text-foreground mb-1">{usta.name}</h3>
                <p className="text-sm text-accent uppercase tracking-widest">{usta.instrument}</p>
              </div>
              <div className="flex items-center gap-1 text-gold">
                <Star className="w-4 h-4 fill-current" />
                <span className="font-semibold text-foreground">{usta.rating}</span>
              </div>
            </div>

            <div className="flex items-center gap-4 text-sm text-muted-foreground mb-6">
              <span className="flex items-center gap-1.5"><MapPin className="w-3.5 h-3.5" /> {usta.city}</span>
              <span className="flex items-center gap-1.5"><Phone className="w-3.5 h-3.5" /> {usta.phone}</span>
            </div>

            <div className="space-y-2 mb-6 border-t border-border/50 pt-4">
              {usta.items.map((item) => (
                <div key={item.name} className="flex justify-between items-center text-sm">
                  <span className="text-foreground/80">{item.name}</span>
                  <span className="font-semibold text-accent">{item.price}</span>
                </div>
              ))}
            </div>

            <Button variant="default" size="default" className="w-full">
              <Phone className="w-4 h-4" /> Bog'lanish
            </Button>
          </article>
        ))}
      </div>

      <div className="suzani-divider max-w-md mx-auto mb-16" />

      <h2 className="font-display text-4xl lg:text-5xl text-foreground mb-3">
        Jihozlar va <span className="italic text-accent">aksessuarlar</span>
      </h2>
      <p className="text-muted-foreground mb-10 max-w-xl">Giloflar, simlar, harraklar va boshqa kerakli buyumlar.</p>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {jihozlar.map((j, i) => (
          <div
            key={j.name}
            className="ornament-card p-6 animate-fade-in-up"
            style={{ animationDelay: `${i * 0.05}s` }}
          >
            <div className="text-foreground mb-2">{j.name}</div>
            <div className="font-semibold text-accent mb-4">{j.price}</div>
            <Button variant="outline" size="sm" className="w-full">Sotib olish</Button>
          </div>
        ))}
      </div>
    </PageLayout>
  );
};

export default Ustalar;
