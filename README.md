
# Trading Journal 

Ce projet a été réalisé dans le cadre du module WebApp Predictive à la Sorbonne Université.
L’objectif est de créer une application web interactive avec Streamlit, permettant de suivre ses trades, prendre des notes quotidiennes, et visualiser sa progression à travers des indicateurs simples et une courbe d’équité.


## Sommaire
- [Objectif](#objectif)
- [Fonctionnalités](#Fonctionnalités)
- [Utilisation](#utilisation)
- [Installation](#installation)
- [Demo](#demo)
- [F.A.Q](#f.a.q)




## 🎯 Objectif 

**Trading Journal** est une application Python simple et rapide pour :
- ✏️ **Saisir ses trades** (date, heure, paire, résultat, notes)
- 🧠 **Écrire ses notes quotidiennes**
- 📊 **Visualiser ses performances** (KPIs, courbe de capital, graphiques hebdomadaires/mensuels)

Le tout, sans base de données : tout est stocké en **CSV**, donc lisible et portable.



## 🌟 Fonctionnalités principales

Quick Trade Entry : ajout rapide d’un trade (date, heure, paire, sens, prix d’entrée/sortie, lot size, notes, résultat en $).

Daily Notes : saisie du mood, résultat journalier et leçon clé de la journée.

Édition / Suppression : correction des trades et notes directement dans l’interface.

Progress Page :

Statistiques globales : nombre de trades, win rate, total des résultats ($).

Courbe d’équité (résultats cumulés dans le temps).

Résultats hebdomadaires et mensuels en graphiques.

Sauvegarde & Restauration automatiques :

Backup automatique avant chaque réinitialisation.

Restauration et import de CSV disponibles depuis l’interface.




    🧠 Stack technique

Python 3.11+

Streamlit — Interface web interactive

Pandas — Manipulation et stockage des données

Altair — Visualisation des performances


## 💡 Utilisation rapide

Onglet Journal → saisir un trade via Quick Trade Entry → Add trade.

Renseigner une Daily Note (mood, résultat, leçon du jour).

Onglet Progress → visualiser :

la courbe d’équité (somme cumulée des résultats),

les résultats hebdomadaires et mensuels,

les indicateurs clés (nombre de trades, win rate, total P/L).

Dans la sidebar, section Data Safety :

🛟 Backup now → créer une sauvegarde,

↩️ Restore last backup → restaurer la dernière version,

🗑️ Reset ALL data (with backup) → réinitialiser après backup.


## 🚀 Installation 

###  Cloner le dépôt
git clone https://github.com/chaina9114-a11y/projet-python-1

###  Créer un environnement virtuel (facultatif)
conda create -n trading_env python=3.11
conda activate trading_env

### Installer les dépendances
pip install -r requirements.txt

### Lancer l’application
streamlit run app.py

L’application s’ouvre automatiquement dans le navigateur 

🌐Sinon, copiez le lien affiché dans le terminal (généralement http://localhost:8501).


 

    
---

## 📹 Video de démonstration 

Dure environ : 4:45 minutes 

Contenu : problématique création application, démonstration des fonctionnalités, explication du code. 


Lien Google drive : https://drive.google.com/file/d/1Wo_1pjfd2DDq0C1r8kgTnwjeSYEQrZ-k/view?usp=drivesdk

##  Auteur 

Nom : Chaina Spusteck & Leslie Tagne

Groupe : Projet WebApp Predictive- Data-Sorbonne 

Année universitaire : 2025-2026


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

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](<STREAMLIT_SHARE_URL>)




