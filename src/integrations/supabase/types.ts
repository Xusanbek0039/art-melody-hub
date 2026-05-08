export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "14.5"
  }
  public: {
    Tables: {
      ai_conversations: {
        Row: {
          created_at: string
          id: string
          title: string
          updated_at: string
          user_id: string
        }
        Insert: {
          created_at?: string
          id?: string
          title?: string
          updated_at?: string
          user_id: string
        }
        Update: {
          created_at?: string
          id?: string
          title?: string
          updated_at?: string
          user_id?: string
        }
        Relationships: []
      }
      ai_messages: {
        Row: {
          content: string
          conversation_id: string
          created_at: string
          id: string
          role: string
        }
        Insert: {
          content: string
          conversation_id: string
          created_at?: string
          id?: string
          role: string
        }
        Update: {
          content?: string
          conversation_id?: string
          created_at?: string
          id?: string
          role?: string
        }
        Relationships: [
          {
            foreignKeyName: "ai_messages_conversation_id_fkey"
            columns: ["conversation_id"]
            isOneToOne: false
            referencedRelation: "ai_conversations"
            referencedColumns: ["id"]
          },
        ]
      }
      competition_registrations: {
        Row: {
          category: string | null
          competition_id: string
          composer: string | null
          created_at: string
          duration_minutes: number | null
          id: string
          institution: string | null
          notes: string | null
          piece_title: string | null
          teacher_name: string | null
          teacher_phone: string | null
          user_id: string
        }
        Insert: {
          category?: string | null
          competition_id: string
          composer?: string | null
          created_at?: string
          duration_minutes?: number | null
          id?: string
          institution?: string | null
          notes?: string | null
          piece_title?: string | null
          teacher_name?: string | null
          teacher_phone?: string | null
          user_id: string
        }
        Update: {
          category?: string | null
          competition_id?: string
          composer?: string | null
          created_at?: string
          duration_minutes?: number | null
          id?: string
          institution?: string | null
          notes?: string | null
          piece_title?: string | null
          teacher_name?: string | null
          teacher_phone?: string | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "competition_registrations_competition_id_fkey"
            columns: ["competition_id"]
            isOneToOne: false
            referencedRelation: "competitions"
            referencedColumns: ["id"]
          },
        ]
      }
      competition_winners: {
        Row: {
          category: string | null
          competition_id: string | null
          created_at: string
          description: string | null
          full_name: string
          id: string
          photo_url: string | null
          place: number | null
          region: string | null
          user_id: string | null
          year: number | null
        }
        Insert: {
          category?: string | null
          competition_id?: string | null
          created_at?: string
          description?: string | null
          full_name: string
          id?: string
          photo_url?: string | null
          place?: number | null
          region?: string | null
          user_id?: string | null
          year?: number | null
        }
        Update: {
          category?: string | null
          competition_id?: string | null
          created_at?: string
          description?: string | null
          full_name?: string
          id?: string
          photo_url?: string | null
          place?: number | null
          region?: string | null
          user_id?: string | null
          year?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "competition_winners_competition_id_fkey"
            columns: ["competition_id"]
            isOneToOne: false
            referencedRelation: "competitions"
            referencedColumns: ["id"]
          },
        ]
      }
      competitions: {
        Row: {
          contact: string | null
          created_at: string
          description: string | null
          event_end: string | null
          event_start: string | null
          id: string
          is_featured: boolean | null
          level: string | null
          location: string | null
          organizer: string | null
          poster_url: string | null
          registration_end: string | null
          registration_start: string | null
          rules: string | null
          status: Database["public"]["Enums"]["competition_status"]
          title: string
          updated_at: string
        }
        Insert: {
          contact?: string | null
          created_at?: string
          description?: string | null
          event_end?: string | null
          event_start?: string | null
          id?: string
          is_featured?: boolean | null
          level?: string | null
          location?: string | null
          organizer?: string | null
          poster_url?: string | null
          registration_end?: string | null
          registration_start?: string | null
          rules?: string | null
          status?: Database["public"]["Enums"]["competition_status"]
          title: string
          updated_at?: string
        }
        Update: {
          contact?: string | null
          created_at?: string
          description?: string | null
          event_end?: string | null
          event_start?: string | null
          id?: string
          is_featured?: boolean | null
          level?: string | null
          location?: string | null
          organizer?: string | null
          poster_url?: string | null
          registration_end?: string | null
          registration_start?: string | null
          rules?: string | null
          status?: Database["public"]["Enums"]["competition_status"]
          title?: string
          updated_at?: string
        }
        Relationships: []
      }
      note_categories: {
        Row: {
          created_at: string
          description: string | null
          id: string
          name: string
          slug: string
        }
        Insert: {
          created_at?: string
          description?: string | null
          id?: string
          name: string
          slug: string
        }
        Update: {
          created_at?: string
          description?: string | null
          id?: string
          name?: string
          slug?: string
        }
        Relationships: []
      }
      notes: {
        Row: {
          audio_url: string | null
          category_id: string | null
          composer: string | null
          cover_url: string | null
          created_at: string
          description: string | null
          difficulty: string | null
          downloads_count: number | null
          id: string
          is_featured: boolean | null
          pdf_url: string | null
          title: string
          updated_at: string
          views_count: number | null
        }
        Insert: {
          audio_url?: string | null
          category_id?: string | null
          composer?: string | null
          cover_url?: string | null
          created_at?: string
          description?: string | null
          difficulty?: string | null
          downloads_count?: number | null
          id?: string
          is_featured?: boolean | null
          pdf_url?: string | null
          title: string
          updated_at?: string
          views_count?: number | null
        }
        Update: {
          audio_url?: string | null
          category_id?: string | null
          composer?: string | null
          cover_url?: string | null
          created_at?: string
          description?: string | null
          difficulty?: string | null
          downloads_count?: number | null
          id?: string
          is_featured?: boolean | null
          pdf_url?: string | null
          title?: string
          updated_at?: string
          views_count?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "notes_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "note_categories"
            referencedColumns: ["id"]
          },
        ]
      }
      order_items: {
        Row: {
          id: string
          order_id: string
          product_id: string | null
          product_name: string
          quantity: number
          total_price: number
          unit_price: number
        }
        Insert: {
          id?: string
          order_id: string
          product_id?: string | null
          product_name: string
          quantity?: number
          total_price: number
          unit_price: number
        }
        Update: {
          id?: string
          order_id?: string
          product_id?: string | null
          product_name?: string
          quantity?: number
          total_price?: number
          unit_price?: number
        }
        Relationships: [
          {
            foreignKeyName: "order_items_order_id_fkey"
            columns: ["order_id"]
            isOneToOne: false
            referencedRelation: "orders"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "order_items_product_id_fkey"
            columns: ["product_id"]
            isOneToOne: false
            referencedRelation: "products"
            referencedColumns: ["id"]
          },
        ]
      }
      orders: {
        Row: {
          address: string
          created_at: string
          customer_name: string
          customer_phone: string
          delivery_fee: number | null
          id: string
          notes: string | null
          order_number: string
          payment_method: string | null
          region: string
          status: Database["public"]["Enums"]["order_status"]
          total_amount: number
          updated_at: string
          user_id: string | null
        }
        Insert: {
          address: string
          created_at?: string
          customer_name: string
          customer_phone: string
          delivery_fee?: number | null
          id?: string
          notes?: string | null
          order_number: string
          payment_method?: string | null
          region: string
          status?: Database["public"]["Enums"]["order_status"]
          total_amount?: number
          updated_at?: string
          user_id?: string | null
        }
        Update: {
          address?: string
          created_at?: string
          customer_name?: string
          customer_phone?: string
          delivery_fee?: number | null
          id?: string
          notes?: string | null
          order_number?: string
          payment_method?: string | null
          region?: string
          status?: Database["public"]["Enums"]["order_status"]
          total_amount?: number
          updated_at?: string
          user_id?: string | null
        }
        Relationships: []
      }
      product_categories: {
        Row: {
          created_at: string
          icon: string | null
          id: string
          name: string
          slug: string
        }
        Insert: {
          created_at?: string
          icon?: string | null
          id?: string
          name: string
          slug: string
        }
        Update: {
          created_at?: string
          icon?: string | null
          id?: string
          name?: string
          slug?: string
        }
        Relationships: []
      }
      products: {
        Row: {
          category_id: string | null
          created_at: string
          currency: string
          description: string | null
          id: string
          image_url: string | null
          in_stock: boolean | null
          is_active: boolean | null
          master_id: string | null
          master_name: string | null
          master_phone: string | null
          name: string
          price: number
          region: string | null
          stock_quantity: number | null
          updated_at: string
          views_count: number | null
        }
        Insert: {
          category_id?: string | null
          created_at?: string
          currency?: string
          description?: string | null
          id?: string
          image_url?: string | null
          in_stock?: boolean | null
          is_active?: boolean | null
          master_id?: string | null
          master_name?: string | null
          master_phone?: string | null
          name: string
          price?: number
          region?: string | null
          stock_quantity?: number | null
          updated_at?: string
          views_count?: number | null
        }
        Update: {
          category_id?: string | null
          created_at?: string
          currency?: string
          description?: string | null
          id?: string
          image_url?: string | null
          in_stock?: boolean | null
          is_active?: boolean | null
          master_id?: string | null
          master_name?: string | null
          master_phone?: string | null
          name?: string
          price?: number
          region?: string | null
          stock_quantity?: number | null
          updated_at?: string
          views_count?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "products_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "product_categories"
            referencedColumns: ["id"]
          },
        ]
      }
      profiles: {
        Row: {
          avatar_url: string | null
          bio: string | null
          created_at: string
          direction: string | null
          district: string | null
          education_place: string | null
          education_type: Database["public"]["Enums"]["education_type"] | null
          email: string | null
          father_name: string | null
          first_name: string | null
          id: string
          instrument: string | null
          last_name: string | null
          phone: string | null
          region: string | null
          updated_at: string
        }
        Insert: {
          avatar_url?: string | null
          bio?: string | null
          created_at?: string
          direction?: string | null
          district?: string | null
          education_place?: string | null
          education_type?: Database["public"]["Enums"]["education_type"] | null
          email?: string | null
          father_name?: string | null
          first_name?: string | null
          id: string
          instrument?: string | null
          last_name?: string | null
          phone?: string | null
          region?: string | null
          updated_at?: string
        }
        Update: {
          avatar_url?: string | null
          bio?: string | null
          created_at?: string
          direction?: string | null
          district?: string | null
          education_place?: string | null
          education_type?: Database["public"]["Enums"]["education_type"] | null
          email?: string | null
          father_name?: string | null
          first_name?: string | null
          id?: string
          instrument?: string | null
          last_name?: string | null
          phone?: string | null
          region?: string | null
          updated_at?: string
        }
        Relationships: []
      }
      reel_likes: {
        Row: {
          created_at: string
          reel_id: string
          user_id: string
        }
        Insert: {
          created_at?: string
          reel_id: string
          user_id: string
        }
        Update: {
          created_at?: string
          reel_id?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "reel_likes_reel_id_fkey"
            columns: ["reel_id"]
            isOneToOne: false
            referencedRelation: "reels"
            referencedColumns: ["id"]
          },
        ]
      }
      reels: {
        Row: {
          category: string | null
          created_at: string
          description: string | null
          duration_seconds: number | null
          id: string
          is_blocked: boolean | null
          likes_count: number | null
          thumbnail_url: string | null
          title: string
          user_id: string
          video_url: string
          views_count: number | null
        }
        Insert: {
          category?: string | null
          created_at?: string
          description?: string | null
          duration_seconds?: number | null
          id?: string
          is_blocked?: boolean | null
          likes_count?: number | null
          thumbnail_url?: string | null
          title: string
          user_id: string
          video_url: string
          views_count?: number | null
        }
        Update: {
          category?: string | null
          created_at?: string
          description?: string | null
          duration_seconds?: number | null
          id?: string
          is_blocked?: boolean | null
          likes_count?: number | null
          thumbnail_url?: string | null
          title?: string
          user_id?: string
          video_url?: string
          views_count?: number | null
        }
        Relationships: []
      }
      user_roles: {
        Row: {
          created_at: string
          id: string
          role: Database["public"]["Enums"]["app_role"]
          user_id: string
        }
        Insert: {
          created_at?: string
          id?: string
          role: Database["public"]["Enums"]["app_role"]
          user_id: string
        }
        Update: {
          created_at?: string
          id?: string
          role?: Database["public"]["Enums"]["app_role"]
          user_id?: string
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      has_role: {
        Args: {
          _role: Database["public"]["Enums"]["app_role"]
          _user_id: string
        }
        Returns: boolean
      }
    }
    Enums: {
      app_role: "admin" | "moderator" | "user"
      competition_status: "upcoming" | "open" | "in_progress" | "finished"
      education_type: "oliy" | "professional" | "bmsm" | "maktab" | "mustaqil"
      order_status: "new" | "confirmed" | "shipping" | "delivered" | "cancelled"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      app_role: ["admin", "moderator", "user"],
      competition_status: ["upcoming", "open", "in_progress", "finished"],
      education_type: ["oliy", "professional", "bmsm", "maktab", "mustaqil"],
      order_status: ["new", "confirmed", "shipping", "delivered", "cancelled"],
    },
  },
} as const
