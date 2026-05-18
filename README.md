# CEAPresentation

Dépôt illustrant la création de présentations avec Beamer et **Manim-Slides**, utilisant le package maison **`manim_cea`** qui fournit le branding CEA (logo, cube décoratif, footer paginé) et des composants prêts à l'emploi (listes à puces, colonnes, vidéo).

Manim-Slides est un outil permettant de transformer des animations Manim en présentations interactives, navigables slide par slide.

---

## Installation

Depuis la racine du dépôt :

```bash
pip install -e ./manim_cea
```

Dépendances tirées automatiquement : `manim`, `manim-slides`, `opencv-python`, `Pillow`, `numpy`.

---

## Démarrage rapide

Un script minimal `example.py` :

```python
from manim import *
from manim_cea import CEAScene, bullet_list

class MaPartie(CEAScene):
    AUTHOR  = "Prénom NOM"
    SEMINAR = "Mon séminaire"
    DATE    = "Mai 2026"

    def construct(self):
        self.title_slide("Titre de la présentation")
        self.wait()
        self.next_slide()

        self.new_slide("Introduction")
        self.play(FadeIn(bullet_list(["Premier point", "Deuxième point"])))
        self.next_slide()
```

Compilation et affichage :

```bash
manim example.py MaPartie -ql
manim-slides convert MaPartie slides.html --open
```

---

## API du package `manim_cea`

### La scène : `CEAScene`

Tout se passe en héritant de `CEAScene` (qui hérite elle-même de `Slide` de `manim-slides`). Les métadonnées sont déclarées en **attributs de classe** :

```python
class MaPartie(CEAScene):
    AUTHOR  = "..."
    SEMINAR = "..."
    DATE    = "..."
```

Pour partager les mêmes métadonnées entre plusieurs scènes, factoriser via une classe de base :

```python
class Base(CEAScene):
    AUTHOR, SEMINAR, DATE = "P. Bouteiller", "Revue Projet", "Mai 2026"

class Slide1(Base): ...
class Slide2(Base): ...
```

Trois méthodes haut-niveau couvrent les besoins courants :

| Méthode | Rôle |
|---|---|
| `self.title_slide(title)` | Slide de titre (grand logo, cube décoratif, titre/auteur/séminaire/date). |
| `self.new_slide(title)` | Démarre une slide standard : nettoie l'écran, pose cube/titre/footer, incrémente la pagination. |
| `self.clear_slide()` | Efface l'écran (appelé automatiquement par `new_slide`). |

`self.next_slide()` reste disponible (hérité de `manim-slides`) pour marquer une pause / coupure de slide pendant la présentation.

### Composants visuels

| Fonction | Description |
|---|---|
| `bullet_list(items)` | Liste à puces carrées rouges. Les tuples `(item, [sous-items])` créent automatiquement un niveau d'indentation. |
| `numbered_list(items)` | Liste numérotée, numéros rouges en gras. |
| `red_square_list(items)` | Liste de Mobjects préfixés de carrés rouges (pratique pour mélanger `Text`, `MathTex`, `VGroup`). |
| `two_columns(left, right)` | Mise en page à deux colonnes. |
| `VideoMobject(filename, loop=...)` | Insertion d'une vidéo dans la scène. |

Toutes les listes retournent un `VGroup` quand leur contenu est entièrement vectorisé (compatible `Write`, `Create`), un `Group` sinon (utiliser `FadeIn`).

### Palette de couleurs

Importables directement depuis `manim_cea` :

`CEA_RED`, `CEA_DARK_BLUE`, `CEA_LIGHT_BLUE`, `CEA_DARK_GRAY`, `CEA_GRAY`, `CEA_LIGHT_GRAY`, `CEA_YELLOW`, `CEA_MACARON`, `CEA_ARCHIPEL`, `CEA_OPERA`, `CEA_GLYCINE`, `CEA_GREEN`, `CEA_ORANGE`.

### Macros LaTeX

Le fichier `macros.tex` est à placer à côté du script utilisateur (il n'est pas embarqué dans le package) :

```python
from manim import TexTemplate
tex_template = TexTemplate()
tex_template.add_to_preamble(r"\input{macros.tex}")
```

---

## Compilation des slides avec Manim-Slides

Supposons que le fichier utilisateur s'appelle `example.py`.

### Commandes de base

Les commandes de base pour compiler une slide et l'afficher dans le navigateur :

```bash
manim example.py Partie
manim-slides convert Partie slides.html --open
```

### Présentations longues

Pour éviter des recompilations excessives, nous conseillons aux utilisateurs de découper leur présentation en parties ou sous-parties matérialisées par plusieurs classes. La compilation de plusieurs classes s'effectue de la façon suivante :

```bash
manim example.py PartieUne PartieDeux
manim-slides convert PartieUne PartieDeux slides.html --open
```

Mais si l'utilisateur n'est amené à modifier qu'une seule partie, par exemple `PartieUne`, il peut simplement recompiler celle-ci :

```bash
manim example.py PartieUne
```

Puis afficher la présentation complète (manim-slides utilisera l'ancienne version de `PartieDeux`) avec la commande suivante :

```bash
manim-slides PartieUne PartieDeux
```

### Options utiles

#### Compilation rapide

Pour accélérer la compilation, l'utilisateur peut rajouter l'option `-ql` (basse qualité) à la ligne de commande :

```bash
manim example.py PartieUne -ql
```

#### Compilation en boucle

Si les scènes ont été numérotées `Slide1`, `Slide2`, etc., il est possible de toutes les compiler en une seule commande grâce à une boucle shell :

```bash
for i in {1..5}; do manim -ql example.py Slide$i; done
```

Puis de les convertir et afficher en une seule commande :

```bash
manim-slides convert $(for i in {1..5}; do echo Slide$i; done) slides.html --open
```

#### Export en PowerPoint

Pour exporter la présentation au format `.pptx` plutôt qu'en HTML, il suffit de changer l'extension dans la commande de conversion :

```bash
manim-slides convert PartieUne PartieDeux slides.pptx
```

Ou avec une boucle si les scènes sont numérotées :

```bash
manim-slides convert $(for i in {1..5}; do echo Slide$i; done) slides.pptx
```

---

## Organisation conseillée

```
ma_presentation/
├── presentation.py     # une ou plusieurs classes (Slide1, Slide2, ...)
├── macros.tex          # macros LaTeX éventuelles
├── media/              # vidéos et images
└── slides.html         # généré
```

Découper en plusieurs classes permet de :
- ne recompiler que la partie modifiée,
- isoler les bugs ou les scènes longues,
- réutiliser facilement une partie dans une autre présentation.

## Exemples

- `example.py` — script minimal de démonstration.
- `Revue_projet.py` — présentation complète (titre, plan, animations de réseaux atomiques, schémas blocs).
