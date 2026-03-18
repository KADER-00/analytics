import pandas as pd
import numpy as np
import streamlit as st

# La fonction de chargement reste utile et bien conçue.
def load_file(uploaded_file):
    """Chargement d'un fichier CSV ou Excel avec gestion des encodages."""
    try:
        if uploaded_file.name.endswith('.csv'):
            try:
                # Laisser pandas inférer l'encodage est souvent plus robuste
                df = pd.read_csv(uploaded_file, encoding_errors='replace')
            except Exception:
                # Fallback sur les encodages communs si l'inférence échoue
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin-1')
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Format de fichier non supporté. Veuillez utiliser CSV ou Excel.")
            return None
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None

def clean_data(df, 
               missing_value_strategy='auto', 
               missing_col_threshold=0.8, 
               outlier_strategy='flag',
               outlier_method='iqr', 
               iqr_multiplier=1.5):
    """
    Pipeline de nettoyage de données unifié, configurable et robuste.
    Retourne le DataFrame nettoyé et un journal des opérations.
    """
    if df is None or df.empty:
        return pd.DataFrame(), ["Le DataFrame initial est vide."]

    # Copie pour éviter de modifier l'original et initialisation du journal
    cleaned_df = df.copy()
    cleaning_log = []

    # --- 1. Nettoyage Structurel de Base ---
    initial_shape = cleaned_df.shape
    # Suppression des lignes et colonnes entièrement vides
    cleaned_df.dropna(how='all', inplace=True)
    cleaned_df.dropna(axis=1, how='all', inplace=True)
    shape_after_drop_all = cleaned_df.shape
    if initial_shape != shape_after_drop_all:
        cleaning_log.append(f"INFO: Suppression des lignes/colonnes entièrement vides. Taille passée de {initial_shape} à {shape_after_drop_all}.")

    # --- 2. Nettoyage des Noms de Colonnes ---
    original_columns = cleaned_df.columns.tolist()
    cleaned_df.columns = (cleaned_df.columns
                          .str.strip()
                          .str.lower()
                          .str.replace(r'\s+', '_', regex=True)
                          .str.replace(r'[^a-z0-9_]', '', regex=True))
    new_columns = cleaned_df.columns.tolist()
    renamed_cols = {o: n for o, n in zip(original_columns, new_columns) if o != n}
    if renamed_cols:
        cleaning_log.append(f"INFO: {len(renamed_cols)} noms de colonnes ont été standardisés (ex: '{list(renamed_cols.keys())[0]}' -> '{list(renamed_cols.values())[0]}').")

    # --- 3. Nettoyage des Données Textuelles et Standardisation des "Nuls" ---
    # Convertit les chaînes vides et autres variantes de "null" en véritables NaN
    text_cols = cleaned_df.select_dtypes(include=['object']).columns
    null_variants = ['', 'nan', 'na', 'none', 'null', 'n/a', '--']
    for col in text_cols:
        # Trim whitespace
        cleaned_df[col] = cleaned_df[col].str.strip()
        # Standardize nulls
        cleaned_df[col] = cleaned_df[col].str.lower().replace(null_variants, np.nan)
    cleaning_log.append(f"INFO: Nettoyage des espaces et standardisation des valeurs textuelles vides en NaN.")

    # --- 4. Suppression des Doublons ---
    initial_rows = len(cleaned_df)
    cleaned_df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - len(cleaned_df)
    if duplicates_removed > 0:
        cleaning_log.append(f"IMPORTANT: {duplicates_removed} ligne(s) en double ont été supprimée(s).")

    # --- 5. Gestion des Colonnes Fortement Vides ---
    # A faire avant l'imputation
    missing_ratios = cleaned_df.isnull().sum() / len(cleaned_df)
    cols_to_drop = missing_ratios[missing_ratios > missing_col_threshold].index
    if not cols_to_drop.empty:
        cleaned_df.drop(columns=cols_to_drop, inplace=True)
        cleaning_log.append(f"AVERTISSEMENT: {len(cols_to_drop)} colonnes ({', '.join(cols_to_drop)}) supprimées car plus de {missing_col_threshold:.0%} de valeurs sont manquantes.")

    # --- 6. Inférence et Conversion des Types ---
    original_types = cleaned_df.dtypes.to_dict()
    # Tente de convertir en numérique, puis date, puis booléen.
    for col in cleaned_df.columns:
        # Tente la conversion numérique
        converted_series = pd.to_numeric(cleaned_df[col], errors='coerce')
        if converted_series.notna().sum() > 0.8 * cleaned_df[col].notna().sum(): # Si >80% de succès
            # Tente de convertir en entier si possible pour économiser la mémoire
            if converted_series.dropna().apply(lambda x: x == int(x)).all():
                cleaned_df[col] = converted_series.astype('Int64')
            else:
                cleaned_df[col] = converted_series
            continue # Passe à la colonne suivante

        # Tente la conversion en date
        try:
            converted_series = pd.to_datetime(cleaned_df[col], errors='coerce')
            if converted_series.notna().sum() > 0.8 * cleaned_df[col].notna().sum():
                cleaned_df[col] = converted_series
                continue
        except Exception:
            pass
            
        # Tente la conversion en booléen
        if cleaned_df[col].nunique() <= 2:
             bool_map = {'true': True, '1': True, 'yes': True, 'oui': True,
                         'false': False, '0': False, 'no': False, 'non': False}
             if cleaned_df[col].dropna().str.lower().isin(bool_map.keys()).all():
                 cleaned_df[col] = cleaned_df[col].str.lower().map(bool_map).astype('boolean')

    new_types = cleaned_df.dtypes.to_dict()
    types_changed = {k: f"{original_types[k]} -> {new_types[k]}" for k in new_types if str(original_types.get(k)) != str(new_types[k])}
    if types_changed:
        cleaning_log.append(f"INFO: {len(types_changed)} types de colonnes ont été convertis (ex: '{list(types_changed.keys())[0]}' de {list(types_changed.values())[0]}).")

    # --- 7. Gestion des Valeurs Aberrantes (Outliers) ---
    numeric_cols_for_outliers = cleaned_df.select_dtypes(include=np.number).columns
    if outlier_strategy != 'none' and outlier_method == 'iqr':
        for column in numeric_cols_for_outliers:
            Q1 = cleaned_df[column].quantile(0.25)
            Q3 = cleaned_df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - iqr_multiplier * IQR
            upper_bound = Q3 + iqr_multiplier * IQR
            
            outliers = (cleaned_df[column] < lower_bound) | (cleaned_df[column] > upper_bound)
            
            if outliers.sum() > 0:
                if outlier_strategy == 'flag':
                    cleaned_df[f'{column}_outlier'] = outliers
                    cleaning_log.append(f"INFO: {outliers.sum()} valeurs aberrantes détectées et signalées dans '{column}'.")
                elif outlier_strategy == 'remove':
                    cleaned_df = cleaned_df[~outliers]
                    cleaning_log.append(f"IMPORTANT: {outliers.sum()} lignes contenant des valeurs aberrantes pour '{column}' ont été supprimées.")
                elif outlier_strategy == 'cap':
                    cleaned_df[column] = np.where(cleaned_df[column] < lower_bound, lower_bound, cleaned_df[column])
                    cleaned_df[column] = np.where(cleaned_df[column] > upper_bound, upper_bound, cleaned_df[column])
                    cleaning_log.append(f"INFO: {outliers.sum()} valeurs aberrantes pour '{column}' ont été plafonnées (winsorized).")

    # --- 8. Gestion des Valeurs Manquantes (Imputation) ---
    if missing_value_strategy != 'none':
        for column in cleaned_df.columns:
            if cleaned_df[column].isnull().sum() > 0:
                if missing_value_strategy == 'remove_row':
                    cleaned_df.dropna(subset=[column], inplace=True)
                    cleaning_log.append(f"INFO: Lignes avec valeurs manquantes pour '{column}' supprimées.")
                elif missing_value_strategy == 'auto':
                    dtype = cleaned_df[column].dtype
                    if pd.api.types.is_numeric_dtype(dtype):
                        # La médiane est plus robuste aux outliers que la moyenne 
                        impute_value = cleaned_df[column].median()
                        cleaned_df[column].fillna(impute_value, inplace=True)
                        cleaning_log.append(f"INFO: Valeurs manquantes de '{column}' remplacées par la médiane ({impute_value:.2f}).")
                    elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
                        # Le mode est le choix standard pour les variables catégorielles 
                        impute_value = cleaned_df[column].mode()[0]
                        cleaned_df[column].fillna(impute_value, inplace=True)
                        cleaning_log.append(f"INFO: Valeurs manquantes de '{column}' remplacées par le mode ('{impute_value}').")
                    else: # Dates, booléens...
                        impute_value = cleaned_df[column].mode()[0]
                        cleaned_df[column].fillna(impute_value, inplace=True)
                        cleaning_log.append(f"INFO: Valeurs manquantes de '{column}' remplacées par la valeur la plus fréquente ('{impute_value}').")
    
    final_shape = cleaned_df.shape
    cleaning_log.append(f"SUCCÈS: Nettoyage terminé. Taille finale du DataFrame : {final_shape}.")
    
    return cleaned_df, cleaning_log