-- ============================================
-- TABLE mfp_feedback — questionnaire de satisfaction des élèves MFP
-- ============================================
-- À lancer UNE fois dans Supabase > SQL Editor > New query.
-- Le formulaire (questionnaire-mfp.html) écrit ici à chaque réponse.
-- Le dashboard (questionnaire-mfp-resultats.html) lit ici pour l'analyse.
--
-- Sécurité : on autorise INSERT + SELECT via la clé publishable (la même
-- que le dashboard webinaires). On N'autorise PAS UPDATE / DELETE : comme le
-- lien du formulaire est public, personne ne peut effacer ou modifier les
-- réponses des autres avec la clé. Pour supprimer un test/spam : Table Editor.
-- ============================================

create table if not exists public.mfp_feedback (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  niveau_depart         text,    -- niveau au moment de rejoindre
  galere_avant          text,    -- plus grosse galère avant (or)
  declic                text,    -- ce qui l'a convaincu de rejoindre (or)
  arguments             text[],  -- ce qui a le plus compté, multi, max 3 (or)
  hesitation            text,    -- ce qui faisait hésiter (or)
  ce_qui_a_convaincu    text,    -- ce qui a levé l'hésitation (or)
  changement            text,    -- LE truc qui a changé (or)
  nps                   int,     -- recommandation 0-10
  manque_pour_10        text,    -- ce qui manque pour 10/10
  dirait_a_un_ami       text,    -- ce qu'il dirait à un ami (= témoignage anonyme) (or)
  ameliorations         text,    -- ce que je pourrais améliorer
  contenus_futurs       text[],  -- contenus souhaités (multi)
  contenus_futurs_autre text,    -- autre idée de contenu (facultatif)
  dernier_mot           text     -- un dernier truc
);

create index if not exists idx_mfp_feedback_created_at on public.mfp_feedback(created_at desc);

-- ===== Row Level Security =====
alter table public.mfp_feedback enable row level security;

-- Insertion ouverte (le formulaire public écrit avec la clé publishable)
drop policy if exists "mfp_feedback_insert" on public.mfp_feedback;
create policy "mfp_feedback_insert" on public.mfp_feedback
  for insert with check (true);

-- Lecture ouverte (le dashboard lit avec la clé publishable, UI protégée par mot de passe)
drop policy if exists "mfp_feedback_select" on public.mfp_feedback;
create policy "mfp_feedback_select" on public.mfp_feedback
  for select using (true);

-- Pas de policy UPDATE / DELETE = impossible d'effacer ou modifier via la clé publique.

-- ============================================
-- DONE — vérifie dans Table Editor que la table mfp_feedback est créée.
-- ============================================
