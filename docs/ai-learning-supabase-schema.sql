-- AI 학습 탭 Supabase 스키마 (선택적 적용)
-- 현재 MVP는 user_state.data.ai_learning 서브트리만 동기화한다.
-- 본 SQL은 정식 분리 저장으로 마이그레이션할 때 사용한다.
-- RLS는 user_id = auth.uid() 정책으로 모두 보호.

-- 학습 세션 (하루 1~N건)
create table if not exists public.learning_sessions (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  subject     text not null,             -- 'civil' 등
  chapter_code text not null,            -- 'M02', 'B03' 등
  section_key text,                      -- 'full' | 'ch10' | 'L2' 등
  started_at  timestamptz not null default now(),
  ended_at    timestamptz,
  msg_count   int not null default 0,
  summary     text,                      -- AI가 세션 종료 시 생성
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index if not exists idx_sessions_user_date on public.learning_sessions(user_id, started_at desc);
alter table public.learning_sessions enable row level security;
create policy "own-sessions" on public.learning_sessions
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- 대화 메시지 (날짜별 인덱스 = 사용자 검색용)
create table if not exists public.conversations (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  session_id  uuid references public.learning_sessions(id) on delete cascade,
  date        date not null,             -- YYYY-MM-DD (사용자 로컬 기준)
  role        text not null check (role in ('system','user','assistant')),
  content     jsonb not null,            -- {text, refs?, attachments?} 구조
  token_count int,                       -- 알면 채워 둠
  created_at  timestamptz not null default now()
);
create index if not exists idx_conv_user_date on public.conversations(user_id, date desc);
create index if not exists idx_conv_session   on public.conversations(session_id);
alter table public.conversations enable row level security;
create policy "own-conversations" on public.conversations
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- 단원 단위 숙련도 (user × subject × code 1행)
create table if not exists public.chapter_mastery (
  user_id      uuid not null references auth.users(id) on delete cascade,
  subject      text not null,
  chapter_code text not null,
  coverage     real not null default 0,  -- 학습 깊이 0~1
  accuracy     real not null default 0,  -- 문제 정확도 0~1
  status       text not null default 'not_started', -- not_started | in_progress | mastered
  last_studied timestamptz,
  next_review  timestamptz,              -- SRS 자동 복습 예정
  updated_at   timestamptz not null default now(),
  primary key (user_id, subject, chapter_code)
);
alter table public.chapter_mastery enable row level security;
create policy "own-mastery" on public.chapter_mastery
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- AI 평가 로그 (세션 종료 시 1건)
create table if not exists public.ai_assessments (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references auth.users(id) on delete cascade,
  session_id   uuid references public.learning_sessions(id) on delete cascade,
  subject      text not null,
  chapter_code text not null,
  score        int,                      -- 0~100
  comments     text,
  next_topic   jsonb,                    -- {code, section_key, reason}
  created_at   timestamptz not null default now()
);
create index if not exists idx_assess_user on public.ai_assessments(user_id, created_at desc);
alter table public.ai_assessments enable row level security;
create policy "own-assessments" on public.ai_assessments
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
