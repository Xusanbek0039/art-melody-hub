import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
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

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
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
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
