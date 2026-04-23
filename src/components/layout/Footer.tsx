import { Music2, Mail, Phone, MapPin } from "lucide-react";
import { Link } from "react-router-dom";

export const Footer = () => {
  return (
    <footer className="bg-primary text-primary-foreground mt-32">
      <div className="suzani-divider opacity-60" />
      <div className="container mx-auto px-6 lg:px-12 py-16">
        <div className="grid md:grid-cols-4 gap-12">
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-full bg-gradient-gold flex items-center justify-center">
                <Music2 className="w-5 h-5 text-primary" strokeWidth={2.5} />
              </div>
              <div className="flex flex-col leading-tight">
                <span className="font-display text-xl font-bold">Madaniyat</span>
                <span className="text-[10px] uppercase tracking-[0.2em] opacity-70">Platformasi</span>
              </div>
            </Link>
            <p className="text-primary-foreground/70 max-w-md leading-relaxed">
              San'at va musiqa sohasini raqamlashtirgan, yosh istedodlarni qo'llab-quvvatlaydigan yagona milliy platforma.
            </p>
          </div>

          <div>
            <h4 className="font-display text-lg mb-4 text-gold">Bo'limlar</h4>
            <ul className="space-y-2 text-sm text-primary-foreground/70">
              <li><Link to="/notalar" className="hover:text-gold transition-smooth">Notalar kutubxonasi</Link></li>
              <li><Link to="/ustalar" className="hover:text-gold transition-smooth">Instrument ustalari</Link></li>
              <li><Link to="/tanlovlar" className="hover:text-gold transition-smooth">Ko'rik tanlovlari</Link></li>
              <li><Link to="/nazariya" className="hover:text-gold transition-smooth">Musiqa nazariyasi</Link></li>
              <li><Link to="/reels" className="hover:text-gold transition-smooth">ART Reels</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-display text-lg mb-4 text-gold">Aloqa</h4>
            <ul className="space-y-3 text-sm text-primary-foreground/70">
              <li className="flex items-center gap-2"><Mail className="w-4 h-4 text-gold" /> info@madaniyat.uz</li>
              <li className="flex items-center gap-2"><Phone className="w-4 h-4 text-gold" /> +998 71 200 00 00</li>
              <li className="flex items-center gap-2"><MapPin className="w-4 h-4 text-gold" /> Toshkent, O'zbekiston</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-primary-foreground/15 mt-12 pt-6 flex flex-col md:flex-row justify-between gap-4 text-sm text-primary-foreground/50">
          <p>© 2025 Madaniyat Platformasi. Barcha huquqlar himoyalangan.</p>
          <p>San'at — millat ko'zgusi.</p>
        </div>
      </div>
    </footer>
  );
};
