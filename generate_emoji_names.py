"""
Génère EMOJI_NAMES (emoji → nom français) et l'injecte dans data.json.
"""
import json, unicodedata, re, os

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Overrides français pour les emojis qui ont un nom technique peu lisible
# ou qui sont des séquences multi-codepoints (ZWJ, variation selectors…)
FR = {
    # ── Éléments naturels ──
    '🌊':'Vague',          '⚡':'Éclair',        '🔥':'Feu',
    '❄️':'Glace',          '🌙':'Lune',           '☀️':'Soleil',
    '🌸':'Fleur cerisier', '🌺':'Fleur',          '🌹':'Rose',
    '🌻':'Tournesol',      '🌿':'Feuille',        '🌾':'Blé',
    '🌴':'Palmier',        '🌲':'Arbre',          '🌵':'Cactus',
    '🌋':'Volcan',         '🏔️':'Montagne',       '🏝️':'Île',
    '🏜️':'Désert',         '🌑':'Lune noire',     '🌕':'Pleine lune',
    '⛅':'Nuage et soleil','☁️':'Nuage',          '🌩️':'Orage',
    '🌪️':'Tornade',        '🌫️':'Brouillard',     '💧':'Goutte',
    '💦':'Éclaboussure',   '💨':'Vent',           '☄️':'Comète',
    '🌌':'Galaxie',        '⭐':'Étoile',         '🌟':'Étoile filante',
    '✨':'Étincelles',
    # ── Corps / visages ──
    '💪':'Muscle',         '✊':'Poing',          '👊':'Coup de poing',
    '🤜':'Poing droit',    '✋':'Main',           '🤚':'Main levée',
    '👃':'Nez',            '👁️':'Œil',           '💋':'Baiser',
    '😁':'Grand sourire',  '😴':'Endormi',        '😏':'Sourire malicieux',
    '😤':'Vapeur de nez',  '😠':'Colère',         '😈':'Diable',
    '😭':'Pleurs',         '😅':'Sourire gêné',   '😍':'Amoureux',
    '😢':'Larme',          '😰':'Sueur froide',
    # ── Cœurs ──
    '❤️':'Cœur rouge',    '💙':'Cœur bleu',      '💚':'Cœur vert',
    '💛':'Cœur jaune',     '🖤':'Cœur noir',      '🤍':'Cœur blanc',
    '💜':'Cœur violet',    '🧡':'Cœur orange',    '💔':'Cœur brisé',
    '💕':'Cœurs',          '💘':'Cœur percé',     '💗':'Cœur rose',
    '🩷':'Cœur rose clair','💫':'Étoile tournante',
    # ── Armes & combat ──
    '⚔️':'Épées croisées', '🗡️':'Épée',          '🔪':'Couteau',
    '🏹':'Arc',            '🔫':'Pistolet',       '💣':'Bombe',
    '🛡️':'Bouclier',       '🪚':'Scie',
    # ── Nourriture ──
    '🍖':'Cuisse de poulet','🍶':'Saké',          '🍭':'Sucette',
    '🍬':'Bonbon',          '🍡':'Dango',         '🍰':'Gâteau',
    '🎂':'Gâteau d\'anniv', '🧁':'Cupcake',        '🍮':'Flan',
    '🍎':'Pomme rouge',     '🍊':'Orange',        '🍋':'Citron',
    '🍇':'Raisins',         '🍕':'Pizza',         '🍺':'Bière',
    '🍻':'Bières',          '🍹':'Cocktail',      '🥤':'Boisson',
    '🍼':'Biberon',         '🍱':'Bento',         '🍲':'Soupe',
    '🍳':'Poêle',           '🫕':'Casserole',     '💊':'Médicament',
    # ── Vêtements & accessoires ──
    '👒':'Chapeau de paille','🎩':'Chapeau haut-de-forme','🧢':'Casquette',
    '👔':'Chemise',         '👘':'Kimono',        '👠':'Talon haut',
    '👙':'Bikini',          '🕶️':'Lunettes de soleil','👓':'Lunettes',
    '💄':'Rouge à lèvres',  '💍':'Bague',         '💎':'Diamant',
    '💰':'Argent',          '💸':'Billet volant', '💲':'Dollar',
    # ── Animaux ──
    '🐲':'Dragon',          '🐉':'Dragon impérial','🦊':'Renard',
    '🐺':'Loup',            '🦁':'Lion',          '🐱':'Chat',
    '🐕':'Chien',           '🐟':'Poisson',       '🐠':'Poisson tropical',
    '🦈':'Requin',          '🐋':'Baleine',       '🐙':'Pieuvre',
    '🦑':'Calamar',         '🐊':'Crocodile',     '🐷':'Cochon',
    '🐰':'Lapin',           '🐻':'Ours',          '🐘':'Éléphant',
    '🦅':'Aigle',           '🦇':'Chauve-souris', '🦩':'Flamant',
    '🦢':'Cygne',           '🕊️':'Colombe',       '🦆':'Canard',
    '🐆':'Léopard',         '🦦':'Loutre',        '🐸':'Grenouille',
    '🦕':'Dinosaure',       '🦖':'T-Rex',         '🐛':'Chenille',
    '🦠':'Microbe',         '🕷️':'Araignée',      '🦋':'Papillon',
    '🐝':'Abeille',         '🪶':'Plume',          '🐾':'Empreintes',
    '🦴':'Os',              '🐍':'Serpent',       '🦗':'Grillon',
    '🦟':'Moustique',       '🐗':'Sanglier',      '🐎':'Cheval',
    '🦒':'Girafe',          '🦬':'Bison',         '🐮':'Vache',
    # ── Symboles / formes ──
    '☠️':'Tête de mort',   '💀':'Crâne',         '⚓':'Ancre',
    '⛩️':'Torii',          '🔱':'Trident',       '⚖️':'Balance',
    '🔵':'Rond bleu',       '🔴':'Rond rouge',    '🟢':'Rond vert',
    '🟡':'Rond jaune',      '🟣':'Rond violet',   '⚫':'Rond noir',
    '🔲':'Carré',           '🔹':'Losange bleu',  '🟫':'Carré marron',
    '🟠':'Rond orange',     '🟩':'Carré vert',    '🔷':'Grand losange',
    '♟️':'Pion',            '♨️':'Source chaude', '🌀':'Tourbillon',
    '⬇️':'Flèche bas',     '⬆️':'Flèche haut',  '🔄':'Cycle',
    '🔒':'Cadenas',         '🔓':'Cadenas ouvert','🔑':'Clé',
    '⏰':'Réveil',          '⏳':'Sablier',       '⏱️':'Chronomètre',
    '🔮':'Boule de cristal','🃏':'Joker',          '🎲':'Dé',
    '🏅':'Médaille',        '🏆':'Trophée',       '🎖️':'Insigne',
    '📚':'Livres',          '📖':'Livre ouvert',  '📜':'Parchemin',
    '📡':'Antenne',         '💡':'Ampoule',       '🔬':'Microscope',
    '⚗️':'Alambic',        '🧪':'Éprouvette',    '🧬':'ADN',
    '🔭':'Télescope',       '🔧':'Clé anglaise',  '⚙️':'Engrenage',
    '🔩':'Boulon',          '🪩':'Boule disco',
    # ── Lieux & structures ──
    '🏰':'Château',         '🏯':'Château japonais','🏛️':'Temple',
    '⛩️':'Sanctuaire',     '🏗️':'Construction',  '🏟️':'Stade',
    '🏠':'Maison',          '🚢':'Bateau',         '🏴':'Drapeau noir',
    '🏴‍☠️':'Drapeau pirate', '🚩':'Drapeau rouge', '🎌':'Drapeaux japonais',
    '🌍':'Globe terrestre', '🌐':'Globe réseau',   '🗺️':'Carte',
    '🏜️':'Désert aride',
    # ── Personnes & gestes ──
    '👑':'Couronne',        '👸':'Princesse',     '🤴':'Prince',
    '👴':'Vieil homme',     '👵':'Grand-mère',    '👶':'Bébé',
    '👨‍🍳':'Cuisinier',       '👩‍🎨':'Artiste',      '👮':'Policier',
    '🕵️':'Détective',       '🤸':'Acrobate',      '🏃':'Coureur',
    '🥷':'Ninja',           '🦸':'Super-héros',   '🦹':'Super-vilain',
    '👤':'Silhouette',
    # ── Sports & loisirs ──
    '⚔️':'Duel',            '🥊':'Gant de boxe',  '🤼':'Lutte',
    '🏊':'Natation',        '🤿':'Tuba',          '🏄':'Surf',
    '🎮':'Manette',         '🎭':'Masque théâtre','🎨':'Palette',
    '🖼️':'Tableau',         '🎪':'Cirque',        '🎊':'Confettis',
    '🎀':'Nœud',            '🎵':'Note de musique','🎶':'Musique',
    '🎸':'Guitare',         '🎹':'Piano',         '🎺':'Trompette',
    '🎻':'Violon',          '🥁':'Tambour',       '🔊':'Volume',
    '🎤':'Microphone',      '🎧':'Casque audio',
    # ── Autre ──
    '💉':'Seringue',        '🩺':'Stéthoscope',   '🩻':'Radiographie',
    '🧲':'Aimant',          '🦾':'Bras mécanique','🦿':'Jambe mécanique',
    '🤖':'Robot',           '🧠':'Cerveau',       '🫀':'Cœur anatomique',
    '🚬':'Cigarette',       '🍶':'Saké',          '🌶️':'Piment',
    '🧭':'Boussole',        '⚕️':'Médecine',      '💼':'Mallette',
    '🧤':'Gants',           '💅':'Manucure',      '🩰':'Chaussons ballet',
    '🧼':'Savon',           '🪢':'Nœud de corde', '🧵':'Fil',
    '🧸':'Peluche',         '🪆':'Poupée russe',  '🎯':'Cible',
    '🪖':'Casque militaire','🎩':'Haut-de-forme', '🏔️':'Sommet',
    '🌠':'Étoile filante',  '🎑':'Chrysanthème',  '🎋':'Bambou',
    '🌅':'Lever de soleil', '🌃':'Nuit étoilée',  '🌞':'Soleil souriant',
    '🗿':'Moaï',            '💫':'Étoile brillante','🌑':'Obscurité',
    '🕯️':'Bougie',          '🪩':'Boule miroir',  '🔱':'Trident de Neptune',
    '⛓️':'Chaîne',          '🧰':'Boîte à outils', '🪓':'Hache',
    '🔐':'Serrure sécurisée','📐':'Équerre',       '🔲':'Bouton carré',
    '🌗':'Demi-lune',       '🌓':'Quartier de lune','🌚':'Visage lune',
    '🍵':'Thé',             '🥢':'Baguettes',
}

def get_name(em):
    if em in FR:
        return FR[em]
    # Fallback : nom Unicode du premier codepoint visible
    stripped = ''.join(
        c for c in em
        if unicodedata.category(c) not in ('Mn', 'Cf') and c != '️'
    )
    if not stripped:
        return None
    try:
        name = unicodedata.name(stripped[0])
        # Nettoyer les préfixes techniques
        name = re.sub(
            r'^(EMOJI MODIFIER |COMBINING ENCLOSING |REGIONAL INDICATOR SYMBOL LETTER )', '', name
        )
        return name.title()
    except ValueError:
        return None

# Collecter tous les emojis uniques des personnages
emoji_set = set()
for char in data['CHARACTERS']:
    for em in char.get('emoji', []):
        emoji_set.add(em)

names = {}
missing = []
for em in emoji_set:
    n = get_name(em)
    if n:
        names[em] = n
    else:
        missing.append(repr(em))

# Écrire AVANT tout print pour éviter les crashes terminal
data['EMOJI_NAMES'] = names

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

size = os.path.getsize('data.json')
print(f'EMOJI_NAMES: {len(names)}/{len(emoji_set)} emojis nommes')
print(f'data.json: {size} bytes')
if missing:
    print(f'Sans nom: {missing}')
else:
    print('Tous les emojis ont un nom !')
