#!/usr/bin/env python3
"""Add the anti-rate section to recettes-geoffrey.json based on Guide Anti raté PDF (122 pages)."""
import json
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "data" / "recettes-geoffrey.json"

with JSON_PATH.open() as f:
    data = json.load(f)

data["anti-rate"] = {
    "description": "Diagnostic anti-ratés de Geoffrey : pour chaque grand classique de la pâtisserie, les raisons qui font rater + les solutions qui sauvent. Tiré du Guide Anti-ratés (11 chapitres, 60+ problèmes).",
    "regles-dor": {
        "titre": "Les 5 règles d'or de Geoffrey",
        "regles": [
            {
                "numero": 1,
                "nom": "Lis la recette en entier avant de commencer",
                "detail": "Avant de sortir le moindre ingrédient, lis la recette du début à la fin. Comprends chaque étape, repère les temps de repos, anticipe les étapes qui demandent du matériel spécifique. 90% des ratés viennent d'une lecture approximative."
            },
            {
                "numero": 2,
                "nom": "Pèse TOUT au gramme près",
                "detail": "La pâtisserie n'est pas la cuisine. Jamais au volume (cuillères, tasses), toujours au poids. Même l'eau, même les oeufs. Une balance au 0,1g pour les petites quantités (gélatine, levure)."
            },
            {
                "numero": 3,
                "nom": "Respecte la précision : matériel + températures",
                "detail": "Un bon thermomètre, des moules aux bonnes dimensions, les bons embouts de douille. Les températures (frigo, four, émulsions) ne sont pas des suggestions — ce sont des règles physiques."
            },
            {
                "numero": 4,
                "nom": "Respecte les temps de repos",
                "detail": "30 min au frigo, ce n'est pas 15. Une nuit, ce n'est pas 3h. Les temps de repos servent à hydrater, relâcher le gluten, cristalliser, mûrir les arômes. Zapper un repos = zapper la réussite."
            },
            {
                "numero": 5,
                "nom": "Sois curieux : comprends le pourquoi",
                "detail": "Ne te contente pas de suivre. Demande-toi pourquoi on fait fondre le chocolat à 35°C, pourquoi on tape la plaque des macarons, pourquoi la crème doit être froide. Quand tu comprends, tu ne rates plus."
            }
        ]
    },
    "pates-a-tarte": {
        "titre": "Pâtes à tarte (sucrée, sablée, sucrée au beurre)",
        "problemes": [
            {
                "probleme": "Des morceaux de beurre ne s'amalgament pas",
                "raisons": ["Beurre trop froid", "Sablage pas assez poussé"],
                "solutions": ["Beurre en pommade (souple, pas fondu)", "Sable la pâte jusqu'à obtenir une texture façon sable fin, sans morceau visible"]
            },
            {
                "probleme": "La pâte est difficile à étaler, elle colle",
                "raisons": ["Pas assez de repos au frigo", "Pâte trop chaude"],
                "solutions": ["Repos minimum 1h au frigo, idéalement toute une nuit", "Étale entre deux feuilles guitare ou papier cuisson", "Travaille vite sur un plan de travail froid"]
            },
            {
                "probleme": "La pâte se casse à l'étalage",
                "raisons": ["Pâte trop froide / mal travaillée"],
                "solutions": ["Sors la pâte 5-10 min avant de l'étaler", "Malaxe légèrement pour l'assouplir (sans chauffer)"]
            },
            {
                "probleme": "La pâte rétrécit à la cuisson",
                "raisons": ["Gluten trop développé (pâte trop travaillée)", "Pas assez de repos avant cuisson"],
                "solutions": ["Mélange le minimum — fraise une seule fois", "Repose la pâte foncée dans le moule 30 min au frigo avant cuisson"]
            },
            {
                "probleme": "Le fond de tarte gonfle à la cuisson",
                "raisons": ["Pas de trous (piquage)", "Pas de cuisson à blanc avec des poids"],
                "solutions": ["Pique le fond à la fourchette ou avec un rouleau pic-vite", "Cuisson à blanc avec billes de céramique, riz ou haricots secs"]
            },
            {
                "probleme": "Les bords s'affaissent à la cuisson",
                "raisons": ["Fonçage pas assez serré contre le cercle", "Pâte pas assez ferme au moment de la cuisson"],
                "solutions": ["Serre bien la pâte contre les parois (pas de pli d'air)", "Congèle le fond foncé 15 min avant d'enfourner"]
            }
        ]
    },
    "pate-a-choux": {
        "titre": "Pâte à choux",
        "problemes": [
            {
                "probleme": "La pâte est trop liquide",
                "raisons": ["Trop d'oeufs incorporés", "Panade pas assez desséchée"],
                "solutions": ["Dessèche bien la panade (film gras au fond de la casserole)", "Incorpore les oeufs progressivement et vérifie la texture en continu : la pâte doit former un 'V' à la spatule"]
            },
            {
                "probleme": "La pâte est trop ferme",
                "raisons": ["Pas assez d'oeufs", "Évaporation trop forte pendant le dessèchement"],
                "solutions": ["Ajoute 1 oeuf supplémentaire légèrement battu, progressivement", "La texture parfaite : ruban épais qui forme un bec"]
            },
            {
                "probleme": "Les choux ne gonflent pas",
                "raisons": ["Four pas assez chaud au démarrage", "Ouverture du four pendant la cuisson", "Pâte trop liquide"],
                "solutions": ["Enfourne dans un four à 250°C puis descends immédiatement à 170°C (choc thermique)", "N'ouvre JAMAIS le four pendant les 20 premières minutes", "Respecte la texture idéale de la pâte"]
            },
            {
                "probleme": "Les choux dégonflent à la sortie du four",
                "raisons": ["Sortie trop tôt (pas assez cuits)", "Choc thermique à la sortie"],
                "solutions": ["Les choux doivent être bien dorés et légers quand tu les prends en main", "Laisse refroidir progressivement, porte du four entrouverte 5 min avant de les sortir"]
            },
            {
                "probleme": "Les choux craquent sur le dessus",
                "raisons": ["Pochage irrégulier", "Croûtage insuffisant / craquelin absent"],
                "solutions": ["Poche régulièrement, lisse la pointe avec un doigt mouillé", "Pose un disque de craquelin sur chaque chou : répartit la poussée et donne une surface parfaite"]
            }
        ]
    },
    "biscuits-cakes": {
        "titre": "Biscuits et cakes",
        "problemes": [
            {
                "probleme": "Le biscuit ne gonfle pas uniformément",
                "raisons": ["Mélange non homogène (blancs, farine ou beurre fondu mal incorporés)"],
                "solutions": ["Mélange soigneusement pour une incorporation parfaite : pas de mottes de farine, pas de traces de beurre, blancs bien intégrés"]
            },
            {
                "probleme": "La génoise ne foisonne pas au bain-marie",
                "raisons": ["Les oeufs ont commencé à cuire (micro-grumeaux invisibles)"],
                "solutions": ["Mélange en continu pendant toute la durée du bain-marie", "Ne dépasse jamais 50°C", "Retire du bain-marie dès que le mélange est tiède-chaud et commence à mousser"]
            },
            {
                "probleme": "Impossible de démouler le biscuit",
                "raisons": ["Moule mal graissé", "Biscuit pas assez cuit", "Cuit sur papier sulfurisé / tapis silicone"],
                "solutions": ["Graissage impeccable : beurre + farine, spray graissant, ou chemisage papier", "Ajoute 1-2 min de cuisson : bords qui se rétractent, dessus qui rebondit", "Pose la feuille (avec biscuit) sur une grille froide pendant 5 min : la vapeur s'échappe et la feuille se détache toute seule"]
            }
        ]
    },
    "macarons": {
        "titre": "Macarons",
        "problemes": [
            {
                "probleme": "Les macarons craquent à la cuisson",
                "raisons": ["Étape du croûtage zappée", "Four trop humide"],
                "solutions": ["Laisse croûter jusqu'à ce que la surface soit mate et ne colle plus au doigt (20 min à 1h)", "Cale la porte du four avec un manche de cuillère en bois, ou intercale une spatule en métal pour laisser l'humidité s'échapper"]
            },
            {
                "probleme": "Les macarons sont granuleux",
                "raisons": ["Poudres pas assez mixées et/ou tamisées"],
                "solutions": ["Mixe poudre d'amande + sucre glace par petites pulsations (évite de faire sortir l'huile)", "Tamise soigneusement, sans forcer — jette les grains trop gros", "Objectif : un tant-pour-tant aussi fin que du talc"]
            },
            {
                "probleme": "Les macarons ont une pointe",
                "raisons": ["Pas assez macaronné : l'appareil est trop épais"],
                "solutions": ["Macaronne jusqu'à obtenir un ruban souple et brillant : il forme un ruban continu, retombe en coulant doucement, se réabsorbe en quelques secondes, la surface se lisse toute seule"]
            },
            {
                "probleme": "Les macarons sont en forme de dôme",
                "raisons": ["La plaque n'a pas été tapée après pochage"],
                "solutions": ["Soulève la plaque de quelques cm, laisse-la retomber fermement. Répète 2-3 fois. Les coques s'aplatissent, deviennent lisses, perdent leurs bulles d'air"]
            },
            {
                "probleme": "Les macarons sont tout plats",
                "raisons": ["Tapé trop fort sur la plaque", "Trop macaronné (appareil trop liquide)", "Recette pas équilibrée", "Blancs pas assez montés"],
                "solutions": ["Tape fermement mais raisonnablement", "Macaronne jusqu'au ruban, pas au-delà — le ruban doit retomber mais la pâte doit garder une légère tenue", "Utilise une recette testée et fiable", "Monte les blancs jusqu'au bec d'oiseau ferme"]
            },
            {
                "probleme": "Les macarons n'ont pas de collerette",
                "raisons": ["Blancs pas assez montés", "Blancs trop frais ou trop froids", "Collerette a cuit trop tôt (chaleur trop forte par le bas)"],
                "solutions": ["Monte les blancs jusqu'au bec d'oiseau ferme : brillants, fermes, forment un joli pic qui se tient", "Utilise des blancs vieillis (2-3 jours) et à température ambiante", "Cuis sur double plaque pour ralentir la chaleur du bas"]
            },
            {
                "probleme": "Les macarons sont secs",
                "raisons": ["Trop cuits", "Trop frais (juste cuits, pas maturés)"],
                "solutions": ["Raccourcis la cuisson de 1 à 2 min", "Retire la feuille de cuisson de la plaque chaude dès la sortie du four (la chaleur résiduelle continue de sécher)", "Laisse maturer 24h au frigo : la garniture hydrate la coque de l'intérieur", "Sors les macarons au moins 10 min avant dégustation"]
            }
        ]
    },
    "caramel": {
        "titre": "Caramel",
        "problemes": [
            {
                "probleme": "Le sucre masse (recristallise)",
                "raisons": ["Récipient pas parfaitement propre (gras, résidus)", "Récipient diffuse mal la chaleur", "Sucre contient des impuretés", "Sucre a subi un choc (remué, éclaboussures)"],
                "solutions": ["Travaille dans un récipient impeccable (dégraisse avec vinaigre blanc)", "Casserole à fond épais, idéalement double fond ou cuivre", "Écume les impuretés qui remontent", "NE TOUILLE PAS — fais tourner la casserole sur elle-même, pas de spatule"]
            },
            {
                "probleme": "Le caramel au beurre tranche",
                "raisons": ["Beurre ajouté trop froid (caramel trop froid à ce moment-là)"],
                "solutions": ["Ajoute le beurre entre 60°C et 70°C — zone parfaite d'émulsion", "Rattrapage : retire du feu, réchauffe légèrement, fouette énergiquement"]
            }
        ],
        "astuce-cle": {
            "titre": "Astuce glucose : évite le massage",
            "detail": "Ajoute jusqu'à 10% du poids total de sucre en sirop de glucose (ex : 200g sucre → 20g glucose). Anti-cristallisant naturel : empêche le sucre de recristalliser, stabilise la cuisson, caramel parfaitement lisse. Idéal débutants et pros."
        }
    },
    "ganaches-cremes": {
        "titre": "Ganaches et crèmes",
        "problemes": [
            {
                "probleme": "La ganache a des bulles",
                "raisons": ["Mélangé trop vite / trop fort avec un fouet"],
                "solutions": ["Utilise une spatule ou maryse, pas de fouet", "Mélange du centre vers l'extérieur, gestes circulaires et réguliers", "Passe à la passette / chinois fin après la préparation"]
            },
            {
                "probleme": "La ganache n'est pas lisse sur la tarte",
                "raisons": ["Coulée trop froide (déjà cristallisée)"],
                "solutions": ["Détends la ganache juste avant de la couler : 10-20s au micro-ondes en mélangeant, ou bain-marie court", "Elle doit être fluide, brillante et tiède, pas chaude"]
            },
            {
                "probleme": "La ganache n'est pas brillante (terne)",
                "raisons": ["Cristallisation trop brutale (mise au frigo trop vite)"],
                "solutions": ["Laisse cristalliser à température ambiante d'abord, jusqu'à ce que la ganache soit prise", "Ensuite seulement, place au frais si besoin. Cristallisation lente = ganache brillante"]
            },
            {
                "probleme": "La ganache est cassante",
                "raisons": ["Trop de chocolat (ou cacao trop puissant)"],
                "solutions": ["Rééquilibre le ratio : augmente la crème (+20%) ou réduis le chocolat (-10%)", "Objectif : souple, fondante, crémeuse, mais qui tient parfaitement à la coupe"]
            },
            {
                "probleme": "La ganache a tranché",
                "raisons": ["Crème et chocolat pas à la bonne température", "Mélange trop énergique", "Crème trop chaude (bouillante) ou chocolat trop chaud"],
                "solutions": ["Crème : chaude mais pas brûlante — juste frémissante", "Chocolat : juste fondu, idéalement autour de 35°C", "Rattrapage : attends que la ganache revienne à 35°C, puis mixe quelques secondes au Thermomix / Companion — l'émulsion se reforme"]
            },
            {
                "probleme": "La crème à base d'oeufs a des grains",
                "raisons": ["Oeufs trop chauffés (coagulation)"],
                "solutions": ["Cuis à feu doux en permanence", "Mélange en continu (ne lâche jamais la maryse / fouet)", "Bain-marie pour les appareils sensibles (lemon curd, flan, crème anglaise)", "Stoppe la cuisson immédiatement : verse dans un récipient froid dès que c'est cuit (nappe la spatule)"]
            },
            {
                "probleme": "Le flan déborde à la cuisson",
                "raisons": ["Pas assez attendu avant d'enfourner (crème pas croûtée)", "Trop rempli le fond de pâte", "Four trop chaud"],
                "solutions": ["Laisse l'appareil à flan reposer 2-4h au frais jusqu'à ce que la surface soit légèrement sèche", "Laisse 1 à 2 cm entre le haut du cercle et le niveau de la crème", "Cuis à 150°C à 170°C selon l'épaisseur"]
            },
            {
                "probleme": "La crème d'amande a tranché",
                "raisons": ["Beurre trop froid", "Oeufs trop froids (figent le beurre)"],
                "solutions": ["Beurre pommade : souple, crémeux, pas fondu, s'écrase facilement au doigt", "Oeufs à température ambiante : sors-les 1h avant, ou plonge 5 min dans eau tiède", "Mélange en douceur, pas de mousse"]
            },
            {
                "probleme": "La crème d'amande déborde à la cuisson",
                "raisons": ["Foisonnée (trop d'air incorporé)", "Fond de tarte trop rempli"],
                "solutions": ["Travaille-la comme un simple mélange, pas une mousse", "Laisse 5 à 8 mm de marge sous le bord du cercle (surtout tartes bourdaloue)"]
            }
        ]
    },
    "mousses-meringues": {
        "titre": "Mousses et meringues",
        "problemes": [
            {
                "probleme": "La chantilly ou ganache montée a tranché",
                "raisons": ["Fouetté trop vite", "Fouetté trop longtemps", "Crème pas assez froide (ou cuisine trop chaude)"],
                "solutions": ["Monte à petite vitesse : plus lent mais émulsion stable", "Arrête au bec d'oiseau net pour chantilly, encore plus tôt pour ganache montée d'entremets (souple, brillante, ruban épais)", "Crème entre 2°C et 4°C, bol et fouet froids (5 min au congélateur)"]
            },
            {
                "probleme": "La chantilly ou ganache montée ne monte pas",
                "raisons": ["Trop de crème chauffée", "Crème ou cuisine trop chaude", "Pas assez de matière grasse (crème <30% MG)"],
                "solutions": ["Ne chauffe qu'une petite partie de la crème (juste pour dissoudre / infuser)", "Garde la crème au frigo jusqu'à la dernière seconde — bol + fouet 10 min au congélateur", "Utilise une crème entière minimum 30% MG — crème fleurette 30-35% ou UHT de qualité"]
            },
            {
                "probleme": "Les blancs d'oeuf montés retombent",
                "raisons": ["Montés trop vite (grosses bulles instables)", "Montés trop longtemps (graineux, secs, cassants)"],
                "solutions": ["Monte à petite vitesse : bulles fines, régulières, stables", "Arrête au bec d'oiseau : souple pour appareils délicats, ferme pour meringue — jamais plus"]
            },
            {
                "probleme": "Les blancs d'oeuf ne montent pas",
                "raisons": ["Récipient pas propre (trace de gras)", "Blancs pas purs (trace de jaune)", "Oeufs de mauvaise qualité (pauvres en albumine)"],
                "solutions": ["Récipient propre et dégraissé (vinaigre blanc → magique)", "Sépare les oeufs soigneusement — si une goutte de jaune tombe, recommence", "Utilise des oeufs plein air ou bio (en coquille ou en bidon, la qualité compte)"]
            },
            {
                "probleme": "La mousse au chocolat n'est pas homogène",
                "raisons": ["Blancs trop montés (trop fermes, cassants → blocs)", "Chocolat trop froid (cristallise d'un coup → paillettes)"],
                "solutions": ["Monte au bec d'oiseau : fermes, brillants, qui se tiennent, mais pas granuleux", "Chocolat fluide, lisse, tiède à 35-40°C"]
            },
            {
                "probleme": "Il y a de l'eau au fond de la mousse",
                "raisons": ["Blancs trop fouettés (granuleux, cassants → libèrent l'eau)", "Chocolat trop chaud (explose les bulles d'air → libère l'eau)"],
                "solutions": ["Monte doucement, arrête au bec d'oiseau, jamais plus", "Chocolat toujours tiède (35-40°C)", "Méthode : mélange une petite portion de blancs dans le chocolat pour le détendre, puis incorpore délicatement au reste"]
            },
            {
                "probleme": "La mousse d'entremets a des bulles au démoulage",
                "raisons": ["Mousse trop montée (emprisonne les bulles)", "Bords du moule pas lissés"],
                "solutions": ["Monte jusqu'au bec d'oiseau très souple, presque tremblotant — la tenue vient du congélateur, pas du fouet", "Après la première couche dans le moule, presse et lisse contre les rebords avec une spatule coudée, fais tout le tour, puis continue le montage"]
            },
            {
                "probleme": "La crème mousseline est granuleuse",
                "raisons": ["Ingrédients pas à la même température (beurre froid → paillettes)"],
                "solutions": ["Tout à la même température, même consistance, souple", "Rattrapage : fouette à vitesse élevée + chauffe légèrement la cuve avec chalumeau ou décapeur thermique. Dès que les paillettes fondent → texture redevient lisse. Attention : juste ce qu'il faut, pas plus (sinon beurre fondu = mousseline détruite)"]
            }
        ]
    },
    "entremets": {
        "titre": "Entremets",
        "problemes": [
            {
                "probleme": "L'entremets se casse la figure à la décongélation",
                "raisons": ["Mousse pas assez foisonnée (trop liquide au coulage)", "Mousse manque de structure (pas assez de chocolat / gélatine)", "Insert trop liquide (se déplace, brise la mousse)", "Entremets mal équilibré (lourd sur léger)"],
                "solutions": ["Monte la mousse jusqu'à un ruban dense ou bec d'oiseau souple — pas trop ferme, clairement pas liquide", "Vérifie scrupuleusement les quantités de gélatine ou chocolat dans la recette", "Insert bien gélifié, complètement congelé avant montage, suffisamment ferme pour rester en place", "Respecte la règle d'or : LE DENSE ET LE LOURD EN BAS (brownie, biscuit moelleux, praliné croustillant), LE LÉGER ET L'AÉRIEN AU-DESSUS (mousses, ganache montée, chantilly). Jamais l'inverse"]
            },
            {
                "probleme": "La gelée ou le confit coule, rend de l'eau",
                "raisons": ["Insert pas assez gélifié (fruits riches en eau : framboise, fraise, mangue, agrumes)", "Insert a pris le givre au congélateur"],
                "solutions": ["Insert souple mais ferme : se tient au couteau, ne coule pas, ne bave pas, ne rend pas d'eau", "Augmente légèrement la gélatine, cuis un peu plus longtemps la purée (évaporer), ou ajoute du sucre (retient l'humidité)", "Vérifie l'absence de givre avant montage : sèche délicatement ou refais l'insert si trop givré"]
            }
        ]
    },
    "glacages": {
        "titre": "Glaçages miroir",
        "problemes": [
            {
                "probleme": "Le glaçage coule ou se déchire",
                "raisons": ["Pas assez gélifié (recette déséquilibrée)", "Entremets givré au moment du glaçage"],
                "solutions": ["Utilise une recette fiable : chocolat/cacao + sucre + crème + eau + gélatine en proportions testées", "Un bon glaçage est fluide mais nappant, sans être trop liquide", "Pas de givre sur l'entremets : retire-le délicatement au doigt ou au pinceau sec, glace immédiatement après"]
            },
            {
                "probleme": "Le glaçage miroir est terne",
                "raisons": ["Trop chauffé (>40°C)", "Entremets remis au congélateur après glaçage"],
                "solutions": ["Jamais au-dessus de 40°C : zone idéale 35°C-37°C. Au-delà, perte de brillance irréversible", "Règle d'or : Glacé → frigo → dégusté. JAMAIS au congélateur une fois glacé (casse la structure, rend terne, granuleux ou cassant)"]
            },
            {
                "probleme": "La couche de glaçage est trop épaisse",
                "raisons": ["Glaçage trop froid (<31°C, fige instantanément)", "Forme de l'entremets retient trop (creux, cuvettes, angles prononcés)"],
                "solutions": ["Utilise le glaçage à 31-35°C : 35°C = fluide, 31°C = glaçages denses. En dessous = catastrophe", "Astuce de chef : couler en UN SEUL mouvement continu, ne jamais repasser deux fois", "Ou change de finition : flocage, velours, spray cacao, pochage décoratif"]
            },
            {
                "probleme": "Le glaçage fait des coulures",
                "raisons": ["Trop froid au moment de l'application"],
                "solutions": ["Verse à 31°C-35°C, jamais en dessous :", "< 31°C → figement instantané, coulures assurées", "31°C à 33°C → parfait pour glaçages épais", "33°C à 35°C → idéal pour nappage fluide"]
            },
            {
                "probleme": "Le glaçage ne marque pas l'arête de l'entremets",
                "raisons": ["Glaçage trop chaud (>35°C, glisse trop)", "Arête trop vive / saillante (ne retient pas le glaçage)"],
                "solutions": ["Travaille à 35°C max — en dessous il nappe, au-dessus il glisse", "Adoucis l'arête avant de glacer : passe un doigt ganté ou la paume dessus, arrondis très légèrement l'angle"]
            },
            {
                "probleme": "Le glaçage fait des bulles",
                "raisons": ["Mixeur plongeant pas performant (incorpore de l'air)", "Glaçage trop froid au mixage (trop épais, emprisonne l'air)"],
                "solutions": ["Investis dans un bon mixeur (Bamix) : zéro bulle, émulsion parfaite", "Chauffe à 40°C (fluide parfait) → mixe en penchant légèrement le mixeur (évite d'aspirer l'air) → laisse redescendre à 31-35°C avant de glacer"]
            },
            {
                "probleme": "Le glaçage glisse de l'entremets",
                "raisons": ["Entremets givré (l'eau empêche l'adhérence)"],
                "solutions": ["Ne glace JAMAIS un entremets givré", "Laisse-le 5-10 min à l'air libre : juste assez pour que le givre fonde, pas assez pour décongeler", "Surface doit être : nette, sèche, mate", "Astuce : congèle l'entremets dans une boîte hermétique pour éviter les cristaux de glace"]
            }
        ]
    },
    "enrobages": {
        "titre": "Enrobages chocolat",
        "problemes": [
            {
                "probleme": "L'enrobage se décolle de l'entremets ou du cake",
                "raisons": ["Entremets ou cake givré au moment de l'enrobage (le givre fond → eau sous l'enrobage)"],
                "solutions": ["Sors l'entremets du congélateur, vérifie le givre (blanc = givre)", "Laisse 2 à 5 min à l'air libre pour que le givre fonde, sans commencer à décongeler", "Surface doit être : propre, mate, légèrement figée mais sèche", "Enrobe immédiatement après"]
            },
            {
                "probleme": "L'enrobage fait des coulures",
                "raisons": ["Pas assez chaud (fige trop vite, glisse mal)", "Pas assez fluide (chocolat noir naturellement plus épais)"],
                "solutions": ["Température idéale : 35°C pour biscuit / entremets frais (sorti du frigo), 35°C à 40°C pour cake congelé (la chaleur compense le froid)", "Ajoute 5% à 10% d'huile de pépins de raisin au mélange chocolat + beurre de cacao : fluidifie, améliore l'écoulement, réduit les traces, rendu ultra propre", "Huile de pépins de raisin : neutre, stable, n'altère pas le goût"]
            }
        ]
    }
}

with JSON_PATH.open("w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added anti-rate section. Top-level keys: {list(data.keys())}")
print(f"Anti-rate sub-keys: {list(data['anti-rate'].keys())}")
print(f"File size: {JSON_PATH.stat().st_size} bytes")
