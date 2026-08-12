-- ============================================
-- TABLE passion_feedback — questionnaire « Raconte-moi ta pâtisserie »
-- (recherche désir profond + verbatims, diffusé dans les communautés WhatsApp)
-- ============================================
-- À lancer UNE fois dans Supabase > SQL Editor > New query.
-- Le formulaire (questionnaire-passion-patisserie.html) écrit ici à chaque réponse.
-- Le dashboard (questionnaire-passion-patisserie-resultats.html) lit ici pour l'analyse.
--
-- Sécurité : on autorise INSERT + SELECT + DELETE via la clé publishable
-- (même posture que mfp_feedback et le dashboard webinaires).
-- ⚠️ Le lien du formulaire est public (la clé est dans son code source) :
-- quelqu'un qui récupère la clé pourrait lire ou effacer les réponses.
-- Risque faible vu l'audience, durcissement possible plus tard via Supabase Auth.
-- ============================================

create table if not exists public.passion_feedback (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  anciennete    text,  -- depuis combien de temps elle pâtisse
  importance    text,  -- pourquoi la pâtisserie est importante pour elle (or)
  pire_ratage   text,  -- le pire ratage + ce qu'elle s'est dit dans sa tête (or)
  phrase_revee  text,  -- LA phrase qu'elle rêve d'entendre (désir profond en scène) (or)
  phrase_recue  text,  -- la phrase de l'entourage restée en travers (facultatif)
  si_reussite   text,  -- ce que la maîtrise totale changerait (or)
  prenom        text,  -- facultatif
  contact       text   -- @ Instagram ou téléphone si ok pour creuser en DM (facultatif)
);

create index if not exists idx_passion_feedback_created_at on public.passion_feedback(created_at desc);

-- ===== Row Level Security =====
alter table public.passion_feedback enable row level security;

-- Insertion ouverte (le formulaire public écrit avec la clé publishable)
drop policy if exists "passion_feedback_insert" on public.passion_feedback;
create policy "passion_feedback_insert" on public.passion_feedback
  for insert with check (true);

-- Lecture ouverte (le dashboard lit avec la clé publishable, UI protégée par mot de passe)
drop policy if exists "passion_feedback_select" on public.passion_feedback;
create policy "passion_feedback_select" on public.passion_feedback
  for select using (true);

-- Suppression ouverte (boutons « Supprimer » et « Réinitialiser » du dashboard)
drop policy if exists "passion_feedback_delete" on public.passion_feedback;
create policy "passion_feedback_delete" on public.passion_feedback
  for delete using (true);

-- Pas de policy UPDATE = personne ne peut modifier une réponse via la clé publique.

-- ============================================
-- DONE — vérifie dans Table Editor que la table passion_feedback est créée.
-- ============================================
