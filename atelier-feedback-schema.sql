-- ============================================
-- TABLE atelier_feedback — avis post-masterclass macarons (live)
-- ============================================
-- À lancer UNE fois dans Supabase > SQL Editor > New query.
-- Le formulaire (questionnaire-atelier-macarons.html) écrit ici à chaque réponse.
-- Le dashboard (questionnaire-atelier-macarons-resultats.html) lit ici pour l'analyse.
--
-- Sécurité : INSERT + SELECT + DELETE via la clé publishable (même posture que
-- le questionnaire MFP et le dashboard webinaires). Le DELETE sert au bouton
-- « Réinitialiser » du dashboard.
-- ⚠️ Le lien du formulaire est public (clé dans le code source) → autoriser le
-- DELETE = quelqu'un qui récupère la clé pourrait aussi effacer les réponses.
-- Risque faible vu l'audience ; durcissement possible plus tard via Supabase Auth.
-- ============================================

create table if not exists public.atelier_feedback (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  note                int,     -- Q1 note de la masterclass (0-10)
  prefere             text,    -- Q2 ce qu'il a préféré
  a_rejoint           text,    -- Q3 a intégré la MFP ? (Oui / Non)
  raison_pas_rejoint  text,    -- Q4 (si Non) raison qui l'a empêché (or = objection)
  prix_ideal          text,    -- Q5 (si Non) prix qui l'aurait fait rejoindre (or)
  oui_tout_de_suite   text,    -- Q6 (si Non) ce qui le ferait dire oui tout de suite (or)
  blocage_patisserie  text,    -- Q7 ce qui le bloque le plus en pâtisserie

  -- bloc coordonnées (facultatif) — pour décrocher un call de vente post-live
  prenom              text,
  email               text,
  telephone           text
);

create index if not exists idx_atelier_feedback_created_at on public.atelier_feedback(created_at desc);

-- Si la table existait DÉJÀ (avant l'ajout du bloc coordonnées), ces 3 lignes
-- ajoutent les colonnes sans rien casser :
alter table public.atelier_feedback add column if not exists prenom text;
alter table public.atelier_feedback add column if not exists email text;
alter table public.atelier_feedback add column if not exists telephone text;

-- ===== Row Level Security =====
alter table public.atelier_feedback enable row level security;

drop policy if exists "atelier_feedback_insert" on public.atelier_feedback;
create policy "atelier_feedback_insert" on public.atelier_feedback
  for insert with check (true);

drop policy if exists "atelier_feedback_select" on public.atelier_feedback;
create policy "atelier_feedback_select" on public.atelier_feedback
  for select using (true);

drop policy if exists "atelier_feedback_delete" on public.atelier_feedback;
create policy "atelier_feedback_delete" on public.atelier_feedback
  for delete using (true);

-- Pas de policy UPDATE = personne ne peut modifier une réponse via la clé publique.

-- ============================================
-- DONE — vérifie dans Table Editor que la table atelier_feedback est créée.
-- ============================================
