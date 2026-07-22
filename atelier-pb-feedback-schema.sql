-- ============================================
-- TABLE atelier_feedback_pb — avis post-masterclass PARIS-BREST (live)
-- ============================================
-- À lancer UNE fois dans Supabase > SQL Editor > New query.
-- Le formulaire (questionnaire-atelier-paris-brest.html) écrit ici à chaque réponse.
-- Le dashboard (questionnaire-atelier-paris-brest-resultats.html) lit ici pour l'analyse.
--
-- ⚠️ Table SÉPARÉE de atelier_feedback (les avis macarons) : les deux ateliers ne se
-- mélangent jamais, chaque dashboard n'affiche que ses propres réponses.
--
-- Sécurité : INSERT + SELECT + DELETE via la clé publishable (même posture que le
-- questionnaire macarons). Le DELETE sert aux boutons « Supprimer » et « Réinitialiser ».
-- ⚠️ Le lien du formulaire est public (clé dans le code source) → autoriser le DELETE =
-- quelqu'un qui récupère la clé pourrait aussi effacer les réponses. Risque faible vu
-- l'audience ; durcissement possible plus tard via Supabase Auth.
-- ============================================

create table if not exists public.atelier_feedback_pb (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  note                int,     -- Q1 note de la masterclass (0-10)
  prefere             text,    -- Q2 ce qu'il a préféré
  amelioration        text,    -- Q3 ce qui rendrait la masterclass encore meilleure
  a_rejoint           text,    -- Q4 a intégré la MFP ? (Oui / Non)
  raison_pas_rejoint  text,    -- Q5 (si Non) raison qui l'a empêché (or = objection)
  prix_ideal          text,    -- Q6 (si Non) prix qui l'aurait fait rejoindre (or)
  oui_tout_de_suite   text,    -- Q7 (si Non) ce qui le ferait dire oui tout de suite (or)
  blocage_patisserie  text,    -- Q8 ce qui le bloque le plus en pâtisserie

  -- coordonnées — prénom + téléphone OBLIGATOIRES côté formulaire (échangés contre le
  -- « cadeau »), pour relancer chaque personne une par une.
  prenom              text,
  email               text,    -- non collecté par le formulaire, gardé pour compat
  telephone           text
);

create index if not exists idx_atelier_feedback_pb_created_at
  on public.atelier_feedback_pb(created_at desc);

-- ===== Row Level Security =====
alter table public.atelier_feedback_pb enable row level security;

drop policy if exists "atelier_feedback_pb_insert" on public.atelier_feedback_pb;
create policy "atelier_feedback_pb_insert" on public.atelier_feedback_pb
  for insert with check (true);

drop policy if exists "atelier_feedback_pb_select" on public.atelier_feedback_pb;
create policy "atelier_feedback_pb_select" on public.atelier_feedback_pb
  for select using (true);

drop policy if exists "atelier_feedback_pb_delete" on public.atelier_feedback_pb;
create policy "atelier_feedback_pb_delete" on public.atelier_feedback_pb
  for delete using (true);

-- Pas de policy UPDATE = personne ne peut modifier une réponse via la clé publique.

-- ============================================
-- DONE — vérifie dans Table Editor que la table atelier_feedback_pb est créée.
-- ============================================
