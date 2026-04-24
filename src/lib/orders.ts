// Order persistence + delivery helpers (localStorage)

export type OrderStatus = "Yangi" | "Tasdiqlandi" | "Yo'lda" | "Yetkazildi" | "Bekor qilindi";

export interface OrderItem {
  id: string;
  name: string;
  image: string;
  price: number;
  qty: number;
}

export interface Order {
  id: string;
  createdAt: number;
  status: OrderStatus;
  items: OrderItem[];
  subtotal: number;
  delivery: number;
  total: number;
  customer: {
    name: string;
    phone: string;
    region: string;
    address: string;
    notes?: string;
  };
  payment: {
    method: "cash" | "card";
    provider?: "click" | "payme";
  };
}

const STORAGE_KEY = "madaniyat_orders_v1";

export const loadOrders = (): Order[] => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
};

export const saveOrder = (order: Order) => {
  const all = loadOrders();
  all.unshift(order);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
};

// Region-based delivery pricing (so'm)
// Toshkent shahri eng arzon, uzoq viloyatlar qimmatroq.
const REGION_FEES: Record<string, number> = {
  "Toshkent shahri": 20000,
  "Toshkent viloyati": 30000,
  "Sirdaryo": 40000,
  "Jizzax": 45000,
  "Samarqand": 50000,
  "Namangan": 55000,
  "Andijon": 55000,
  "Farg'ona": 55000,
  "Navoiy": 55000,
  "Buxoro": 60000,
  "Qashqadaryo": 65000,
  "Surxondaryo": 70000,
  "Xorazm": 70000,
  "Qoraqalpog'iston": 80000,
};

export const FREE_DELIVERY_THRESHOLD = 300000;

export const getDeliveryFee = (region: string, subtotal: number): number => {
  if (subtotal >= FREE_DELIVERY_THRESHOLD) return 0;
  if (!region) return 35000; // default until region selected
  return REGION_FEES[region] ?? 35000;
};

export const formatPrice = (n: number) =>
  n.toLocaleString("uz-UZ").replace(/,/g, " ") + " so'm";

export const formatDate = (ts: number) =>
  new Date(ts).toLocaleString("uz-UZ", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
