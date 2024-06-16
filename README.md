Ce projet est un décodeur pour un fichier binaire crypté en utilisant différentes techniques cryptographiques. Le code est écrit en Python et utilise des bibliothèques standard telles que random, os, typing, heapq et string.
Fonctionnalités

Le décodeur prend en entrée un fichier binaire crypté et effectue les opérations suivantes :

    Lit le contenu du fichier et le convertit en une liste d'octets.
    Corrige les erreurs de transmission dans les données en utilisant le code de Hamming.
    Réduit l'encodage en supprimant les bits de contrôle.
    Regroupe les octets en blocs de 8 bits et convertit les données en chaîne de caractères ASCII.
    Déchiffre la chaîne de caractères en utilisant le chiffrement de Vigenère avec une clé fixe.
    Chiffre la chaîne de caractères déchiffrée en utilisant une variante de chiffrement de Vigenère avec une clé aléatoire.
    Compresse la chaîne de caractères chiffrée en utilisant l'algorithme de compression de Huffman.
    Décompresser le message à la fin.

Utilisation

Pour utiliser le décodeur, exécutez le fichier Python "decrypter.py" dans un terminal en utilisant la commande suivante :

python decrypter.py

Le décodeur lit le fichier "code.txt" dans le répertoire courant et affiche les résultats des différentes étapes de décodage dans la console.
Structure du code

Le code est structuré en plusieurs fonctions, chacune effectuant une tâche spécifique. Les fonctions sont documentées avec des docstrings décrivant leur fonctionnalité, leurs paramètres et leurs valeurs de retour.

Le code utilise également des exceptions pour gérer les erreurs et les conditions exceptionnelles. Les exceptions sont levées lorsque des erreurs se produisent et sont gérées dans la fonction principale "main()".
Dépendances

Le code utilise les bibliothèques standard de Python suivantes :

    random : pour générer des clés aléatoires pour le chiffrement de Vigenère.
    os : pour interagir avec le système d'exploitation.
    typing : pour définir les types de données des paramètres et des valeurs de retour des fonctions.
    heapq : pour implémenter l'algorithme de compression de Huffman.
    string : pour générer des clés aléatoires pour le chiffrement de Vigenère.

Le code ne dépend pas de bibliothèques externes.
Auteur

Le code a été écrit par moi, étudiant en première année de Master BDIA à l'Université de Technologie de Bourgogne.
