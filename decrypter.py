import random
import os
from typing import List
import heapq
import string


def lire_fichier(fichier: str) -> list: 
    #  lire le contenu d'un fichier et à le convertir en une liste d'octets. La fonction lire_fichier est utilisée à cette fin. Elle lit le fichier, applique une opération XOR avec 0x30 à chaque octet, et renvoie la liste d'octets.

    """
    ---> Lit le contenu d'un fichier et le convertit en liste d'octets.
    Parameters:
        fichier (str): le chemin d'accès du fichier à lire
    Returns:
        la liste d'octets représentant le contenu du fichier
    Raises:
        ValueError: si le fichier n'existe pas ou est inaccessible
    """
  
    # Ouvre un fichier et lit son contenu
    try : 
     with open(fichier, 'r') as f:
        contenu = f.read()
    # Applique une opération XOR avec 0x30 sur chaque octet du contenu
        octets = [b ^ 0x30 for b in contenu.encode()]
     return octets
    except FileNotFoundError:
        raise ValueError(f"Le fichier '{fichier}' n'existe pas.")
    except PermissionError:
        raise ValueError(f"Le fichier '{fichier}' est inaccessible.")



def ecrire_fichier_binaire(fichier: str, octets: list):
    """
    Écrit un fichier binaire à partir d'une liste d'octets.

    Parameters:
        fichier (str): le chemin d'accès du fichier à écrire
        octets (list): la liste d'octets à écrire dans le fichier binaire

    Raises:
        ValueError: si le fichier n'existe pas ou est inaccessible
    """
    # Convertit une liste d'octets en chaîne de caractères en appliquant une opération OR avec 0x30
    try:
      sortie = ''.join([chr(b | 0x30) for b in octets])
    # Écrit la chaîne obtenue dans un fichier
      with open(fichier, 'w') as f:
          f.write(sortie)
    except FileNotFoundError:
         raise ValueError(f"Le fichier '{fichier}' n'existe pas.")
    except PermissionError:
        raise ValueError(f"Le fichier '{fichier}' est inaccessible.")



def ecrire_fichier_texte(fichier: str, ascii: str):
    """
    Écrit un fichier texte à partir d'une chaîne de caractères ASCII.

    Parameters:
        fichier (str): le chemin d'accès du fichier à écrire
        ascii (str): la chaîne de caractères ASCII à écrire dans le fichier texte

    Raises:
        ValueError: si le fichier n'existe pas ou est inaccessible
    """
    # Écrit une chaîne de caractères dans un fichier
    try:
      with open(fichier, 'w') as f:
          f.write(ascii)
    except FileNotFoundError:
         raise ValueError(f"Le fichier '{fichier}' n'existe pas.")
    except PermissionError:
        raise ValueError(f"Le fichier '{fichier}' est inaccessible.")      
 

def hamming(c1: int, c2: int, c3: int, c4: int, c5: int, c6: int, c7: int) -> int:
    """
    Calcule le nombre d'erreurs de Hamming sur 7 octets.

    Parameters:
        c1, c2, c3, c4, c5, c6, c7 (int): les 7 octets à tester

     parite pair = 0 , parite impair = 1

    Returns:
        le nombre d'erreurs de Hamming, ou 0 si aucune erreur n'est détectée

    Raises:
        ValueError: si une valeur n'est pas un octet valide (0 à 255)
    """
    try:
        # Calcule les bits de parité et détermine si une correction est nécessaire
        p1 = c1 ^ c2 ^ c3
        p2 = c1 ^ c2 ^ c4
        p3 = c2 ^ c3 ^ c4
        # Utilise les bits de parité pour identifier et corriger une erreur éventuelle
        if c5!= p1 and c6!= p2 and not (c7!= p3):
            return 1
        elif c5!= p1 and c6!= p2 and c7!= p3:
            return 2
        elif c5!= p1 and not (c6!= p2) and c7!= p3:
            return 3
        elif not (c5!= p1) and c6!= p2 and c7!= p3:
            return 4
        else:
            return 0
    except ValueError:
        # Capture l'exception ValueError et affiche un message d'erreur personnalisé
        print("Erreur : une ou plusieurs valeurs d'entrée ne sont pas des octets valides (entre 0 et 255)")
    




def corriger_erreurs(entre: list) -> list:
    """
    Corrige les erreurs de Hamming dans une liste d'octets.

    Parameters:
        entre (list): la liste d'octets à corriger

    Returns:
        la liste d'octets corrigée

    Raises:
        ValueError: si une valeur n'est pas un octet valide (0 à 255)
    """
    # Parcourt la liste d'entrée et applique la correction d'erreur de Hamming si nécessaire
    corrige = []
    erreurs = []
    i = 0
    while i + 7 < len(entre):
        c = hamming(entre[i], entre[i+1], entre[i+2], entre[i+3], entre[i+4], entre[i+5], entre[i+6])
        if c != 0:
            erreurs.append(i + c)
            corrige.append(entre[i] ^ 0x01)
        else:
            corrige.append(entre[i])
        for j in range(1, 7):
            corrige.append(entre[i+j])
        i += 7
    return corrige, erreurs






def reduire(entre: list) -> list:
    """
    Réduit une liste d'octets en supprimant les bits de contrôle.

    Parameters:
        entre (list): la liste d'octets à réduire

    Returns:
        la liste réduite

    Raises:
        ValueError: si une valeur n'est pas un octet valide (0 à 255)
    """
    reduit = []
    i = 0
    while i + 7 <= len(entre):
        for j in range(4):
            reduit.append(entre[i+j])
        i += 7
    return reduit




def regrouper_octets(octets: list) -> list:
    """
    Regroupes les octets en blocs de 8 bits.

    Parameters:
        octets (list): la liste d'octets à regrouper

    Returns:
        la liste regroupée

    Raises:
        ValueError: si une valeur n'est pas un octet valide (0 à 255)
    """
    groupe = []
    i = 0
    b = 0
    for octet in octets:
        b = (b << 1) | octet
        i += 1
        if i == 8:
            groupe.append(b)
            b = 0
            i = 0
    return groupe





def convertir_en_ascii(entre: list) -> str:
    """
    Convertit une liste d'octets en chaîne de caractères ASCII.

    Parameters:
        entre (list): la liste d'octets à convertir

    Returns:
        la chaîne de caractères ASCII

    Raises:
        ValueError: si une valeur n'est pas un octet valide (0 à 255)
    """
    # Convertit une liste d'octets en chaîne de caractères ASCII
    s = ''.join([chr(b) for b in regrouper_octets(entre)])
    return s





def dechiffrer(entre: str) -> str:
    """
    Déchiffre une lettre chiffrée avec le chiffrement de Vigenère.

    Parameters:
        entre (str): la lettre chiffrée

    Returns:
        la lettre déchiffrée

    Raises:
        ValueError: si la clé de chiffrement est incorrecte
    """
    cle = "python"
    ecart = [ord(c) for c in cle]
    dechiffre = ""
    i = 0
    for c in entre:
        b = ord('a') if 'a' <= c <= 'z' else ord('A') if 'A' <= c <= 'Z' else 0
        if b!= 0:
            l = ord(c) - b
            k = ecart[i] - ord('a')
            d = chr((l + 26 - k) % 26 + b)
            dechiffre += d
            i = (i + 1) % len(cle)
        else:
            dechiffre += c
    return dechiffre





def convertir_en_bin(entre: str) -> list:
    """
    Convertit une chaîne de caractères en liste d'octets binaires.

    Parameters:
        entre (str): la chaîne de caractères à convertir

    Returns:
        la liste d'octets binaires

    Raises:
        ValueError: si une valeur n'est pas un caractère ASCII valide
    """
    # Convertit une chaîne de caractères en liste d'octets binaires
    bin = []
    for c in entre.encode():
        for i in range(8):
            bin.append((c >> (7 - i)) & 1)
    return bin




def chiffrer(entre: str) -> tuple:
    """
    Chiffre une lettre avec une variante de chiffrement de Vigenère.

    Parameters:
        entre (str): la lettre à chiffrer

    Returns:
        une tuple contenant le texte chiffré et la clé de chiffrement

    Raises:
        ValueError: si la clé de chiffrement est incorrecte
    """

    # chiffrement de Vigenère avec une clé fixe est vulnérable à une attaque par force brute. 
    # Pour améliorer la sécurité, jutilise une clé aléatoire de la même longueur que le message à chiffrer :
    
    cle = ''.join(random.choice(string.ascii_letters) for _ in range(len(entre)))
    #cle = "python"
    
    ecart = [ord(c) for c in cle]
    chiffre = []
    i = 0
    for c in entre:
        b = ord('a') if 'a' <= c <= 'z' else ord('A') if 'A' <= c <= 'Z' else 0
        if b != 0:
            l = ord(c) - b
            k = ecart[i] - ord('a')
            d = chr((l + 26 - k) % 26 + b)
            chiffre.append(d)
            i = (i + 1) % len(cle)
        else:
            chiffre.append(c)
    return (''.join(chiffre), cle)




class Noeud:
    def __init__(self, gauche=None, droite=None, frequence=0, valeur=None):
        self.gauche = gauche
        self.droite = droite
        self.frequence = frequence
        self.valeur = valeur
#classe Noeud est définie pour représenter un nœud dans l'arbre de Huffman. Chaque nœud a une valeur  et des références à ses enfants gauche et droit. 

 
    def est_feuille(self): #La méthode est_feuille vérifie si le nœud est une feuille (il n'a pas d'enfants). 
        return self.gauche is None and self.droite is None
    
    def __lt__(self, other): #La méthode __lt__ est utilisée pour comparer deux nœuds en fonction de leur valeur, ce qui est nécessaire pour construire l'arbre de Huffman.
        return self.frequence < other.frequence



def compresser(texte):
    # Initialise un dictionnaire pour stocker les fréquences de chaque caractère dans le texte
    frequences = {}
    for car in texte:
        if car not in frequences:
            # Si le caractère n'est pas encore dans le dictionnaire, ajoute-le avec une fréquence de 0
            frequences[car] = 0
        # Incrémente la fréquence du caractère dans le dictionnaire
        frequences[car] += 1

    # Initialise un tas vide pour stocker les nœuds de l'arbre de Huffman
    tas = []
    for car, freq in frequences.items():
        # Crée un nouveau nœud avec le caractère et sa fréquence, et l'ajoute au tas
        noeud = Noeud(None, None, freq, car)
        heapq.heappush(tas, noeud)

    # Tant qu'il reste plus d'un nœud dans le tas, répète la boucle suivante :
    while len(tas) > 1:
        # Retire les deux nœuds de fréquence la plus basse du tas
        noeud1 = heapq.heappop(tas)
        noeud2 = heapq.heappop(tas)
        # Crée un nouveau nœud avec les deux nœuds précédents comme enfants, et avec une fréquence égale à la somme des fréquences des enfants
        nouveau_noeud = Noeud(noeud1, noeud2, noeud1.frequence + noeud2.frequence)
        # Ajoute le nouveau nœud au tas
        heapq.heappush(tas, nouveau_noeud)

    # Récupère l'arbre de Huffman final (qui est le seul nœud restant dans le tas)
    arbre_huffman = tas[0]

    # Initialise un dictionnaire pour stocker les codes binaires de chaque caractère
    code = {}
    def parcourir(noeud, code_binaire):
        # Si le nœud est une feuille (c'est-à-dire qu'il représente un caractère), ajoute le code binaire correspondant au dictionnaire
        if noeud.est_feuille():
            code[noeud.valeur] = code_binaire
        else:
            # Sinon, répète la fonction parcourir récursivement sur les enfants gauche et droit du nœud, en ajoutant '0' ou '1' au code binaire
            parcourir(noeud.gauche, code_binaire + '0')
            parcourir(noeud.droite, code_binaire + '1')

    # Appelle la fonction parcourir sur l'arbre de Huffman pour remplir le dictionnaire de codes binaires
    parcourir(arbre_huffman, '')

    # Parcourt le texte et remplace chaque caractère par son code binaire correspondant
    texte_comprime = ''
    for car in texte:
        code_binaire = code[car]
        texte_comprime += code_binaire

    # Retourne le texte compressé et le code Huffman
    return texte_comprime, code


def decompresser(texte_comprime, code):
    # Crée un dictionnaire de codes inversé à partir du code Huffman
    code_inverse = {v: k for k, v in code.items()}

    texte_decompresse = ''
    code_binaire = ''

    # Parcourt le texte compressé
    for bit in texte_comprime:
        # Ajoute le bit au code binaire
        code_binaire += bit

        # Si le code binaire est dans le dictionnaire de codes inversé
        if code_binaire in code_inverse:
            # Ajoute le caractère correspondant au texte décompressé
            caractere = code_inverse[code_binaire]
            texte_decompresse += caractere
            # Réinitialise le code binaire
            code_binaire = ''

    return texte_decompresse



def dechiffrer_message_decompresse(texte_decompresse: str, cle: str) -> str:
    """
    Déchiffre le texte décompressé à l'aide de la clé de chiffrement.

    Parameters:
        texte_decompresse (str): le texte décompressé à déchiffrer
        cle (str): la clé de chiffrement

    Returns:
        le texte déchiffré
    """
# Convertit chaque caractère de la clé en son équivalent ASCII et stocke le résultat dans une liste
    ecart = [ord(c) for c in cle]

    # Initialise une chaîne vide pour stocker le texte déchiffré
    texte_dechiffre = ""

    # Initialise un compteur pour parcourir la clé
    i = 0

    # Parcourt chaque caractère du texte décompressé
    for c in texte_decompresse:

        # Détermine si le caractère est une lettre minuscule, une lettre majuscule ou un autre caractère
        # et stocke son équivalent ASCII dans la variable b
        b = ord('a') if 'a' <= c <= 'z' else ord('A') if 'A' <= c <= 'Z' else 0

        # Si le caractère est une lettre (minuscule ou majuscule)
        if b != 0:

            # Calcule l'indice de décalage dans l'alphabet en utilisant la formule de déchiffrement de Vigenère
            l = ord(c) - b
            k = ecart[i] - ord('a')
            d = chr((l + 26 - k) % 26 + b)

            # Ajoute la lettre déchiffrée au texte déchiffré
            texte_dechiffre += d

            # Incrémente le compteur pour passer au caractère suivant de la clé
            i = (i + 1) % len(cle)

        # Si le caractère n'est pas une lettre, il est laissé inchangé
        else:
            texte_dechiffre += c

    # Retourne le texte déchiffré
    return texte_dechiffre




def main():
    erreurs = []

    # Lecture du fichier
    try:
        bits_entree = lire_fichier("code.txt")
        print("Étape 1 : Lecture du fichier")
        print("Bits lus :", bits_entree)
    except Exception as e:
        erreurs.append(f"Erreur lors de la lecture du fichier : {str(e)}")

    # Correction des erreurs
    try:
        bits_corriges, erreurs_positions = corriger_erreurs(bits_entree)
        print("\nÉtape 2 : Correction des erreurs")
        print("Bits corrigés :", bits_corriges)
        if erreurs_positions:
            print("Erreurs détectées et corrigées aux positions :", erreurs_positions)
        else:
            print("Aucune erreur détectée.")
    except Exception as e:
        erreurs.append(f"Erreur lors de la correction des erreurs : {str(e)}")

    # Réduction de l'encodage
    try:
        bits_reduits = reduire(bits_corriges)
        print("\nÉtape 3 : Réduction de l'encodage")
        print("Bits réduits :", bits_reduits)
    except Exception as e:
        erreurs.append(f"Erreur lors de la réduction de l'encodage : {str(e)}")

    # Conversion en ASCII
    try:
        caracteres_ascii = convertir_en_ascii(bits_reduits)
        print("\nÉtape 4 : Conversion en ASCII")
        print("Caractères ASCII :", caracteres_ascii)
    except Exception as e:
        erreurs.append(f"Erreur lors de la conversion en ASCII : {str(e)}")

    # Déchiffrement
    try:
        texte_dechiffre = dechiffrer(caracteres_ascii)
        print("\nÉtape 5 : Déchiffrement")
        print("Texte déchiffré :", texte_dechiffre)
    except Exception as e:
        erreurs.append(f"Erreur lors du déchiffrement : {str(e)}")

    # Chiffrement avec variante
    try:
        texte_chiffre, cle = chiffrer(texte_dechiffre)
        print("\nÉtape 6 : Chiffrement avec variante")
        print("Texte chiffré :", texte_chiffre)
        print("Clé de chiffrement :", cle)
    except Exception as e:
        erreurs.append(f"Erreur lors du chiffrement avec variante : {str(e)}")

    # Compression du texte
    try:
        texte_comprime, code = compresser(texte_chiffre)
        print("\nÉtape 7 : Compression du texte")
        print("Texte compressé :", texte_comprime)
    except Exception as e:
        erreurs.append(f"Erreur lors de la compression du texte : {str(e)}")

    try:
        texte_decompresse = decompresser(texte_comprime, code)
        print("\nÉtape 8 : Décompression du texte")
        print("Texte décompressé :", texte_decompresse)
    except Exception as e:
        erreurs.append(f"Erreur lors de la compression/décompression du texte : {str(e)}")
     
    # Déchiffrement du message décompressé
    #cle= "python"
    #texte_dechiffre = dechiffrer_message_decompresse(texte_decompresse, cle)
    #print("\nÉtape 9 : Déchiffrement du message décompressé")
    #print("Texte déchiffré :", texte_dechiffre)

    # Affichage des erreurs
    if erreurs:
        print("\nErreurs rencontrées :")
        for erreur in erreurs:
            print(erreur)




if __name__ == "__main__":
    main()