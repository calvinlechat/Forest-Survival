##########################################################   IMPORTS  ########################################################################################

import pyxel
from random import randint

##########################################################   JOUEUR   ########################################################################################

class Joueur:
    """
    Classe représentant le joueur.
    Gère la position, le déplacement, l'état (vie, nourriture), les collisions, et les sprites.
    """
    def __init__(self):
        self.vitesse = 1
        self.x = 90
        self.y = 80

        self.inventaire = Inventaire()

        self.direction = 0
        self.en_mouvement = False
        self.block = False
        self.decompte_immobile = 0
        
        self.bouffe = 10
        self.vie = 10

        self.sprite = (64,56)
        self.animation = 1

        self.cooldown = True
        self.ancienne_pos = (self.x,self.y)
        
    def mouvement_joueur(self):
        """Met à jour la position du joueur en fonction des touches directionnelles."""
        self.ancienne_pos = (self.x, self.y)

        if pyxel.btn(pyxel.KEY_D) and not(self.x >= 186) and (self.direction == 2 or self.en_mouvement is False):
            self.x += self.vitesse                            # droite
            self.direction = 2
         
        if pyxel.btn(pyxel.KEY_S) and not(self.y >= 122) and (self.direction == 0 or self.en_mouvement is False):
            self.y += self.vitesse                            # bas
            self.direction = 0 
            
        if pyxel.btn(pyxel.KEY_Q) and not(self.x <= -7) and (self.direction == 3 or self.en_mouvement is False):
            self.x -= self.vitesse                            # gauche
            self.direction = 3
           
        if pyxel.btn(pyxel.KEY_Z) and not(self.y <= -3) and (self.direction == 1 or self.en_mouvement is False):
            self.y -= self.vitesse                            # haut
            self.direction = 1

        if self.ancienne_pos == (self.x,self.y):
            self.en_mouvement = False
        else:
            self.en_mouvement = True
            
    def sprite_joueur(self):
        """Gère l'animation du sprite du joueur selon sa direction et son mouvement."""
        liste_sprite = [[(64,56),(80,56),(96,56)],[(64,40),(80,40),(96,40)],[(64,24),(80,24),(96,24)],[(64,8),(80,8),(96,8)]]  # [bas,haut,droite,gauche] --> [immobile, animation1, animation2]
        
        if not self.en_mouvement or self.block:
            if self.decompte_immobile == 1:
                self.sprite = liste_sprite[self.direction][0]
                self.decompte_immobile = 0
            else:
                self.decompte_immobile = 1
                self.block = False
        else:
            self.sprite = liste_sprite[self.direction][self.animation]         
            if pyxel.frame_count % 10 == 0 :
                if self.animation == 1:
                    self.animation =2
                else:
                    self.animation = 1
    
    def collision(self, arbre):
        """Renvoie True si le joueur est en collision avec un arbre."""
        # Vérifie si le joueur est proche de l'arbre (zone de collision)
        if abs(self.x_milieu() - arbre.x_milieu()) < 6 and abs(self.y_base() - arbre.y_base()) < 6 and not(arbre.type in [8,9,5,15,16,17,18,19]) :
            return True
        return False
    
    def delai_cooldown(self):
        """Réinitialise le cooldown du joueur toutes les 20 frames."""
        if pyxel.frame_count % 20 == 0 :
            self.cooldown = True
 
    def y_base(self):
        """Renvoie la coordonnée y de la base du sprite du joueur."""
        return self.y + 16  # base du sprite du joueur
    
    def x_milieu(self):
        """Renvoie la coordonnée x du centre du sprite du joueur."""
        return self.x + 8  # milieu du sprite du joueur
    
    def vie_joueur(self,pourcentage_oxygene):
        """
        Met à jour la vie et la nourriture du joueur.
        La nourriture baisse régulièrement, et la vie varie selon l’oxygène disponible et la nourriture.
        """

        # gestion bouffe
        if self.bouffe > 10:
            self.bouffe = 10
        if pyxel.frame_count % 500 == 0 and self.bouffe > 0 :
            self.bouffe -= 1
        elif self.bouffe == 0 and pyxel.frame_count % 1500 == 0:
            self.vie -=1


        if pourcentage_oxygene > 60 and self.bouffe > 4 and self.vie < 10 and pyxel.frame_count % 1500 == 0:
            self.vie += 1
        elif pourcentage_oxygene < 50 and pyxel.frame_count % 1500 == 0:
            self.vie -= 1
        elif pourcentage_oxygene < 30 and pyxel.frame_count % 1500 == 0:
            self.vie -= 2
        elif pourcentage_oxygene < 10:
            self.vie = 0

    
    def update(self):
        """Met à jour l'état du joueur à chaque frame (sprite, mouvement, cooldown)."""
        self.sprite_joueur()
        self.delai_cooldown()
        self.mouvement_joueur()

    def draw(self):
        # affichage joueur
        pyxel.blt(self.x, self.y , 0 , self.sprite[0], self.sprite[1], 16, 16, 5)  

###############################################################  INVENTAIRE DU JOUEUR ####################################################################################


class Inventaire:
    """
    Gère l'inventaire du joueur (objets, outils, durabilité, et actions comme le craft).
    """
    def __init__(self):
        self.stockage = {} 
        self.vie_hache = 25 
        self.vie_pelle = 5
        self.vie_foreuse = 30

    def ajout(self, objet, quantite=1):
        """Ajoute un objet à l'inventaire."""
        if objet in self.stockage:
            self.stockage[objet] += quantite
        else:
            self.stockage[objet] = quantite
    
    def craft(self,objet,materiaux):
        """Tente de crafter un objet si les matériaux sont disponibles."""
        for mater in materiaux:
            if int(self.quantite_recup(mater[0])) < mater[1]:  
                return
            
        for mater in materiaux:
            self.stockage[mater[0]] -= mater[1]
        self.ajout(objet[0],objet[1])
            

    def quantite_recup(self,objet):
        """Renvoie la quantité d'un objet sous forme de chaîne."""
        if objet in self.stockage:
            return str(self.stockage[objet])
        else:
            return "0"

    def forage(self):
        """Ajoute des ressources avec la foreuse et gère sa durabilité."""
        self.ajout("roche",2)
        if self.vie_foreuse > 0:
            self.vie_foreuse -=1 # baisse la durabilité de la hache
        else:
            self.stockage["foreuse"] -= 1
            self.vie_foreuse = 30
    
    def planter_arbre_inv(self):
        """Plante un arbre avec des batons et diminue la durabilité de la pelle."""
        self.stockage["baton"] -= 5
        if self.vie_pelle > 0:
            self.vie_pelle -=1 # baisse la durabilité de la hache
        else:
            self.stockage["pelle"] -= 1
            self.vie_pelle = 5
    
    def poser_piege_inv(self,type_p):
        """Diminue le nombre de pièges du type correspondant dans l’inventaire."""
        self.stockage[type_p] -=1

    def afficher(self):
        """Affiche l’état de l’inventaire dans la console (debug)."""
        print("Inventaire:", self.stockage)
        
        


##########################################################   ARBRE ET ROCHER  ########################################################################################


    
class ArbreEtRoche:
    """
    Représente un arbre ou une roche dans le jeu.
    Gère sa position, son état, ses points de vie, et les interactions avec le joueur.
    """
    def __init__(self,x,y,type_arbre_roche):
        self.x = x
        self.y = y
        self.etat = "vie" 
        self.pv = 5
        self.sprite = (0,0,16,16)
        self.type = type_arbre_roche
        self.tranche = [0,None]
        self.sprite_arbre_roche()
        self.init_vie_arbre_roche()
    
    def hachage(self,x_joueur,y_joueur,direction_joueur,inventaire_joueur):
        """Permet de hacher un arbre si le joueur est en position correcte et possède une hache."""
        if abs((x_joueur+8) - self.x_milieu()) < 8 and abs((y_joueur+16)-self.y_base()) < 8 and int(inventaire_joueur.quantite_recup("hache")) > 0:   # +8 pour le milieu du joueur
            
            # Vérifie que le joueur regarde bien l’arbre
            if (
                (direction_joueur == 0 and y_joueur+16 < self.y_base()) or  # vers le bas
                (direction_joueur == 1 and y_joueur+16 > self.y_base()) or  # vers le haut
                (direction_joueur == 2 and x_joueur+8 < self.x_milieu()) or  # vers la droite
                (direction_joueur == 3 and x_joueur+8 > self.x_milieu())     # vers la gauche
                ):              
                self.animation_hachage(direction_joueur)
                self.pv -= 1
                
                if inventaire_joueur.vie_hache > 0:
                    inventaire_joueur.vie_hache -=1 # baisse la durabilité de la hache
                else:
                    inventaire_joueur.stockage["hache"] -= 1
                    inventaire_joueur.vie_hache = 25

                # Ajouter du bois à l'inventaire à chaque coup
                if self.type in [12,13,14]:
                    inventaire_joueur.ajout("roche",2)
                elif self.type in [0,1,2,3,4,5,6,7,8,9,10,11]:
                    inventaire_joueur.ajout("bois",2)
  
    def animation_hachage(self,direction_joueur):
        """Active l’animation de hachage dans la direction indiquée."""
        self.tranche = [4,(direction_joueur*16,152)]

    def sprite_arbre_roche(self):
        """Définit le sprite correspondant au type d’arbre ou roche."""                                                                                                                                                                               # (tuile x , tuile y , largeur ,hauteur)
        liste_sprite_arbre = [(115,9,9,15),(126,6,18,18),(145,6,13,18),(115,24,9,12),(133,25,5,15),(147,24,11,10),(161,19,13,18),(112,37,15,19),(132,41,8,6),(131,48,10,8),(145,35,13,22),(161,38,13,18),(112,60,15,12),(129,59,15,13),(146,59,14,13),(165,12,6,4),(179,16,9,8),(177,28,12,12),(177,42,13,14),(176,56,16,16)] # ordre : gauche à droite et haut en bas
        self.sprite = liste_sprite_arbre[self.type]
    
    def arbre(self):
        """Retourne 1 si c’est un arbre, 0 si c’est une roche."""
        if self.type in [12,13,14]:
            return 0
        else:
            return 1
        
    def y_base(self):
        """Renvoie la coordonnée y de la base de l’arbre/roche."""
        return self.y + self.sprite[3]  # le bas du sprite de l’arbre   
    
    def x_milieu(self):
        """Renvoie la coordonnée x du centre de l’arbre/roche."""
        return self.x + self.sprite[2]//2  # le milieu du sprite de l’arbre
    
    def init_vie_arbre_roche(self):
        """Initialise les points de vie selon le type d’objet (arbre ou roche)."""
        if self.type in [8,9,15,16,17,18,19]:
            self.pv = 1
        elif self.type == 5:
            self.pv = 2
        elif self.type in [4,3]:
            self.pv = 3
        elif self.type in [0,11]:
            self.pv = 4
        elif self.type in [2,6,7,12,13,14]:
            self.pv = 5
        else:
            self.pv = 7
    
    def update(self, joueur, attaque=False):
        """Met à jour l’objet en fonction des actions du joueur (attaque, animation)."""
        if attaque:
            self.hachage(joueur.x,joueur.y,joueur.direction,joueur.inventaire)

        if self.tranche[0] > 0:
            self.tranche[0] -= 1  # compte à rebours

     
        if self.pv <= 0 and self.tranche[0] == 0:         # - plus de PV
            self.etat = "mort"                            # - animation terminée

        if self.type in [15,16,17,18] and pyxel.frame_count % 1000 == 0 :
            self.type += 1
            self.sprite_arbre_roche()

        elif self.type == 19 and pyxel.frame_count % 1000 == 0 and (abs((joueur.x+8) - self.x_milieu()) > 8 or abs((joueur.y+16)-self.y_base()) > 8):
            self.type = [0,1,2,6,7,10,11][randint(0,6)]
            self.sprite_arbre_roche()
            self.init_vie_arbre_roche()
    
            


    def draw(self):
        """Affiche l’arbre ou la roche à l’écran avec Pyxel."""
        # affichage arbre et roche
        pyxel.blt(self.x, self.y , 0,self.sprite[0],self.sprite[1],self.sprite[2],self.sprite[3],5)

        if self.tranche[0] > 0:
             pyxel.blt(self.x_milieu()-8, self.y_base()-16 , 0,self.tranche[1][0],self.tranche[1][1],16,16,5)


def init_arbre_roche():
    """
    Initialise une liste d'objets ArbreEtRoche avec des positions aléatoires.
    
    Returns:
        list: Liste d'instances de la classe ArbreEtRoche.
    """
    liste_arbre_roche = []
    for i in range(60):
        presence_abr = False
        x_arbre_roche = randint(0,176)
        y_arbre_roche = randint(2,100)
        for abr in liste_arbre_roche:
            if abs(abr.x-x_arbre_roche) < 16 and abs(abr.y-y_arbre_roche) < 16:
                presence_abr = True
        if presence_abr == False:               
            liste_arbre_roche.append(ArbreEtRoche(x_arbre_roche,y_arbre_roche,randint(0,14)))
    return liste_arbre_roche

def planter_arbre(liste_arbre_roche,x_joueur,y_joueur,inventaire_joueur):
    """
    Plante un arbre si aucun arbre ou piège n'est déjà à proximité.

    Args:
        liste_arbre_roche (list): Liste des arbres et rochers de la scène.
        x_joueur (int): Position x du joueur.
        y_joueur (int): Position y du joueur.
        inventaire_joueur (Inventaire): Inventaire du joueur.

    Returns:
        list: Liste mise à jour des arbres et rochers.
    """
    presence_abr = False
    x_arbre = x_joueur + 8
    y_arbre = y_joueur + 16
    for abr in liste_arbre_roche:
        if abs(abr.x-x_arbre) < 16 and abs(abr.y-y_arbre) < 16:
            presence_abr = True
    if presence_abr == False:               
        liste_arbre_roche.append(ArbreEtRoche(x_arbre,y_arbre,15))
        inventaire_joueur.planter_arbre_inv()
    return liste_arbre_roche

def compter_arbre(liste_arbre_roche):
    """
    Compte le nombre d’arbres vivants dans la liste.

    Args:
        liste_arbre_roche (list): Liste des objets ArbreEtRoche.

    Returns:
        int: Nombre d’arbres (exclut les rochers).
    """
    compteur = 0
    for abr in liste_arbre_roche:
        compteur += abr.arbre()
    return compteur

##########################################################   BATON ET PIERRE  ########################################################################################

class BatonEtPierre:
    """
    Représente un objet collectable au sol : soit un bâton, soit une pierre.
    Le joueur peut les ramasser pour crafter des outils.
    """
    def __init__(self,x,y,type_baton_pierre):
        self.x = x
        self.y = y
        self.etat = "vie" 
        self.pv = 3
        self.sprite = (0,0,16,16)
        self.type = type_baton_pierre
        self.sprite_baton_pierre()
    
    def sprite_baton_pierre(self):                                                         # (tuile x , tuile y , largeur ,hauteur)
        """Définit le sprite associé au type (bâton ou pierre)."""
        liste_sprite_baton_pierre = [(112,72,16,16),(128,72,16,16),(144,72,16,16),(160,56,16,16),(160,56,16,16),(160,56,16,16)] 
        self.sprite = liste_sprite_baton_pierre[self.type]
    
    def y_milieu(self):
        """Renvoie la coordonnée y du centre de l’objet."""
        return self.y + self.sprite[3]//2  # le milieu du sprite  
     
    def x_milieu(self):
        """Renvoie la coordonnée x du centre de l’objet."""
        return self.x + self.sprite[2]//2  # le milieu du sprite 
    
    def ramasser(self,x_joueur,y_joueur,inventaire_joueur):
        """
        Si le joueur est assez proche, il ramasse l’objet
        et l’ajoute à son inventaire (pierre ou bâton).
        """
        if abs((x_joueur+8) - self.x_milieu()) < 8 and abs((y_joueur+8)-self.y_milieu()) < 8:   # +8 pour le milieu du joueur
            self.pv -= 1
            
            # Ajouter du bois à l'inventaire à chaque coup
            if self.type in [0,1,2]:
                inventaire_joueur.ajout("pierre",2)
            else:
                inventaire_joueur.ajout("baton",2)
    

    def update(self, joueur, attaque=False):
        """Met à jour l’état de l’objet si ramassé."""
        if attaque:
            self.ramasser(joueur.x,joueur.y,joueur.inventaire)
     
        if self.pv <= 0:         # - plus de PV
            self.etat = "mort"                            
            

    def draw(self):
        """Affiche l’objet à l’écran avec Pyxel."""
        # affichage arbre
        pyxel.blt(self.x, self.y , 0,self.sprite[0],self.sprite[1],self.sprite[2],self.sprite[3],5)
    


def init_baton_pierre():
    """
    Initialise une liste d'objets BatonEtPierre à des positions aléatoires.

    Returns:
        list: Liste d’instances de la classe BatonEtPierre.
    """
    liste_baton_pierre = []
    for i in range(15):
        presence_b_p = False
        x_b_p = randint(0,176)
        y_b_p = randint(2,100)
        for b_p in liste_baton_pierre:
            if abs(b_p.x-x_b_p) < 16 and abs(b_p.y-y_b_p) < 16:
                presence_b_p = True
        if presence_b_p == False:               
            liste_baton_pierre.append(BatonEtPierre(x_b_p,y_b_p,randint(0,5)))
    return liste_baton_pierre

    
##########################################################  ANIMAUX ########################################################################################

class Animaux:
    """
    Gère la population d’animaux dans le monde.
    Trois espèces : lapins, sangliers, ragondins.
    Ils peuvent être capturés avec des pièges.
    """
    def __init__(self):
        self.lapin = 5
        self.sanglier = 3
        self.ragondin = 6
    
    def update(self):
        """Régénère lentement les populations si elles sont encore viables."""

        if self.lapin < 5 and self.lapin > 1 and pyxel.frame_count % 2000 == 0:
            self.lapin +=1

        if self.sanglier < 3 and self.sanglier > 1 and pyxel.frame_count % 4000 == 0:
            self.sanglier +=1

        if self.ragondin < 6 and self.ragondin > 1 and pyxel.frame_count % 1500 == 0:
            self.ragondin +=1
    
    def prise_au_piege(self,type_p):
        """
        Simule la capture d’un animal par un piège.
        Retourne le type d’animal capturé ou None.
        """
        animal_capturé = randint(0,16)
        if type_p == "pge lap":
    
            if animal_capturé <= 11 and self.lapin > 0:
                self.lapin -= 1
                return "lapin"
            elif animal_capturé == 12 and self.sanglier > 0:
                self.sanglier -= 1
                return "sanglier"
            elif animal_capturé >= 14 and self.ragondin > 0:
                self.ragondin -=1
                return "ragondin"

        elif type_p == "pge san":
            
            if animal_capturé <= 9 and self.sanglier > 0:
                self.sanglier -= 1
                return "sanglier"
            elif animal_capturé in [10,11,12] and self.lapin > 0:
                self.lapin -= 1
                return "lapin"
            elif animal_capturé >= 14 and self.ragondin > 0:
                self.ragondin -=1
                return "ragondin"

        elif type_p == "pge rag":
            
            if animal_capturé <= 13 and self.ragondin > 0:
                self.ragondin -= 1
                return "ragondin"
            elif animal_capturé == 14 and self.sanglier > 0:
                self.sanglier -= 1
                return "sanglier"
            elif animal_capturé >= 16 and self.lapin > 0:
                self.lapin -=1
                return "lapin"
        return None

def poser_piege(liste_piege,liste_arbre_roche,x_joueur,y_joueur,inventaire_joueur,type_p):
    """
    Pose un piège au sol si aucun obstacle ne gêne à l’endroit ciblé.

    Args:
        liste_piege (list): Liste actuelle des pièges dans la scène.
        liste_arbre_roche (list): Liste des arbres et rochers de la scène.
        x_joueur (int): Position x du joueur.
        y_joueur (int): Position y du joueur.
        inventaire_joueur (Inventaire): Inventaire du joueur.
        type_p (str): Type de piège ("pge lap", "pge san", "pge rag").

    Returns:
        list: Liste mise à jour des pièges.
    """
    presence_abr = False
    x_piege = x_joueur + 8
    y_piege = y_joueur + 16
    for abr in liste_arbre_roche:
        if abs(abr.x-x_piege) < 16 and abs(abr.y-y_piege) < 16:
            presence_abr = True
    for abr in liste_piege:
        if abs(abr[0]-x_piege) < 16 and abs(abr[1]-y_piege) < 16:
            presence_abr = True

    if presence_abr == False:               
        liste_piege.append([x_joueur+8,y_joueur+8,type_p,None,0]) # (x,y,viande,sprite)
        inventaire_joueur.poser_piege_inv(type_p)
    return liste_piege


########################################################## SCENE  ########################################################################################################
class Scene:
    """
    Représente une scène de la carte (1 des 9 zones du monde).
    Contient ses propres arbres, roches, objets, et pièges.
    """
    def __init__(self):
        self.liste_arbre_roche = init_arbre_roche()
        self.liste_baton_pierre = init_baton_pierre()
        self.liste_pieges = []

class Gestion_scene:
    """
    Gère l'ensemble des 9 scènes du jeu.
    Permet de naviguer entre les scènes selon les déplacements du joueur.
    """
    def __init__(self):
        self.liste_scene = [[],[],[]] #  [x][y]
        self.scene = [randint(0,2),randint(0,2)]
        for x in self.liste_scene:
            for y in range(3):
                x.append(Scene())
    
    def update(self, joueur):
        """Met à jour la scène active en fonction de la position du joueur."""
         
        if pyxel.btn(pyxel.KEY_D) and joueur.x >= 185 and self.scene[0] < 2:
            self.scene[0] += 1
            joueur.x = -2
         
        if pyxel.btn(pyxel.KEY_Q) and joueur.x <= -6 and self.scene[0] > 0:
            self.scene[0] -= 1
            joueur.x = 180
        
        if pyxel.btn(pyxel.KEY_S) and joueur.y >= 121 and self.scene[1] < 2:
            self.scene[1] += 1
            joueur.y = -2

        if pyxel.btn(pyxel.KEY_Z) and joueur.y <= -2 and self.scene[1] > 0:
            self.scene[1] -= 1
            joueur.y = 118
        
##########################################################   DEROULEMENT PARTIE ET AFFICHAGE ########################################################################################


class App:
    """
    Classe principale du jeu. Gère l'initialisation, la boucle de jeu, les mises à jour et les affichages.
    Contient tous les éléments : joueur, scènes, environnement, interface.
    """
    def __init__(self):
        pyxel.init(192,128, title="jeu_calvin",quit_key = pyxel.KEY_N)
        pyxel.load("1.pyxres")
        
        self.scenes = Gestion_scene()
        self.joueur = Joueur()
        self.Etat_vie = True
        self.nombre_arbre = 0

        self.afficher_inventaire = False  # L'inventaire est caché par défaut
        self.afficher_craft = False # Les crafts sont cachés par défaut 
        self.afficher_map = False
        self.afficher_craft_possible = 0
        self.afficher_etat = False
        
        self.animaux = Animaux() 
        pyxel.run(self.update, self.draw)
       


    def update(self):
        """
        Fonction appelée à chaque frame :
        - met à jour le joueur, les arbres, les objets
        - traite les interactions et les crafts
        - gère les conséquences écologiques
        """
               
        # Basculer l'état de l'inventaire lorsqu'on clique E
        if pyxel.btnr(pyxel.KEY_E) and self.afficher_craft_possible == 0:
            self.afficher_inventaire = not self.afficher_inventaire
            if self.afficher_craft:
                self.afficher_craft = False
                self.afficher_inventaire = False

        # Basculer l'état de l'inventaire vers le craft lorsqu'on clique R
        if pyxel.btnr(pyxel.KEY_R) and not(self.afficher_inventaire == self.afficher_craft) and self.afficher_craft_possible == 0:
            self.afficher_craft = not self.afficher_craft
            self.afficher_inventaire = not self.afficher_inventaire

           # Basculer vers un craft
        if pyxel.btnr(pyxel.KEY_KP_0) and self.afficher_craft:
            self.afficher_craft_possible = 0
        elif pyxel.btnr(pyxel.KEY_KP_1) and self.afficher_craft:
            self.afficher_craft_possible = 1
        elif pyxel.btnr(pyxel.KEY_KP_2) and self.afficher_craft:
            self.afficher_craft_possible = 2
        elif pyxel.btnr(pyxel.KEY_KP_3) and self.afficher_craft:
            self.afficher_craft_possible = 3
        elif pyxel.btnr(pyxel.KEY_KP_4) and self.afficher_craft:
            self.afficher_craft_possible = 4
        elif pyxel.btnr(pyxel.KEY_KP_5) and self.afficher_craft:
            self.afficher_craft_possible = 5
        elif pyxel.btnr(pyxel.KEY_KP_6) and self.afficher_craft:
            self.afficher_craft_possible = 6
        
        # Basculer la map si M est cliqué
        if pyxel.btnr(pyxel.KEY_L):
            self.afficher_etat = not self.afficher_etat

        # Basculer la map si M est cliqué
        if pyxel.btnr(pyxel.KEY_M):
            self.afficher_map = not self.afficher_map

        
        # Détermine si le joueur active la foreuse à cette frame
        if pyxel.btnr(pyxel.KEY_F) and int(self.joueur.inventaire.quantite_recup("foreuse")) > 0:
            self.joueur.inventaire.forage()

        # Détermine si le joueur attaque cette frame
        attaque = self.joueur.cooldown and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)
       
        for abr in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche:
            abr.update(self.joueur, attaque)    
            if self.joueur.collision(abr):
                # Empêche le mouvement si collision
                self.joueur.x, self.joueur.y = self.joueur.ancienne_pos
                self.joueur.block = True

        # Détermine si le joueur interragit cette frame
        interraction = self.joueur.cooldown and pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT)
       
        for b_p in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_baton_pierre:         # mise à jour baton_pierre
            b_p.update(self.joueur, interraction)    
        
        for piege in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges:         # prendre la viande du piege
            if abs((self.joueur.x+8) - piege[0]) < 8 and abs((self.joueur.y+8)-piege[1]) < 8 and interraction and piege[3] != None:   # +8 pour le milieu du joueur etc

                # recuperer la nouritture correspondante
                if piege[3] == "lapin":
                    self.joueur.bouffe += 2
                elif piege[3] == "sanglier":
                    self.joueur.bouffe += 5
                elif piege [3] == "ragondin":
                    self.joueur.bouffe += 1  

                piege[3] = "mort"
        
        
        # Compte les arbres
        self.nombre_arbre = 0
        for x in range (3):
            for y in range (3):
               self.nombre_arbre += compter_arbre(self.scenes.liste_scene[x][y].liste_arbre_roche)
        if self.nombre_arbre > 200:
            self.nombre_arbre = 200

        # Mise à jour de la vie du joueur
        self.joueur.vie_joueur(self.nombre_arbre//2)

        # Si le joueur a attaqué, active le cooldown                       
        if interraction or attaque:
            self.joueur.cooldown = False

        if pyxel.btnr(pyxel.KEY_P) and int(self.joueur.inventaire.quantite_recup("pelle")) > 0 and int(self.joueur.inventaire.quantite_recup("baton")) > 4:
            self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche = planter_arbre(self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche,self.joueur.x,self.joueur.y,self.joueur.inventaire)
        
        if pyxel.btnr(pyxel.KEY_C) and int(self.joueur.inventaire.quantite_recup("pge lap")) > 0 and self.afficher_craft_possible == 0:
            self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges = poser_piege(self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges,self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche,self.joueur.x,self.joueur.y,self.joueur.inventaire,"pge lap")
        if pyxel.btnr(pyxel.KEY_V) and int(self.joueur.inventaire.quantite_recup("pge san")) > 0 and self.afficher_craft_possible == 0:
            self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges = poser_piege(self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges,self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche,self.joueur.x,self.joueur.y,self.joueur.inventaire,"pge san")
        if pyxel.btnr(pyxel.KEY_B) and int(self.joueur.inventaire.quantite_recup("pge rag")) > 0 and self.afficher_craft_possible == 0:
            self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges = poser_piege(self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges,self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche,self.joueur.x,self.joueur.y,self.joueur.inventaire,"pge rag")

        for piege in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges:
            if piege[3] == None and pyxel.frame_count % 3000 == 0:
                piege[3] = self.animaux.prise_au_piege(piege[2])
                if piege[3] != None:
                    piege[4] = 1

        # Supprimer les arbres morts ici
        self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche = [arbre for arbre in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_arbre_roche if arbre.etat != "mort"]

        # Supprimer les batons ou pierres pris ici
        self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_baton_pierre = [b_p for b_p in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_baton_pierre if b_p.etat != "mort"]

         # Supprimer les pieges pris ici
        self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges = [piege for piege in self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]].liste_pieges if piege[3] != "mort"]

        # Mise à jour du joueur
        self.joueur.update()
        
        # Mise à jour des animaux
        self.animaux.update()

        #Mise à jour de la scène
        self.scenes.update(self.joueur)


                
    def draw_inventaire(self):
        """Affiche l’inventaire du joueur à droite de l’écran."""
        # Dessiner une barre verticale à droite
        pyxel.rect(143, 0, 50, 128, 0)  # Fond noir
        pyxel.text(148, 4, "INVENTAIRE", pyxel.frame_count % 16)  # Titre animé
        pyxel.text(145, 120, "CRAFT : R", 1)  # Titre animé

        y_offset = 20  # Position de départ pour les itemse
        for objet, quantite in self.joueur.inventaire.stockage.items():
            pyxel.text(145, y_offset, f"{objet}: {quantite}", 7)  # Texte blanc
            y_offset += 10  # Espacement vertical
    
    def draw_table_craft(self):
        """Affiche la table des crafts disponibles."""
        # Dessiner une barre verticale à droite
        pyxel.rect(143, 0, 50, 128, 0)  # Fond noir
        pyxel.text(148, 4, "CRAFTAGE", pyxel.frame_count % 16)  # Titre animé
        pyxel.text(145, 120, "INVENT : R", 1) 
        pyxel.text(145, 14, "APPUYEZ SUR", 2)  
        pyxel.text(149, 25, "FOREUSE : 1", 7)  # Texte blanc
        pyxel.text(149, 35, "HACHE : 2", 7)  # Texte blanc
        pyxel.text(149, 45, "PELLE : 3", 7)  # Texte blanc
        pyxel.text(149, 55, "PIEGE : 4", 7)  # Texte blanc
        pyxel.text(149, 65, "PIERRE : 5", 7)  # Texte blanc
        pyxel.text(149, 75, "BATON : 6", 7)  # Texte blanc

    def draw_craft(self):
        """Affiche le craft en cours selon l’objet sélectionné."""
        pyxel.rect(143, 84, 50, 42, 7)  # Fond blanc
        pyxel.text(145, 120, "RETOUR: 0", 1)  # Titre bleu
        pyxel.text(145, 114, "CRAFT: C", 1)  # Titre bleu
        if self.afficher_craft_possible == 1:
            pyxel.text(155, 85, "FOREUSE", 2)  
            pyxel.text(144, 95, "BOIS:50" + "(" + self.joueur.inventaire.quantite_recup("bois") + ")", 0)  
            pyxel.text(144, 102, "ROCHE:40"+ "(" + self.joueur.inventaire.quantite_recup("roche") + ")", 0)
            if pyxel.btnr(pyxel.KEY_C):
                self.joueur.inventaire.craft(("foreuse",1),[("bois",50),("roche",40)])  

            
        elif self.afficher_craft_possible == 2:
            pyxel.text(155, 85, "HACHE", 2)
            pyxel.text(144, 95, "BATON:20" + "(" + self.joueur.inventaire.quantite_recup("baton") + ")", 0)  
            pyxel.text(144, 102, "PIERRE:20"+ "(" + self.joueur.inventaire.quantite_recup("pierre") + ")", 0)  
            if pyxel.btnr(pyxel.KEY_C):
                self.joueur.inventaire.craft(("hache",1),[("baton",20),("pierre",20)])  

        elif self.afficher_craft_possible == 3:
            pyxel.text(155, 85, "PELLE", 2)
            pyxel.text(144, 95, "BOIS:7" + "(" + self.joueur.inventaire.quantite_recup("bois") + ")", 0)  
            pyxel.text(144, 102, "PIERRE:15"+ "(" + self.joueur.inventaire.quantite_recup("pierre") + ")", 0) 
            if pyxel.btnr(pyxel.KEY_C):
                self.joueur.inventaire.craft(("pelle",1),[("bois",7),("pierre",15)])   

        elif self.afficher_craft_possible == 4:
            pyxel.text(144, 85, "PIEGE(L,S,R)", 2)
            pyxel.text(144, 95, "BATON:20" + "(" + self.joueur.inventaire.quantite_recup("baton") + ")", 0)  
            pyxel.text(144, 102, "ROCHE:5"+ "(" + self.joueur.inventaire.quantite_recup("roche") + ")", 0) 
            pyxel.text(177, 114, "/V/B", 1)  # Titre bleu 
            if pyxel.btnr(pyxel.KEY_C):
                self.joueur.inventaire.craft(("pge lap",1),[("baton",20),("roche",5)])  
            elif pyxel.btnr(pyxel.KEY_V):
                self.joueur.inventaire.craft(("pge san",1),[("baton",20),("roche",5)])  
            elif pyxel.btnr(pyxel.KEY_B):
                self.joueur.inventaire.craft(("pge rag",1),[("baton",20),("roche",5)])  

        elif self.afficher_craft_possible == 5:
            pyxel.text(150, 85, "PIERRE x2", 2)
            pyxel.text(144, 98.5, "ROCHE:1" + "(" + self.joueur.inventaire.quantite_recup("roche") + ")", 0)  
            if pyxel.btnr(pyxel.KEY_C):
                self.joueur.inventaire.craft(("pierre",2),[("roche",1)])  

        elif self.afficher_craft_possible == 6:
            pyxel.text(150, 85, "BATON x2", 2)
            pyxel.text(144, 98.5, "BOIS:1" + "(" + self.joueur.inventaire.quantite_recup("bois") + ")", 0)  
            if pyxel.btnr(pyxel.KEY_C):
                self.joueur.inventaire.craft(("baton",2),[("bois",1)])  
            


    def draw_etat(self):
        """Affiche l’état du monde : oxygène, animaux, vie du joueur."""
        pyxel.rect(0, 0, 50, 128, 0)  # Fond noir
        pyxel.text(4, 10, "ETAT MONDE", 8)  # Titre 
        pyxel.text(2, 20, "LAPIN: " +  str(self.animaux.lapin) , 7)
        pyxel.text(2, 30, "SANGLIER: " +  str(self.animaux.sanglier) , 7)
        pyxel.text(2, 40, "RAGONDIN: " +  str(self.animaux.ragondin) , 7)
        
        
        pyxel.text(2, 60, "OXYGENE: " +  str(self.nombre_arbre//2) + "%" , 7) 

        pyxel.text(4, 80, "ETAT JOUEUR", 8)  # Titre 
        pyxel.text(2, 90, "BOUFFE: " +  str(self.joueur.bouffe) , 7)
        pyxel.text(2, 100, "VIE: " +  str(self.joueur.vie) , 7)



    def draw_map(self):
        """Affiche la carte avec la position actuelle du joueur."""
        pyxel.blt(3, 3 , 0 , 0, 184, 17, 17, 5)  
        pyxel.rect(5 + self.scenes.scene[0]*5, 6 + self.scenes.scene[1]*4, 3, 3, 2)      
    
            

    def draw(self):
        """Affiche l’état du jeu à l’écran selon la scène active."""
        if self.joueur.vie > 0:
            pyxel.bltm(0,0,0,0,0,192,128,6)
 
            # Récupérer la scène courante
            scene_actuelle = self.scenes.liste_scene[self.scenes.scene[0]][self.scenes.scene[1]]

            # Fusionner les arbres et le joueur
            elements = scene_actuelle.liste_arbre_roche + [self.joueur]
            # Tri selon la base visible (le "pied" au sol)
            elements.sort(key=lambda e: e.y_base())
            
            # Dessine les batons et les pierres
            for b_p in scene_actuelle.liste_baton_pierre:
                b_p.draw()

            for piege in scene_actuelle.liste_pieges:
                # affichage piege
                pyxel.blt(piege[0], piege[1] , 0, 66 + piege[4]*16 , 77 , 11, 7,5)

            # Dessin dans le bon ordre le joueur et les abres et rochers
            for element in elements:
                element.draw()

             # Dessiner le bouton pour l'inventaire
            pyxel.text(166.5, 4, "INV: E", 8)  # Texte rose

            # Dessiner le bouton pour la map
            pyxel.text(166.5, 12, "MAP: M", 8)  # Texte rose

            # Dessiner le bouton pour la map
            pyxel.text(163.5, 20, "ETAT: L", 8)  # Texte rose
            


            # Dessiner l'inventaire s'il est visible
            if self.afficher_inventaire:
                self.draw_inventaire()

            if self.afficher_craft:
                self.draw_table_craft()

            if self.afficher_craft_possible in [1,2,3,4,5,6]:
                self.draw_craft()

            # Dessiner l'etat du monde s'il est visible
            if self.afficher_etat:
                self.draw_etat()

            # Dessiner l'inventaire s'il est visible
            if self.afficher_map:
                self.draw_map()
        else:
            
            pyxel.cls(0)
            pyxel.text(90,64,"GAME OVER",7)

App() # LANCE LE PROGRAMME
