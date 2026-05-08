-- Fix function search_path
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY INVOKER SET search_path = public
AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$;

-- Revoke public/authenticated EXECUTE on SECURITY DEFINER functions
REVOKE ALL ON FUNCTION public.has_role(UUID, public.app_role) FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.has_role(UUID, public.app_role) TO authenticated;
-- Note: has_role used inside RLS runs as the policy evaluator; granting to authenticated for direct calls is fine
-- handle_new_user runs only via trigger
REVOKE ALL ON FUNCTION public.handle_new_user() FROM PUBLIC, anon, authenticated;

-- Restrict order creation to authenticated users
DROP POLICY IF EXISTS "Anyone create order" ON public.orders;
CREATE POLICY "Authenticated create own order" ON public.orders FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL AND (user_id IS NULL OR user_id = auth.uid()));

DROP POLICY IF EXISTS "Anyone insert order items" ON public.order_items;
CREATE POLICY "Insert items for own order" ON public.order_items FOR INSERT WITH CHECK (
  EXISTS(SELECT 1 FROM public.orders o WHERE o.id = order_id AND o.user_id = auth.uid())
);