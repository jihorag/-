// Supabase 클라우드 동기화 (선택). publishable 키는 클라이언트 공개용이며
// 행 단위 보안(RLS)으로 보호되므로 커밋해도 안전하다.
// env(VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY)가 있으면 우선 사용.
import { createClient } from '@supabase/supabase-js';

const URL = import.meta.env.VITE_SUPABASE_URL || 'https://crlqdphephctpurgwxqe.supabase.co';
const KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_shIb9-WGZNfJZsiOJT_2Ew_inH3y5Re';

export const cloudEnabled = !!(URL && KEY);
export const supabase = cloudEnabled
  ? createClient(URL, KEY, { auth: { persistSession: true, autoRefreshToken: true } })
  : null;

// 사용자별 상태 1행: user_state(user_id uuid pk, data jsonb, updated_at timestamptz)
export async function pullState() {
  if (!supabase) return null;
  const { data: u } = await supabase.auth.getUser();
  if (!u || !u.user) return null;
  const { data, error } = await supabase
    .from('user_state').select('data, updated_at').eq('user_id', u.user.id).maybeSingle();
  if (error) throw error;
  return data || null; // { data, updated_at } | null
}

export async function pushState(snapshot) {
  if (!supabase) return null;
  const { data: u } = await supabase.auth.getUser();
  if (!u || !u.user) throw new Error('로그인이 필요합니다.');
  const row = { user_id: u.user.id, data: snapshot, updated_at: new Date().toISOString() };
  const { error } = await supabase.from('user_state').upsert(row, { onConflict: 'user_id' });
  if (error) throw error;
  return row.updated_at;
}
