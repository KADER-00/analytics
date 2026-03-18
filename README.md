# Analyse PME - Application Streamlit

Une application Streamlit complète pour l'analyse de données des petites et moyennes entreprises (PME).

## Fonctionnalités

- **Authentification sécurisée** : Système de login/inscription avec gestion des sessions
- **Import de données** : Support des fichiers CSV et Excel
- **Nettoyage automatique** : Traitement intelligent des données importées
- **Recommandations IA** : Génération automatique de conseils et alertes
- **Visualisations** : Graphiques interactifs avec Plotly
- **Export PDF** : Génération de rapports professionnels
- **telecharger données nettoyé**:telechargement des données deja nettoyées
- **Interface moderne** : Design futuriste et professionnel

##  Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🛠 Installation

1. **Cloner ou télécharger le projet**


---

## ⚙️ Installation

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/KADER-00/analytics.git
cd analytics

2. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**

   ```bash
   streamlit run apps.py
   ```

4. **Accéder à l'application**
   - Ouvrez votre navigateur à l'adresse : `http://localhost:8501`

##  Comptes de démonstration

L'application inclut des comptes de test prêts à utiliser :

### Administrateur

- **Utilisateur** : `admin`
- **Mot de passe** : `admin123`

### Utilisateur demo

- **Utilisateur** : `demo`
- **Mot de passe** : `demo123`

## 📁 Structure du projet

```
analyse-pme/
├── apps.py                     # Application principale
├── requirements.txt            # Dépendances Python
├── assets                      # Dossier d'image logo           
      ├── logo.png              #image du logo
      └── icon.png             # icon du logo                  
├── README.md                  # Documentation
├── users.json                 # Base de données utilisateurs (générée automatiquement)
├── frontend/
│   └── ui.py                  # Interface utilisateur et CSS
├── backend/
│   ├── authentifat.py         # Gestion de l'authentification
│   └── datacleaning.py        # Nettoyage des données
└── utilisation/
    ├── recommendation.py      # Génération de recommandations
    └── exportpdf.py          # Export PDF
└── visualisation.py          # Graphiques et visualisations
```

## Guide d'utilisation

### 1. Connexion

- Utilisez un des comptes de démonstration ou créez un nouveau compte
- L'authentification est requise pour accéder aux fonctionnalités

### 2. Import des données

- Naviguez vers l'onglet "Importer"
- Glissez-déposez ou sélectionnez un fichier CSV/Excel
- Les données sont automatiquement nettoyées et analysées

### 3. Visualisation

- Onglet "Visualiser" pour explorer vos données
- Graphiques interactifs : distributions, corrélations, comparaisons
- Dashboard d'insights automatiques

### 4. Export

- Onglet "Exporter" pour télécharger vos résultats
- Export CSV des données nettoyées
- Rapport PDF professionnel avec recommandations
- telecharger données nettoyées

## 🔧 Fonctionnalités techniques

### Nettoyage automatique des données

- Suppression des doublons
- Gestion des valeurs manquantes
- Détection automatique des types de données
- Identification des valeurs aberrantes
- Normalisation des noms de colonnes

### Recommandations intelligentes

- Analyse de la qualité des données
- Détection d'anomalies
- Conseils d'optimisation
- Recommandations métier
- Alertes de performance

### Visualisations avancées

- Graphiques de distribution
- Matrices de corrélation
- Comparaisons par groupes
- Dashboard d'insights
- Métriques de qualité

## Personnalisation

### Thème et couleurs

Les couleurs principales peuvent être modifiées dans `frontend/ui.py` :

- `--primary-color: #2E86AB` (Bleu principal)
- `--secondary-color: #A23B72` (Violet secondaire)
- `--accent-color: #F18F01` (Orange accent)

### Ajout de nouvelles fonctionnalités

- **Nouveaux types de graphiques** : Modifier `visualisation.py`
- **Recommandations personnalisées** : Étendre `utilisation/recommendation.py`
- **Formats d'export supplémentaires** : Ajouter dans `utilisation/exportpdf.py`

## Sécurité

- Mots de passe hachés avec SHA-256
- Gestion sécurisée des sessions
- Validation des fichiers uploadés
- Protection contre les injections

##  Dépannage

### Erreurs communes

1. **Erreur d'import de modules**

   ```bash
   pip install -r requirements.txt
   ```

2. **Problème d'encodage des fichiers CSV**

   - L'application gère automatiquement UTF-8, Latin-1 et CP1252

3. **Fichier Excel non reconnu**

   - Vérifiez que le fichier a l'extension .xlsx ou .xls

4. **Erreur de mémoire avec gros fichiers**
   - Limitez la taille des fichiers à < 100MB

##  Formats de données supportés

### CSV

- Encodage : UTF-8, Latin-1, CP1252
- Séparateurs : virgule, point-virgule (détection automatique)
- Headers : première ligne considérée comme en-têtes

### Excel

- Formats : .xlsx, .xls
- Feuilles multiples : première feuille utilisée par défaut
- Cellules fusionnées : gérées automatiquement

##  Déploiement

### Déploiement local

```bash
streamlit run apps.py --server.port 8501
```

### Déploiement sur Streamlit Cloud

1. Pusher le code sur GitHub
2. Connecter le repository à Streamlit Cloud
3. Configurer les variables d'environnement si nécessaire

## Performances

### Optimisations incluses

- Mise en cache des données avec `@st.cache_data`
- Traitement par chunks pour gros fichiers
- Optimisation des types de données
- Lazy loading des visualisations

### Limites recommandées

- Fichiers : < 100MB
- Lignes : < 1M pour performances optimales
- Colonnes : < 100
