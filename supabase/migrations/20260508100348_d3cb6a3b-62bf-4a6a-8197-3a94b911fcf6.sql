-- Revoke has_role from authenticated too; RLS uses definer context
REVOKE EXECUTE ON FUNCTION public.has_role(UUID, public.app_role) FROM authenticated;

-- Restrict broad SELECT on storage to prevent listing while keeping file access
DROP POLICY IF EXISTS "Public read content buckets" ON storage.objects;
DROP POLICY IF EXISTS "Reels public read" ON storage.objects;
-- Files in these buckets are accessed by direct public URL, no need for SELECT policy on storage.objects
-- Public buckets serve files via /storage/v1/object/public/... without RLS check on metadata listing
-- We just don't add a permissive SELECT policy, so listing is denied by default while public file URLs still work