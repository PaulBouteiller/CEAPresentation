"""
Utilitaires pour créer des présentations Manim avec le style CEA
"""
from manim import *
import os

class CEATheme:
    """Classe pour gérer le thème visuel CEA"""
    
    # Palette de couleurs CEA
    CEA_RED = "#E50019"
    CEA_DARK_BLUE = "#3E4A83"
    CEA_LIGHT_BLUE = "#7E9CBB"
    CEA_DARK_GRAY = "#262626"
    CEA_GRAY = "#787878"
    CEA_LIGHT_GRAY = "#BEBEBE"
    CEA_YELLOW = "#FFCD31"
    CEA_MACARON = "#DA837B"
    CEA_ARCHIPEL = "#00939D"
    CEA_OPERA = "#BD987A"
    CEA_GLYCINE = "#A72587"
    CEA_GREEN = "#6AB023"
    CEA_ORANGE = "#FF8C42"
    
    def __init__(self, scene, author="", seminar="", date="",):
        self.scene = scene
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.author = author
        self.seminar = seminar
        self.date = date
        self.page_number = 1
        
    def create_logo(self, scale=0.45, position=None):
        """
        Crée le logo CEA
        
        Args:
            scale: Facteur d'échelle du logo
            position: Position personnalisée (par défaut: coin supérieur gauche)
        """
        logo_path = os.path.join(self.script_dir, "graphics/logo_cea.png")
        if not os.path.exists(logo_path):
            print(f"ATTENTION: Logo non trouvé à {logo_path}")
            # Créer un rectangle rouge de remplacement
            logo = Square(side_length=1, color=self.CEA_RED, fill_opacity=1)
            logo.scale(scale)
        else:
            logo = ImageMobject(logo_path)
            logo.scale(scale)
        
        if position is None:
            logo.to_corner(UL, buff=0.5)
        else:
            logo.move_to(position)
        
        return logo
    
    def create_cube(self, cube_type="title", scale=0.65):
        """
        Crée le cube décoratif CEA
        
        Args: cube_type: "title" pour page de titre, "frame" pour slides normales
                scale: Facteur d'échelle du cube
        """
        cube_file = f"graphics/{cube_type}_cube_black.png"
        cube_path = os.path.join(self.script_dir, cube_file)
        
        if not os.path.exists(cube_path):
            print(f"ATTENTION: Cube non trouvé à {cube_path}")
            # Créer un motif de remplacement
            cube = Group()
            for i in range(3):
                for j in range(3):
                    square = Square(side_length=0.2, color=self.CEA_RED, 
                                  fill_opacity=0.7, stroke_width=0)
                    square.shift(RIGHT * i * 0.25 + UP * j * 0.25)
                    cube.add(square)
        else:
            cube = ImageMobject(cube_path)
        
        cube.scale(scale)
        cube.to_corner(UR, buff=0)
        return cube
    
    def create_footer(self, page_number = None, foot_logo=True):
        """
        Crée le footer avec ligne de séparation et informations
        
        Args:
            page_number: Numéro de page (optionnel)
        """
        footer = Group()
        
        # Ligne de séparation
        # line = Line(start=LEFT * 7.5, end=RIGHT * 7.5, color=WHITE, stroke_width=1).to_edge(DOWN, buff=0.5)
        
        # Texte du footer
        footer_parts = []
        footer_parts.append(self.author)
        footer_parts.append(self.seminar)
        footer_parts.append(self.date)
        
        footer_text_str = " – ".join(footer_parts)
        if page_number is not None:
            footer_text_str += f"  {page_number}"
            
            # Aligner le texte en bas à droite
        footer_text = Text(footer_text_str, color=WHITE, font_size=18)
        footer_text.to_corner(DR, buff=0.3)
        footer_text.shift(UP * 0.1)  # Légèrement au-dessus du bord pour l'alignement avec le logo
        footer_logo = self.create_logo(scale=0.2)
        footer_logo.to_corner(DL, buff=0.3)
        if foot_logo:
            footer.add(footer_logo, footer_text)
        else:
            footer.add(footer_text)
        return footer
        
    def create_title_slide(self, title):
        """
        Crée une slide de titre complète
        
        Returns:
            Group contenant tous les éléments de la slide de titre
        """
        slide_elements = Group()
        
        # Logo et cube
        logo = self.create_logo()
        cube = self.create_cube(cube_type="title")
        
        # Textes avec tailles proportionnelles
        base_font_size = 48
        
        title_text = Text(title, font_size=base_font_size, color=WHITE, weight=BOLD)
        author_text = Text(self.author, font_size=base_font_size * 0.65, color=WHITE)
        seminar_text = Text(self.seminar, font_size=base_font_size * 0.55, color=WHITE)
        date_text = Text(self.date, font_size=base_font_size * 0.5, color=WHITE)
        
        # Grouper et arranger les textes
        text_group = Group(title_text, author_text, seminar_text, date_text)
        text_group.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        # Aligner avec le logo et positionner
        text_group.align_to(logo, LEFT)
        text_group.shift(DOWN * 0.5)
        
        # Footer
        footer = self.create_footer(self.page_number, foot_logo = False)
        self.page_number +=1
        slide_elements.add(logo, cube, title_text, author_text, seminar_text, date_text, footer)
        
        return slide_elements
    
    def create_standard_slide(self, title_text):
        """
        Crée les éléments standard d'une slide (cube, titre, footer avec petit logo)
        
        Returns:
            tuple: (Group des éléments fixes, Text du titre)
        """
        slide_elements = Group()
        
        # Cube pour slide normale (pas de grand logo en haut)
        cube = self.create_cube(cube_type="frame", scale=0.5)
        
        # Titre
        title = Text(title_text, font_size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        title.to_edge(LEFT, buff=0.5)
        
        # Footer avec petit logo CEA, texte et numéro
        footer = self.create_footer(self.page_number)
        self.page_number +=1
        
        slide_elements.add(cube, footer)
        
        return slide_elements, title


def create_bullet_list(items, color=WHITE, font_size=32, 
                       buff_between=0.4, indent=0, bullet_style="square"):
    """
    Crée une liste à puces avec style CEA
    
    Args:
        items: Liste de strings ou Mobjects
        color: Couleur du texte
        font_size: Taille de la police
        buff_between: Espacement entre items
        indent: Indentation (pour sous-listes)
        bullet_style: "square" (CEA) ou "dot"
    """
    bullet_list = Group()
    
    for item in items:
        # Créer la puce
        if bullet_style == "square":
            bullet = Square(side_length=0.12, 
                            color=CEATheme.CEA_RED if indent == 0 else color,
                            fill_opacity=1,
                            stroke_width=0)
        else:
            bullet = Dot(radius=0.06, color=color)
        
        # Créer le texte
        if isinstance(item, str):
            text = Text(item, color=color, font_size=font_size)
        else:
            text = item
        
        # Grouper puce et texte
        bullet_item = Group(bullet, text)
        text.next_to(bullet, RIGHT, buff=0.2)
        
        bullet_list.add(bullet_item)
    
    # Arranger verticalement
    bullet_list.arrange(DOWN, aligned_edge=LEFT, buff=buff_between)
    bullet_list.to_edge(LEFT, buff=1.5 + indent)
    
    return bullet_list


def create_numbered_list(items, color=WHITE, font_size=32, buff_between=0.4):
    """
    Crée une liste numérotée avec style CEA (numéros rouges en gras)
    """
    numbered_list = Group()
    
    for i, item in enumerate(items, 1):
        number = Text(f"{i}.", color=CEATheme.CEA_RED, font_size=font_size, weight=BOLD)
        if isinstance(item, str):
            text = Text(item, color=color, font_size=font_size)
        else:
            text = item
        
        # Grouper numéro et texte
        numbered_item = Group(number, text)
        text.next_to(number, RIGHT, buff=0.3)
        
        numbered_list.add(numbered_item)
    
    numbered_list.arrange(DOWN, aligned_edge=LEFT, buff=buff_between)
    numbered_list.to_edge(LEFT, buff=1.5)
    
    return numbered_list


def create_two_columns(left_content, right_content, buff=1.0):
    """
    Crée une mise en page à deux colonnes
    
    Args:
        left_content: Contenu de la colonne gauche (Mobject)
        right_content: Contenu de la colonne droite (Mobject)
        buff: Espacement entre les colonnes
    """
    columns = Group(left_content, right_content)
    columns.arrange(RIGHT, buff=buff)
    
    return columns


def create_itemize(items, buff_horizontal=1, initial_height=1, 
                   espacement=0.5, bullet_text_spacing=0.2, scale_factor=1):
    bullet_items = VGroup()
    for i, item in enumerate(items):
        bullet = Dot(radius=0.05, color=WHITE)
        
        # Vérifie le type de l'élément
        if isinstance(item, Mobject):  # Si c'est déjà un objet Manim
            text = item
        else:  # Sinon, créer un objet Text
            text = Text(item, color=WHITE)
            
        bullet_item = VGroup(bullet, text).scale(scale_factor)
        text.next_to(bullet, RIGHT, buff=bullet_text_spacing)
        bullet_item.shift(UP * initial_height + DOWN * i * espacement)
        bullet_items.add(bullet_item)
    bullet_items.to_edge(LEFT, buff=buff_horizontal)
    return bullet_items

def create_nested_itemize(main_items, sub_items_list, buff_horizontal=1, initial_height=1, 
                         espacement=0.5, bullet_text_spacing=0.2, scale_factor=1, 
                         sub_indent=0.5, sub_scale_factor=0.9):
    
    # Groupe principal pour tous les items (pour le placement)
    all_items = VGroup()
    
    # Liste pour stocker les séquences d'animation
    animation_sequence = []
    
    current_y = initial_height
    
    # Traiter chaque item principal et ses sous-items
    for i, (main_item, sub_items) in enumerate(zip(main_items, sub_items_list)):
        # Créer l'item principal
        bullet = Dot(radius=0.05, color=WHITE)
        text = Text(main_item, color=WHITE) if isinstance(main_item, str) else main_item
        
        main_group = VGroup(bullet, text).scale(scale_factor)
        text.next_to(bullet, RIGHT, buff=bullet_text_spacing)
        main_group.shift(UP * current_y)
        main_group.to_edge(LEFT, buff=buff_horizontal)
        
        all_items.add(main_group)
        animation_sequence.append(main_group)
        
        # Ajuster la position pour les items suivants
        current_y -= espacement * 1.5
        
        # Ajouter les sous-items si présents
        if sub_items:
            sub_groups = VGroup()
            
            for sub_item in sub_items:
                # Créer le sous-item avec un style différent
                sub_bullet = Dot(radius=0.04, color=WHITE)  # Plus petit
                sub_text = Text(sub_item, color=WHITE) if isinstance(sub_item, str) else sub_item
                
                sub_group = VGroup(sub_bullet, sub_text).scale(scale_factor * sub_scale_factor)
                sub_text.next_to(sub_bullet, RIGHT, buff=bullet_text_spacing)
                sub_group.shift(UP * current_y)
                sub_group.to_edge(LEFT, buff=buff_horizontal + sub_indent)
                
                sub_groups.add(sub_group)
                animation_sequence.append(sub_group)
                
                # Ajuster pour le prochain sous-item
                current_y -= espacement
            
            all_items.add(sub_groups)
    
    return all_items, animation_sequence

import cv2
from PIL import Image, ImageOps
from dataclasses import dataclass
import numpy as np

@dataclass
class VideoStatus:
    time: float = 0
    videoObject: cv2.VideoCapture = None
    loop_count: int = 0  # Ajout d'un compteur de boucles
    def __deepcopy__(self, memo):
        return self

class VideoMobject(ImageMobject):
    def __init__(self, filename=None, imageops=None, speed=1.0, loop=False, **kwargs):
        self.filename = filename
        self.imageops = imageops
        self.speed = speed
        # Gestion du paramètre loop
        self.loop = float('inf') if loop is True else (int(loop) if isinstance(loop, (int, float)) else 0)
        self._id = id(self)
        self.status = VideoStatus()
        self.status.videoObject = cv2.VideoCapture(filename)
        self.status.videoObject.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, frame = self.status.videoObject.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            img = Image.fromarray(frame)
            if imageops != None:
                img = imageops(img)
        else:
            img = Image.fromarray(np.uint8([[63, 0, 0, 0],
                                        [0, 127, 0, 0],
                                        [0, 0, 191, 0],
                                        [0, 0, 0, 255]]))
        super().__init__(img, **kwargs)
        if ret:
            self.add_updater(self.videoUpdater)

    def videoUpdater(self, mobj, dt):
        if dt == 0:
            return
        status = self.status
        status.time += 1000*dt*mobj.speed
        self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
        ret, frame = self.status.videoObject.read()
        
        # Gestion du nombre de boucles
        if ret == False:
            if status.loop_count < self.loop:  # Vérifie si on peut encore boucler
                status.loop_count += 1  # Incrémente le compteur
                status.time = 0
                self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
                ret, frame = self.status.videoObject.read()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            if mobj.imageops != None:
                img = mobj.imageops(img)
            mobj.pixel_array = change_to_rgba_array(
                np.asarray(img), mobj.pixel_array_dtype
            )