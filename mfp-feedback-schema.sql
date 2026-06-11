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

  -- Partie 1 — contexte
  anciennete            text,    -- Q1 depuis combien de temps
  niveau_depart         text,    -- Q2 niveau au moment de rejoindre

  -- Partie 2 — pourquoi tu as rejoint (le coeur)
  galere_avant          text,    -- Q3 (or) plus grosse galère avant
  declic                text,    -- Q4 (or) le déclic
  arguments             text[],  -- Q5 (or) ce qui a le plus compté (multi)
  hesitation            text,    -- Q6 (or) ce qui faisait hésiter
  ce_qui_a_convaincu    text,    -- Q7 (or) ce qui a levé l'hésitation

  -- Partie 3 — depuis que tu es dedans
  changement            text,    -- Q8 (or) LE truc qui a changé
  nps                   int,     -- Q9 recommandation 0-10
  manque_pour_10        text,    -- Q10 ce qui manque pour 10/10
  dirait_a_un_ami       text,    -- Q11 (or / témoignage) ce qu'il dirait à un ami

  -- Partie 4 — la suite
  ameliorations         text,    -- Q12 à améliorer
  contenus_futurs       text[],  -- Q13 contenus souhaités (multi)
  contenus_futurs_autre text,    -- Q13 autre (libre)
  dernier_mot           text,    -- Q14 un dernier truc

  -- Partie 5 — clôture
  consentement_temoignage text,  -- Q15 droit d'usage en témoignage
  prenom                text,    -- Q16 prénom (facultatif)
  contact               text     -- Q16 insta / contact (facultatif)
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
