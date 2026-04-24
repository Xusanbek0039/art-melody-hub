import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useState, useEffect } from "react";
import Index from "./pages/Index.tsx";
import NotFound from "./pages/NotFound.tsx";
import Notalar from "./pages/Notalar.tsx";
import Ustalar from "./pages/Ustalar.tsx";
import Tanlovlar from "./pages/Tanlovlar.tsx";
import Nazariya from "./pages/Nazariya.tsx";
import Profil from "./pages/Profil.tsx";
import AI from "./pages/AI.tsx";
import Statistika from "./pages/Statistika.tsx";
import ART from "./pages/ART.tsx";
import Kirish from "./pages/Kirish.tsx";
import Royxat from "./pages/Royxat.tsx";
import Market from "./pages/Market.tsx";
import CulturalLoader from "./components/CulturalLoader.tsx";

const queryClient = new QueryClient();

const AppContent = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate initial app loading
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <CulturalLoader />;
  }

  return (
    <Routes>
      <Route path="/" element={<Index />} />
      <Route path="/notalar" element={<Notalar />} />
      <Route path="/ustalar" element={<Ustalar />} />
      <Route path="/tanlovlar" element={<Tanlovlar />} />
      <Route path="/nazariya" element={<Nazariya />} />
      <Route path="/profil" element={<Profil />} />
      <Route path="/ai" element={<AI />} />
      <Route path="/statistika" element={<Statistika />} />
      <Route path="/reels" element={<ART />} />
      <Route path="/kirish" element={<Kirish />} />
      <Route path="/royxat" element={<Royxat />} />
      <Route path="/market" element={<Market />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
