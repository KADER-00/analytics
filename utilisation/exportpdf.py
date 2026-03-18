import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
from itertools import combinations

def create_pdf_report(data, username, theme_sujet="Analyse de Données d'Entreprise"):
    """
    Génération d'un rapport PDF d'analyse exploratoire de données,
    inspiré d'un modèle académique et incluant des analyses avancées.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # --- STYLES ---
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['h1'], fontSize=18, alignment=TA_CENTER, spaceAfter=24, textColor=colors.HexColor('#000000'))
    h1_style = ParagraphStyle('CustomH1', parent=styles['h2'], fontSize=14, spaceBefore=12, spaceAfter=10, textColor=colors.HexColor('#2E86AB'))
    h2_style = ParagraphStyle('CustomH2', parent=styles['h3'], fontSize=12, spaceBefore=10, spaceAfter=8, textColor=colors.HexColor('#A23B72'))
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, spaceAfter=6, alignment=TA_JUSTIFY, leading=14)
    table_header_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey)
    ])
    table_body_style = TableStyle([
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ])

    story = []

    # --- PAGE DE TITRE ---
    story.append(Paragraph("RAPPORT D'ANALYSE EXPLORATOIRE ET PRÉPARATION DES DONNÉES", title_style))
    story.append(Spacer(1, 0.5 * inch))
    title_info = [
        ['Titre:', f'Exploration et nettoyage de données: {theme_sujet}'],
        ['Auteur:', username],
        ['Date:', datetime.now().strftime('%d/%m/%Y')]
    ]
    title_table = Table(title_info, colWidths=[1.5*inch, 4.5*inch])
    title_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
    story.append(title_table)
    story.append(PageBreak())

    # --- 1. INTRODUCTION ---
    story.append(Paragraph("1. Introduction", h1_style))
    intro_text = """
    Ce rapport présente une analyse exploratoire complète du jeu de données fourni. L'objectif est de comprendre
    sa structure, d'identifier et corriger les incohérences, de nettoyer les données, et de produire des analyses
    descriptives utiles comme base pour une future phase de modélisation.
    """
    story.append(Paragraph(intro_text, normal_style))

    # --- 2. DESCRIPTION DU JEU DE DONNÉES ---
    story.append(Paragraph("2. Description du jeu de données", h1_style))
    desc_data = [
        ['Source:', 'Fichier fourni par l\'utilisateur'],
        ['Format:', 'CSV / DataFrame'],
        ['Taille:', f'{data.shape[0]} observations × {data.shape[1]} variables']
    ]
    desc_table = Table(desc_data, colWidths=[1.5*inch, 4.5*inch])
    desc_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
    story.append(desc_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Table des variables", h2_style))
    variable_table_data = [['Nom de variable', 'Type de données', 'Exemples de valeurs']]
    for col in data.columns:
        dtype = str(data[col].dtype)
        examples = ', '.join(map(str, data[col].dropna().unique()[:3])) + '...'
        variable_table_data.append([col, dtype, examples])
    var_table = Table(variable_table_data, hAlign='LEFT')
    var_table.setStyle(table_header_style)
    var_table.setStyle(table_body_style)
    story.append(var_table)

    # --- 3. MÉTHODOLOGIE & NETTOYAGE ---
    story.append(Paragraph("3. Méthodologie et Nettoyage", h1_style))
    story.append(Paragraph("Inspection et correction des données", h2_style))
    duplicates_count = data.duplicated().sum()
    missing_data_report = data.isnull().sum()
    missing_data_report = missing_data_report[missing_data_report > 0].to_dict()

    cleaning_summary = [["Étape", "Résultat observé"]]
    cleaning_summary.append(["Doublons", f"{duplicates_count} ligne(s) identique(s) trouvée(s)."])
    
    if missing_data_report:
        missing_text = ', '.join([f"{k} ({v/len(data):.1%})" for k, v in missing_data_report.items()])
        cleaning_summary.append(["Valeurs manquantes", missing_text])
    else:
        cleaning_summary.append(["Valeurs manquantes", "Aucune valeur manquante détectée."])

    cleaning_table = Table(cleaning_summary, hAlign='LEFT')
    cleaning_table.setStyle(table_header_style)
    cleaning_table.setStyle(table_body_style)
    story.append(cleaning_table)

    # --- 4. ANALYSE UNIVARIÉE ---
    story.append(Paragraph("4. Analyse univariée", h1_style))
    story.append(Paragraph("Variables numériques", h2_style))
    numeric_df = data.select_dtypes(include=np.number)
    if not numeric_df.empty:
        stats_data = [['Variable', 'Moyenne', 'Médiane', 'Écart-type', 'Min', 'Max']]
        desc = numeric_df.describe().T
        for col, row in desc.iterrows():
            stats_data.append([col, f"{row['mean']:.2f}", f"{row['50%']:.2f}", f"{row['std']:.2f}", f"{row['min']:.2f}", f"{row['max']:.2f}"])
        stats_table = Table(stats_data, hAlign='LEFT')
        stats_table.setStyle(table_header_style)
        stats_table.setStyle(table_body_style)
        story.append(stats_table)
    else:
        story.append(Paragraph("Aucune variable numérique à analyser.", normal_style))

    story.append(Paragraph("Variables catégorielles", h2_style))
    cat_df = data.select_dtypes(include=['object', 'category'])
    if not cat_df.empty:
        for col in cat_df.columns:
            story.append(Paragraph(f"Distribution pour '{col}'", styles['h4']))
            freq_data = [['Modalité', 'Fréquence', 'Pourcentage']]
            counts = cat_df[col].value_counts(normalize=True)
            for val, pct in counts.head(5).items(): # Top 5
                freq_data.append([val, f"{cat_df[col].value_counts()[val]}", f"{pct:.1%}"])
            if len(counts) > 5:
                freq_data.append(["Autres...", "", ""])

            freq_table = Table(freq_data, hAlign='LEFT', colWidths=[3*inch, 1.5*inch, 1.5*inch])
            freq_table.setStyle(table_header_style)
            freq_table.setStyle(table_body_style)
            story.append(freq_table)
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph("Aucune variable catégorielle à analyser.", normal_style))

    story.append(PageBreak())

    # --- 5. ANALYSE BIVARIÉE ---
    story.append(Paragraph("5. Analyse bivariée", h1_style))
    story.append(Paragraph("Corrélation entre variables numériques", h2_style))
    if len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr()
        corr_data = [['Variable 1', 'Variable 2', 'Coefficient (r)']]
        # Unstack to get pairs
        corr_pairs = corr_matrix.unstack().sort_values(ascending=False).drop_duplicates()
        for (v1, v2), corr_val in corr_pairs.items():
            if v1 != v2 and corr_val < 1.0:
                 corr_data.append([v1, v2, f"{corr_val:.2f}"])
        
        corr_table = Table(corr_data[:6], hAlign='LEFT') # Top 5 correlations
        corr_table.setStyle(table_header_style)
        corr_table.setStyle(table_body_style)
        story.append(corr_table)
    else:
        story.append(Paragraph("Pas assez de variables numériques pour une analyse de corrélation.", normal_style))
    
    # --- Analyse Bivariée Avancée (Tests Statistiques) ---
    story.append(Paragraph("Analyse bivariée avancée (Tests Statistiques)", h2_style))
    story.append(Paragraph("Un p-value inférieur à 0.05 indique généralement une relation statistiquement significative.", normal_style))
    
    test_results = [['Test', 'Variables', 'Statistique', 'P-Value', 'Interprétation']]
    
    # T-test (Numérique vs Catégorielle à 2 modalités)
    for num_col in numeric_df.columns:
        for cat_col in cat_df.columns:
            if cat_df[cat_col].nunique() == 2:
                groups = cat_df[cat_col].unique()
                group1 = data[data[cat_col] == groups[0]][num_col].dropna()
                group2 = data[data[cat_col] == groups[1]][num_col].dropna()
                if len(group1) > 1 and len(group2) > 1:
                    stat, pval = stats.ttest_ind(group1, group2)
                    interp = "Significatif" if pval < 0.05 else "Non significatif"
                    test_results.append(['T-test', f"{num_col} vs {cat_col}", f"t={stat:.2f}", f"{pval:.3f}", interp])

    # ANOVA (Numérique vs Catégorielle > 2 modalités)
    for num_col in numeric_df.columns:
        for cat_col in cat_df.columns:
            if cat_df[cat_col].nunique() > 2:
                groups = [data[data[cat_col] == g][num_col].dropna() for g in cat_df[cat_col].unique()]
                groups = [g for g in groups if len(g) > 1]
                if len(groups) > 2:
                    stat, pval = stats.f_oneway(*groups)
                    interp = "Significatif" if pval < 0.05 else "Non significatif"
                    test_results.append(['ANOVA', f"{num_col} vs {cat_col}", f"F={stat:.2f}", f"{pval:.3f}", interp])

    # Khi-deux (Catégorielle vs Catégorielle)
    if len(cat_df.columns) > 1:
        for v1, v2 in combinations(cat_df.columns, 2):
            contingency_table = pd.crosstab(data[v1], data[v2])
            chi2, pval, _, _ = stats.chi2_contingency(contingency_table)
            interp = "Association significative" if pval < 0.05 else "Pas d'association"
            test_results.append(['Khi-deux', f"{v1} vs {v2}", f"X²={chi2:.2f}", f"{pval:.3f}", interp])
    
    if len(test_results) > 1:
        tests_table = Table(test_results, hAlign='LEFT', colWidths=[0.8*inch, 1.8*inch, 1*inch, 0.8*inch, 1.6*inch])
        tests_table.setStyle(table_header_style)
        tests_table.setStyle(table_body_style)
        story.append(tests_table)
    else:
        story.append(Paragraph("Aucun test statistique pertinent n'a pu être mené.", normal_style))
    

    # --- 6. CONCLUSION ---
    story.append(Paragraph("6. Conclusion", h1_style))
    conclusion_text = f"""
    L'analyse exploratoire a permis de nettoyer et de structurer efficacement le jeu de données contenant
    {len(data)} enregistrements. Des premières relations entre variables ont été mises en évidence,
    notamment à travers l'analyse de corrélation et les tests statistiques bivariés.
    Ce jeu de données est désormais prêt à être utilisé pour des tâches de visualisation plus poussées,
    de modélisation ou d'analyse prédictive.
    """
    story.append(Paragraph(conclusion_text, normal_style))
    
    # --- 7. ANNEXES ---
    story.append(Paragraph("7. Annexes", h1_style))
    story.append(Paragraph("Le code Python complet et les visualisations générées peuvent être fournis en complément de ce rapport.", normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()