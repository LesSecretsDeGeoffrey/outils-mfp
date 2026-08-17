-- ============================================
-- TABLE demarrage_mfp — questionnaire de démarrage de La Méthode Fondations Pro
-- (rempli par le client juste après l'inscription, lu par Geoffrey avant l'appel de démarrage 45 min)
-- ============================================
-- À lancer UNE fois dans Supabase > SQL Editor > New query.
-- Le formulaire (questionnaire-demarrage-mfp.html) écrit ici à chaque envoi.
-- La page (questionnaire-demarrage-mfp-resultats.html) lit ici pour afficher les fiches.
--
-- Sécurité : INSERT + SELECT + DELETE via la clé publishable, même posture que
-- passion_feedback. La page de lecture est protégée par mot de passe côté UI.
-- ============================================

create table if not exists public.demarrage_mfp (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  prenom          text,
  telephone       text,
  anciennete      text,     -- depuis combien de temps
  frequence       text,     -- à quelle fréquence
  rates           text[],   -- ce qu'il rate le plus souvent (cases cochées)
  dernier_rate    text,     -- le dernier raté en détail (matière du diagnostic)
  reussi_une_fois text,     -- réussi une fois, jamais retrouvé (facultatif)
  four            text,     -- type de four
  four_marque     text,     -- marque et modèle (facultatif)
  materiel        text[],   -- matériel possédé (cases cochées)
  materiel_manque text,     -- ce qu'il pense devoir acheter (facultatif)
  temps           text,     -- temps par semaine
  moments         text[],   -- quand il pâtisse
  objectif        text,     -- la pièce à réussir dans 12 semaines
  evenement       text,     -- événement cible (facultatif)
  autre           text,     -- autre chose à savoir (facultatif)

  lu              boolean default false  -- coché depuis la page de lecture quand la fiche est traitée
);

create index if not exists idx_demarrage_mfp_created_at on public.demarrage_mfp(created_at desc);

alter table public.demarrage_mfp enable row level security;

drop policy if exists "demarrage_mfp_insert" on public.demarrage_mfp;
create policy "demarrage_mfp_insert" on public.demarrage_mfp
  for insert with check (true);

drop policy if exists "demarrage_mfp_select" on public.demarrage_mfp;
create policy "demarrage_mfp_select" on public.demarrage_mfp
  for select using (true);

drop policy if exists "demarrage_mfp_delete" on public.demarrage_mfp;
create policy "demarrage_mfp_delete" on public.demarrage_mfp
  for delete using (true);

-- UPDATE limité : seule la colonne « lu » est modifiée par la page de lecture (bouton « Fiche traitée »).
-- La policy autorise l'update, le front n'envoie jamais autre chose que { lu }.
drop policy if exists "demarrage_mfp_update" on public.demarrage_mfp;
create policy "demarrage_mfp_update" on public.demarrage_mfp
  for update using (true) with check (true);

-- ============================================
-- DONE — vérifie dans Table Editor que la table demarrage_mfp est créée.
-- ============================================
