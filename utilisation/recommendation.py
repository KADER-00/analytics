import pandas as pd
import numpy as np

def generate_recommendations(df):
    """Génération de recommandations intelligentes basées sur l'analyse des données"""
    if df is None or df.empty:
        return [{"type": "error", "message": "Aucune donnée à analyser"}]
    
    recommendations = []
    
    # 1. Analyse de la qualité des données
    recommendations.extend(analyze_data_quality(df))
    
    # 2. Analyse des valeurs manquantes
    recommendations.extend(analyze_missing_values(df))
    
    # 3. Analyse des valeurs aberrantes
    recommendations.extend(analyze_outliers(df))
    
    # 4. Analyse de la distribution des données
    recommendations.extend(analyze_data_distribution(df))
    
    # 5. Recommandations métier
    recommendations.extend(generate_business_recommendations(df))
    
    # 6. Recommandations de performance
    recommendations.extend(analyze_performance_metrics(df))
    
    return recommendations

def analyze_data_quality(df):
    """Analyse de la qualité générale des données"""
    recommendations = []
    
    # Vérification de la taille du dataset
    if len(df) < 10:
        recommendations.append({
            "type": "warning",
            "message": f"Dataset très petit ({len(df)} lignes). Considérez collecter plus de données pour des analyses plus robustes."
        })
    elif len(df) > 10000:
        recommendations.append({
            "type": "success",
            "message": f"Excellent! Dataset de taille substantielle ({len(df):,} lignes) permettant des analyses statistiques fiables."
        })
    
    # Vérification du nombre de colonnes
    if len(df.columns) < 3:
        recommendations.append({
            "type": "info",
            "message": "Dataset avec peu de variables. Considérez enrichir vos données avec des variables supplémentaires."
        })
    elif len(df.columns) > 50:
        recommendations.append({
            "type": "warning",
            "message": f"Dataset avec beaucoup de variables ({len(df.columns)}). Considérez une sélection de variables pour améliorer les performances."
        })
    
    # Vérification des doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        recommendations.append({
            "type": "warning",
            "message": f"{duplicates} lignes dupliquées détectées ({duplicates/len(df)*100:.1f}%). Nettoyage recommandé."
        })
    else:
        recommendations.append({
            "type": "success",
            "message": "Aucun doublon détecté. Excellente qualité des données!"
        })
    
    return recommendations

def analyze_missing_values(df):
    """Analyse des valeurs manquantes"""
    recommendations = []
    
    missing_stats = df.isnull().sum()
    total_missing = missing_stats.sum()
    
    if total_missing == 0:
        recommendations.append({
            "type": "success",
            "message": "Aucune valeur manquante détectée. Dataset complet!"
        })
    else:
        missing_percentage = (total_missing / (len(df) * len(df.columns))) * 100
        
        if missing_percentage < 5:
            recommendations.append({
                "type": "info",
                "message": f"Peu de valeurs manquantes ({missing_percentage:.1f}%). Qualité acceptable."
            })
        elif missing_percentage < 15:
            recommendations.append({
                "type": "warning",
                "message": f"Valeurs manquantes modérées ({missing_percentage:.1f}%). Stratégie d'imputation recommandée."
            })
        else:
            recommendations.append({
                "type": "error",
                "message": f"Beaucoup de valeurs manquantes ({missing_percentage:.1f}%). Révision de la collecte de données nécessaire."
            })
        
        # Analyse par colonne
        high_missing_cols = missing_stats[missing_stats > len(df) * 0.3]
        if not high_missing_cols.empty:
            recommendations.append({
                "type": "warning",
                "message": f"Colonnes avec >30% de valeurs manquantes: {', '.join(high_missing_cols.index.tolist())}. Considérez les supprimer."
            })
    
    return recommendations

def analyze_outliers(df):
    """Analyse des valeurs aberrantes"""
    recommendations = []
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    outlier_columns = []
    
    for col in numeric_columns:
        if not col.endswith('_outlier'):  # Éviter les colonnes d'indicateurs d'outliers
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            
            if outliers > 0:
                outlier_percentage = (outliers / len(df)) * 100
                outlier_columns.append((col, outliers, outlier_percentage))
    
    if not outlier_columns:
        recommendations.append({
            "type": "success",
            "message": "Aucune valeur aberrante significative détectée dans les données numériques."
        })
    else:
        for col, count, percentage in outlier_columns:
            if percentage < 5:
                recommendations.append({
                    "type": "info",
                    "message": f"Quelques valeurs aberrantes dans '{col}' ({count} valeurs, {percentage:.1f}%). Vérification recommandée."
                })
            else:
                recommendations.append({
                    "type": "warning",
                    "message": f"Nombreuses valeurs aberrantes dans '{col}' ({count} valeurs, {percentage:.1f}%). Investigation nécessaire."
                })
    
    return recommendations

def analyze_data_distribution(df):
    """Analyse de la distribution des données"""
    recommendations = []
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_columns:
        if not col.endswith('_outlier'):
            # Analyse de la variance
            if df[col].var() == 0:
                recommendations.append({
                    "type": "warning",
                    "message": f"Colonne '{col}' a une variance nulle (valeurs constantes). Considérez la supprimer."
                })
            
            # Analyse de l'asymétrie
            skewness = df[col].skew()
            if abs(skewness) > 2:
                recommendations.append({
                    "type": "info",
                    "message": f"Distribution très asymétrique pour '{col}' (skewness: {skewness:.2f}). Transformation recommandée."
                })
    
    # Analyse des colonnes catégorielles
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    for col in categorical_columns:
        unique_values = df[col].nunique()
        total_values = len(df[col].dropna())
        
        if unique_values == total_values:
            recommendations.append({
                "type": "warning",
                "message": f"Colonne '{col}' a toutes des valeurs uniques. Pourrait être un identifiant."
            })
        elif unique_values == 1:
            recommendations.append({
                "type": "warning",
                "message": f"Colonne '{col}' a une seule valeur unique. Considérez la supprimer."
            })
        elif unique_values > total_values * 0.8:
            recommendations.append({
                "type": "info",
                "message": f"Colonne '{col}' a beaucoup de valeurs uniques ({unique_values}). Vérifiez si c'est intentionnel."
            })
    
    return recommendations

def generate_business_recommendations(df):
    """Génération de recommandations métier basées sur les patterns des données"""
    recommendations = []
    
    # Détection de colonnes potentiellement importantes pour le business
    business_keywords = {
        'revenue': ['chiffre', 'affaires', 'revenue', 'vente', 'ca'],
        'cost': ['cout', 'cost', 'depense', 'charge'],
        'profit': ['profit', 'benefice', 'marge'],
        'customer': ['client', 'customer', 'user'],
        'date': ['date', 'time', 'jour', 'mois', 'annee'],
        'quantity': ['quantite', 'quantity', 'nombre', 'count']
    }
    
    detected_business_cols = {}
    
    for category, keywords in business_keywords.items():
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                if category not in detected_business_cols:
                    detected_business_cols[category] = []
                detected_business_cols[category].append(col)
    
    # Recommandations basées sur les colonnes détectées
    if 'revenue' in detected_business_cols and 'cost' in detected_business_cols:
        recommendations.append({
            "type": "success",
            "message": "Données de revenus et coûts détectées. Calcul de rentabilité possible!"
        })
    
    if 'date' in detected_business_cols:
        recommendations.append({
            "type": "info",
            "message": "Données temporelles détectées. Analyses de tendances et saisonnalité recommandées."
        })
    
    if 'customer' in detected_business_cols:
        recommendations.append({
            "type": "info",
            "message": "Données clients détectées. Analyses de segmentation et rétention possibles."
        })
    
    # Analyse des corrélations pour les données numériques
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr()
        high_corr_pairs = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.8:
                    high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_value))
        
        if high_corr_pairs:
            recommendations.append({
                "type": "info",
                "message": f"Corrélations fortes détectées entre certaines variables. Attention à la multicolinéarité."
            })
    
    return recommendations

def analyze_performance_metrics(df):
    """Analyse des métriques de performance et recommandations d'optimisation"""
    recommendations = []
    
    # Analyse de la taille mémoire
    memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    
    if memory_usage > 100:
        recommendations.append({
            "type": "warning",
            "message": f"Dataset volumineux ({memory_usage:.1f} MB). Considérez l'optimisation des types de données."
        })
    
    # Recommandations d'optimisation des types
    optimization_suggestions = []
    
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.5:  # Moins de 50% de valeurs uniques
                optimization_suggestions.append(f"'{col}' pourrait être converti en catégorie")
        
        elif df[col].dtype == 'int64':
            max_val = df[col].max()
            min_val = df[col].min()
            if max_val < 127 and min_val > -128:
                optimization_suggestions.append(f"'{col}' pourrait être converti en int8")
            elif max_val < 32767 and min_val > -32768:
                optimization_suggestions.append(f"'{col}' pourrait être converti en int16")
    
    if optimization_suggestions:
        recommendations.append({
            "type": "info",
            "message": f"Optimisations possibles: {'; '.join(optimization_suggestions[:3])}{'...' if len(optimization_suggestions) > 3 else ''}"
        })
    
    # Recommandations d'indexation pour les gros datasets
    if len(df) > 10000:
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            recommendations.append({
                "type": "info",
                "message": "Pour un dataset de cette taille, considérez l'indexation des colonnes catégorielles fréquemment utilisées."
            })
    
    return recommendations

def get_data_insights(df):
    """Génération d'insights automatiques sur les données"""
    insights = []
    
    if df is None or df.empty:
        return insights
    
    # Insight sur la taille
    insights.append(f"Dataset contient {len(df):,} lignes et {len(df.columns)} colonnes")
    
    # Insight sur les types de données
    type_counts = df.dtypes.value_counts()
    insights.append(f"Types de données: {dict(type_counts)}")
    
    # Insight sur la complétude
    completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    insights.append(f"Complétude des données: {completeness:.1f}%")
    
    # Insights sur les colonnes numériques
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        insights.append(f"Colonnes numériques: {len(numeric_cols)} ({', '.join(numeric_cols[:3])}{'...' if len(numeric_cols) > 3 else ''})")
    
    # Insights sur les colonnes catégorielles
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        insights.append(f"Colonnes catégorielles: {len(cat_cols)} ({', '.join(cat_cols[:3])}{'...' if len(cat_cols) > 3 else ''})")
    
    return insights
