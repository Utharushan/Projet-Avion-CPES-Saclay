from random import randint

class Avion:
    """
    Prend en entrée un indice (str), un entier heures (autonomie), deux booléens pirate et feu
    ------------------------------------------------------------------------------------------------
    Représente un avion avec ses informations de priorité d’atterrissage
    ------------------------------------------------------------------------------------------------
    Initialise un avion avec ses attributs d'identifiant, d’autonomie, de sécurité et de feu
    """
    def __init__(self, indice, heures=0, pirate=False, feu=False):
        self.ind = indice  # Identifiant de l'avion
        self.H = heures  # Autonomie en heures de vol
        self.P = pirate  # Pirate à bord
        self.F = feu  # Feu à bord
        self.poids = self.priorite()

    def priorite(self):
        """Calcule la priorité d'un avion basée sur le feu, le pirate et l'autonomie."""
        count = 0
        if self.F:
            count += 6  # Priorité élevée si feu à bord
        if self.P:
            count += 3  # Priorité accrue si pirate à bord
        if self.H <= 3:
            if self.H in (0, 1):
                count += 5  # Urgence si peu de carburant
            else:
                count += 3
        else:
            count += 1  # Moins prioritaire si plus de 3 heures d'autonomie

        return count

    def __repr__(self):
        """Représentation textuelle de l'avion."""
        return f"Avion {self.ind}:Poids={self.poids}, Pirate={self.P}" #  Feu={self.F}, Autonomie={self.H}h, 


class TAS:
    """
    ------------------------------------------------------------------------------------------------
    Classe abstraite pour les structures de tas
    ------------------------------------------------------------------------------------------------
    Implémente les méthodes de base d’un tas
    """
    def __init__(self):
        raise NotImplementedError

class Vide(TAS):
    """
    Hérite de la classe TAS
    ------------------------------------------------------------------------------------------------
    Classe représentant un tas vide utilisé comme noeud terminal dans la structure de tas
    ------------------------------------------------------------------------------------------------
    Implémente les comportements d’un tas vide
    """
    def __init__(self):
        pass

    def afficher(self, hauteur=1, rep=""):
        return hauteur * "  " + "|-->x\n"

    def fusion(self, autre):
        return autre

    def minimum(self):
        return None

    def appartient(self, avion):
        return False

    def taille(self):
        return 0

    def hauteur(self):
        return 0

    def ajouter(self, avion):
        return Noeud(Vide(), avion, Vide())

    def supprimer(self):
        return Vide()

    def supprimer_avion(self, indice):
        return Vide()

    def tas_to_liste(self):
        return []

    def detourne(self, avion, t_detourne):
        return self, [], []

class Noeud(TAS):
    """
    Prend en entrée un sous-arbre gauche (TAS), un objet avion (Avion), et un sous-arbre droit (TAS)
    ------------------------------------------------------------------------------------------------
    Représente un nœud dans un tas contenant un avion avec des méthodes de gestion
    ------------------------------------------------------------------------------------------------
    Initialise le nœud avec les avions et gère les priorités dans la structure
    """
    def __init__(self, gauche, avion, droite):
        self.gauche = gauche
        self.avion = avion
        self.droite = droite

    def afficher(self, hauteur=1, rep=""):
        """
        Prend en entrée un entier hauteur et un str rep
        --------------------------------------------------------------------------------------------
        Affiche le tas de manière structurée en utilisant une représentation
        visuelle de l'arbre.
        --------------------------------------------------------------------------------------------
        Renvoie une chaîne de caractères représentant la structure de l'arbre
        """
        rep = hauteur * "  " + "|-->" + str(self.avion) + "," + str(hauteur) + "\n"
        repgauche = self.gauche.afficher(hauteur + 1, rep)
        rep += repgauche
        repdroite = self.droite.afficher(hauteur + 1, rep)
        rep += repdroite
        return rep

    def fusion(self, autre):
        """
        Prend en entrée un autre tas de type TAS
        --------------------------------------------------------------------------------------------
        Fusionne le tas actuel avec un autre tas en maintenant les priorités
        de manière récursive.
        --------------------------------------------------------------------------------------------
        Renvoie un nouveau tas fusionné en fonction des priorités des éléments
        """
        if isinstance(autre, Vide):
            return self
        if self.avion.priorite() >= autre.avion.priorite():
            nouveau_noeud = Noeud(self.gauche, self.avion, self.droite.fusion(autre))
            if nouveau_noeud.gauche.hauteur() < nouveau_noeud.droite.hauteur():
                nouveau_noeud.gauche, nouveau_noeud.droite = nouveau_noeud.droite, nouveau_noeud.gauche
            return nouveau_noeud
        else:
            return autre.fusion(self)

    def minimum(self):
        """
        --------------------------------------------------------------------------------------------
        Renvoie l'avion avec la priorité la plus élevée dans le tas (le minimum)
        --------------------------------------------------------------------------------------------
        """
        return self.avion  # L'avion avec la plus haute priorité

    def appartient(self, x):
        """
        Prend en entrée un identifiant d'avion x
       --------------------------------------------------------------------------------------------
        Vérifie si un avion avec l'identifiant x est présent dans le tas
        --------------------------------------------------------------------------------------------
        Renvoie True si l'avion est trouvé, sinon False
        """
        if self.avion.ind == x:
            return True
        else:
            return self.gauche.appartient(x) or self.droite.appartient(x)

    def taille(self):
        """
        --------------------------------------------------------------------------------------------
        Calcule et renvoie la taille totale du tas (nombre de nœuds)
        --------------------------------------------------------------------------------------------
        """
        return 1 + self.gauche.taille() + self.droite.taille()

    def hauteur(self):
        """
        --------------------------------------------------------------------------------------------
        Calcule la hauteur du tas en tenant compte des sous-arbres gauche et droit
        --------------------------------------------------------------------------------------------
        """
        if isinstance(self.gauche, Vide) and isinstance(self.droite, Vide):
            return 1
        elif isinstance(self.gauche, Vide):
            return 1 + self.droite.hauteur()
        elif isinstance(self.droite, Vide):
            return 1 + self.gauche.hauteur()
        else:
            return 1 + max(self.gauche.hauteur(), self.droite.hauteur())
        
    def ajouter(self, avion):
        """
        Prend en entrée un objet avion de type Avion
        --------------------------------------------------------------------------------------------
        Ajoute l'avion au tas en effectuant une fusion pour maintenir l'ordre
        de priorité.
        --------------------------------------------------------------------------------------------
        Renvoie un nouveau tas avec l'avion ajouté
        """
        nouveau_noeud = Noeud(Vide(), avion, Vide())
        return self.fusion(nouveau_noeud)

    def supprimer(self):
        """
        --------------------------------------------------------------------------------------------
        Supprime le noeud racine (élément minimal) et fusionne les sous-arbres gauche
        et droit pour maintenir la structure du tas.
        --------------------------------------------------------------------------------------------
        Renvoie un nouveau tas avec le minimum supprimé
        """
        return self.gauche.fusion(self.droite)

    def supprimer_avion(self, indice):
        """
        Prend en entrée un identifiant d'avion indice
        --------------------------------------------------------------------------------------------
        Supprime un avion spécifique du tas en fonction de son identifiant
        --------------------------------------------------------------------------------------------
        Renvoie un nouveau tas sans l'avion correspondant
        """
        if self.avion.ind == indice:
            return self.supprimer()
        else:
            self.gauche = self.gauche.supprimer_avion(indice)
            self.droite = self.droite.supprimer_avion(indice)
            return self

    def tas_to_liste(self):
        """
        --------------------------------------------------------------------------------------------
        Convertit le tas en une liste ordonnée en fonction des priorités
        --------------------------------------------------------------------------------------------
        Renvoie une liste contenant les avions triés par priorité
        """
        elements = []
        tas_temp = self
        while not isinstance(tas_temp, Vide):
            min_avion = tas_temp.minimum()  
            elements.append(min_avion)
            tas_temp = tas_temp.supprimer()  
        return elements

    def detourne(self, avion, t_detourne):
        """
        Prend en entrée un avion de type Avion et une liste t_detourne
        --------------------------------------------------------------------------------------------
        Avec une probabilité de 30%, supprime un avion piraté du tas et
        l’ajoute à la liste des avions détournés
        --------------------------------------------------------------------------------------------
        Renvoie le tas mis à jour, la liste triée des avions, et la liste des avions détournés
        """
        v = randint(1, 100)
        if v <= 30:
            self = self.supprimer_avion(avion.ind)
            t_detourne.append(avion)
        tab = self.tas_to_liste()
        return self, tab, t_detourne


if __name__ == "__main__":
    # Test 1: Ajout d'avions avec différentes priorités
    tas = Vide()
    avion1 = Avion("PlaneA", heures=2, pirate=True, feu=False)
    avion2 = Avion("PlaneB", heures=4, pirate=False, feu=True)
    avion3 = Avion("PlaneC", heures=1, pirate=False, feu=False)
    tas = tas.ajouter(avion1)
    tas = tas.ajouter(avion2)
    tas = tas.ajouter(avion3)

    print("Test 1: Ajout d'avions")
    assert tas.minimum() == avion2, "Erreur: L'avion avec le feu doit avoir la plus haute priorité"
    assert tas.taille() == 3, "Erreur: Il doit y avoir 3 avions dans le tas"
    print("Test 1 réussi.\n")

    # Test 2: Suppression de l'avion avec la plus haute priorité
    print("Test 2: Suppression du minimum")
    tas = tas.supprimer()
    assert tas.minimum() == avion1, "Erreur: L'avion suivant avec pirate devrait être le minimum"
    assert tas.taille() == 2, "Erreur: Il doit y avoir 2 avions dans le tas après suppression"
    print("Test 2 réussi.\n")

    # Test 3: Fusion de deux tas
    tas1 = Vide().ajouter(Avion("PlaneX", heures=2, pirate=False, feu=True))
    tas2 = Vide().ajouter(Avion("PlaneY", heures=5, pirate=True, feu=False))
    tas_fusion = tas1.fusion(tas2)
    print("Test 3: Fusion de deux tas")
    assert tas_fusion.minimum().ind == "PlaneX", "Erreur: PlaneX devrait avoir la plus haute priorité dans la fusion"
    assert tas_fusion.taille() == 2, "Erreur: La taille après fusion devrait être 2"
    print("Test 3 réussi.\n")

    # Test 4: Suppression d'un avion spécifique (ex. pirate)
    print("Test 4: Suppression d'un avion spécifique")
    tas = tas.ajouter(Avion("PlaneD", heures=3, pirate=True, feu=False))
    tas = tas.supprimer_avion("PlaneD")
    assert not tas.appartient("PlaneD"), "Erreur: PlaneD devrait être supprimé du tas"
    print("Test 4 réussi.\n")

