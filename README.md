# 📘 README – Jeu de Survie Écologique

## 🎮 Présentation
Ce projet est un **jeu de survie** développé en Python avec la bibliothèque **Pyxel**.  
Le joueur doit survivre dans un environnement naturel tout en évitant de surexploiter les ressources qui l’entourent.  
Il s’agit d’un jeu à **forte dimension écologique**, visant à sensibiliser aux conséquences des actions humaines sur l’environnement.

## 🌍 Objectif du jeu
- **Survivre** le plus longtemps possible.
- Gérer sa **nourriture**, ses **outils** et son **environnement**.
- Ne pas surexploiter les **animaux** ni couper trop d’**arbres** :
  - Trop chasser → disparition d’une espèce → plus de nourriture.
  - Trop couper d’arbres → baisse d’oxygène → perte de vie.

## 🧱 Fonctionnalités principales
- Déplacement libre dans une **carte en 3x3 scènes**.
- Système de **craft**, **inventaire** et **collecte de ressources**.
- Interaction avec l’environnement : arbres, rochers, animaux, pièges.
- **Interface graphique** complète avec gestion des états et affichages dynamiques.

## ⚙️ Dépendances
- Python 3
- [Pyxel](https://github.com/kitao/pyxel) (installable via `pip install pyxel`)
- fichier 1.pyxres présent dans le dossier (sprite)

## ▶️ Lancement du jeu
1. Installer Pyxel :
   ```bash
   pip install pyxel

2. Lancer le fichier :
   ```bash
   python jeu_projet_nsi.py
   
   
## ⌨️ Commandes
| Action                    | Touche / Souris    |
| ------------------------- | ------------------ |
| Déplacement               | `Z`, `Q`, `S`, `D` |
| Attaque (ex : hache)      | Clic gauche        |
| Ramasser / Interagir      | Clic droit         |
| Inventaire                | `E`                |
| Interface Craft           | `R`                |
| Craft dans interface      | `C` (`V`,`B)(piege)|
| Carte                     | `M`                |
| État du monde             | `L`                |
| Planter arbre si pelle/bat| `P`                |
| Utiliser foreuse          | `F`                |
| Poser piège (lap/san/rag) | `C`, `V`, `B`      |

## ❗ Avertissements
-Si tous les arbres sont coupés → perte d’oxygène → mort / possibilité d'en planter avec une pelle et 5 de batons.
-Si une espèce disparaît → plus de nourriture possible via pièges.
-Pas de système de sauvegarde pour le moment.

## 💡 Auteur
Projet réalisé dans le cadre de l’enseignement NSI (Numérique et Sciences Informatiques) – Terminale au lycée Notre-Dame-de-Rezé – 2025.
Développement en solo par LECHAT Calvin.
Moteur utilisé : Pyxel
Langage : Python 3
