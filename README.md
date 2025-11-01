# 🗒️ Trading Journal — Projet WebApp (Sorbonne)

## 🔗 [🎯 Objectif](#-objectifs)
Ce projet a été réalisé dans le cadre du module **WebApp Predictive** à la **Sorbonne Université**.  
L’objectif est de créer une **application web interactive** avec **Streamlit**, permettant à l’utilisateur de **suivre ses trades**, **écrire des notes quotidiennes** et **visualiser sa progression** à travers des statistiques et une courbe d’équité.

---

## 🔗 [✨ Fonctionnalités principales](#-fonctionnalités-principales)

- **Quick Trade Entry** : ajout rapide d’un trade (date, heure, session, paire, sens, prix d’entrée/sortie, lot size, notes, résultat en $).  
- **Daily Notes** : humeur, résultat de la journée et leçon clé.  
- **Édition / Suppression** : modification directe dans les tableaux.  
- **Progress Page** :
  - Statistiques globales : nombre de trades, win rate, total P/L ($).  
  - Courbe d’équité (résultats cumulés dans le temps).  
  - Résultats hebdomadaires et mensuels sous forme de graphiques.  
- **Sauvegarde & restauration automatiques** : backup avant chaque reset et restauration disponible depuis l’interface.

---

## 🔗 [🚀 Installation et exécution](#-installation-et-exécution)

### 🧩 Étapes d’installation

```bash
# 1️⃣ Cloner le dépôt
git clone https://github.com/<votre_nom_utilisateur>/streamlit-trading-journal.git
cd streamlit-trading-journal

# 2️⃣ (Optionnel) Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# ou
.\.venv\Scripts\activate    # Windows

# 3️⃣ Installer les dépendances
pip install -r requirements.txt

# 4️⃣ Lancer l’application
streamlit run app.py

L’application s’ouvre automatiquement dans votre navigateur 🌐
Sinon, copiez le lien affiché dans le terminal (souvent http://localhost:8501).
Le projet est 100% local.
Les données restent sur ton ordinateur et aucune connexion externe n’est utilisée.


### 🔗 🗂️ Structure du projet

streamlit-trading-journal/
│
├── app.py                  # Script principal Streamlit
├── requirements.txt        # Dépendances du projet
├── README.md               # Documentation
└── data/                   # Fichiers de données
    ├── trades.csv          # Journal des trades
    ├── daily.csv           # Notes quotidiennes
    └── backups/            # Sauvegardes automatiques

🔗 💡 Utilisation rapide

1. Onglet Journal → saisir un trade via Quick Trade Entry → Add trade.

2. Ajouter une Daily Note (mood, résultat, leçon du jour).

3. Onglet Progress → visualiser :

    la courbe d’équité (cumul des résultats),

    les résultats hebdomadaires et mensuels,

    les indicateurs clés (nombre de trades, win rate, total P/L).

4. Dans la sidebar, section Data Safety :

    🛟 Backup now → créer une sauvegarde,

    ↩️ Restore last backup → restaurer la dernière version,

    🗑️ Reset ALL data (with backup) → réinitialiser après sauvegarde.

🔗 🧠 Stack technique

    Python 3.11+

    Streamlit — Interface web interactive

    Pandas — Manipulation et stockage des données

    Altair — Visualisation des performances

🔗 👥 Auteurs

Chaina SPUSTECK et Leslie TAGNE

Projet WebApp Predictive — Sorbonne Université

Année universitaire 2025-2026



