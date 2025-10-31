
# Trading Journal 

Notre application est une webapp Streamlit qui à pour but d'aider les traders à suivre leurs trades, leurs notes quotidiennes ainsi que leurs progression dans le temps.

## Sommaire
- [Objectif](#objectif)
- [Aperçu](#aperçu)
- [Structure](#structure)
- [Interface](#interface)
- [Badges](#badges)

## 🎯 Objectif

**Trading Journal** est une application Python simple et rapide pour :
- ✏️ **Saisir ses trades** (date, heure, paire, résultat, notes)
- 🧠 **Écrire ses notes quotidiennes**
- 📊 **Visualiser ses performances** (KPIs, courbe de capital, graphiques hebdomadaires/mensuels)

Le tout, sans base de données : tout est stocké en **CSV**, donc lisible et portable.

## 🌟 Aperçu

Le projet Trading Journal est une webapp Streamlit qui permet de suivre vos trades et vos notes quotidiennes de manière simple et efficace.

Points clés :

2 fichiers CSV dans /data : trades.csv (tous les trades) et daily.csv (notes quotidiennes)

Page “Journal” : saisie rapide des trades, notes du jour, édition et suppression des entrées

Page “Progress” : aperçu global avec KPIs, equity curve animée (~2 secondes), totaux hebdomadaires et mensuels

Performance : uniquement la colonne result_usd est utilisée pour calculer les stats et la courbe d’equity

Les colonnes id et strategy sont masquées dans l’interface mais présentes dans les CSV pour compatibilité


## 🧠 Structure & Code

Le projet tient dans un seul fichier : `app.py`, avec une structure simple et robuste.

### 🔹 Interface Streamlit
- **Sidebar** : navigation entre *Journal* et *Progress*, + bouton “Reset data”  
- **Page Journal** : saisie rapide avec formulaire, édition dans un tableau  
- **Page Progress** : calcul automatique de la colonne `_pl_for_stats` et somme cumulée pour l’equity curve  


# Installation

### 1️⃣ Cloner le dépôt
git clone https://github.com/chaina9114-a11y/projet-python-1

### 2️⃣ Se déplacer dans le dossier du projet
cd project-python-1

### 4️⃣ Installer les dépendances
pip install -r requirements.txt

### 5️⃣ Lancer le projet
python main.py

    
## FAQ – Trading Journal

#### 🐍 Faut-il installer Python pour utiliser l’application ?


Oui, l’application nécessite Python.
Installe également les dépendances avec : pip install -r requirements.txt


#### 🚀 Comment lancer l’application ?

Dans le dossier du projet : streamlit run app.py

#### 🔒 Est-ce sécurisé ?

Le projet est 100% local.
Les données restent sur ton ordinateur et aucune connexion externe n’est utilisée.


## Badges

![Python](https://img.shields.io/badge/Python-3.11-blue)




