import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def count_na(df, column, result_type="number"):
    """
        Fonction permettant de savoir le pourcentage de valeur manquante d'une colonne

        -----------
        parmeters
        df: Le dataframe
        column: La colonne sur laquelle le calcul doit se faire

        return
        missing_count: Nombre de valeurs manquantes ou pourcentage de valeurs manquantes
    """
    nb_line = df.shape[0]
    missing_count = df[column].isna().sum()
    if(result_type == "percent"):
        return round((missing_count*100)/nb_line, 2)
    return missing_count


def numeric_descriptive_stat(df, columns=None):
    """
        Fonction permettant d'afficher les statistiques descriptives
        de variables quantitives
        
        ---------
        df: Le dataframe
        columns: colonnes à parcourir
    """
    pd.set_option("display.float_format", "{:,.0f}".format)
    
    if columns:
        for column in columns:
            if(df[column].dtypes == "int64" or df[column].dtypes == "float64"):
                display(df[column].describe())
                print("\n\n")
            else:
                print(f"La colonne {column} est de type {df[column].dtypes}")
    else:    
        for column in df.columns:
            if(df[column].dtypes == "int64" or df[column].dtypes == "float64"):
                display(df[column].describe())
                print("\n\n")
            else:
                print(f"La colonne {column} est de type {df[column].dtypes}")


def category_descriptive_stat(df, columns):
    """
        Fonction qui permet d'afficher le nombre d'occurences leur fréquence dans un variable catégorielle

        --------
        paramrters
        df: le dataframe 
        columns: la liste des colonnes à parcourirs dans le dataframe
    """
    for column in columns:
        print(f"\nPour la colonne {column}")
        display(
            pd.DataFrame({
                "effectif": df[column].value_counts(dropna=False),
                "fréquence":df[column].value_counts(normalize=True, dropna=False)*100
            }))


def make_plot(df, params, type="boxplot"):
    """
        Fonction permettant de faire différents types de plot en fonction des paramètres
    """
    plt.figure(figsize=(15,10))

    if type == "scatterplot":
        sns.scatterplot(
            data = df,
            x = params["x"],
            y = params["y"],
            color = params.get("color", "cyan"),
            alpha = params.get("alpha", 1)
        )
    elif type == "boxplot":
        sns.boxplot(
            data = df,
            x = params["x"],
            y = params["y"],
            color = params.get("color", "cyan"),
        )
    
    plt.xticks(rotation=90)  # utile si x est catégoriel pour lisibilité
    plt.grid(params["grid"])
    plt.title(params["title"])
    plt.show()
    
        
def outlier_detect_iqr(df, column):
    """
        Fonction permettant de détecter les outliers d'une colonne numérique suivant la méthode des IQR
        Q1: Le premier quartile
        Q2: La médiane
        Q3: Le troisième quartile
        IQR(interquartile) = Q3 - Q1
        
        Est considérer comme outlier tout élément d'une colonne ne se trouvant pas dans l'intervalle [Q1 - 1.5xIQR, Q3 + 1.5xIQR]


        parameters
        -----------------------
        df: dataframe
        column: colonne du dataframe
    """

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5*IQR
    upper_bound = Q3 + 1.5*IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound )].index
    outliers_idx = df[(df[column] < lower_bound) | (df[column] > upper_bound )].index

    print(f"Colonne {column}")
    print(f"Q1 = {Q1}, Q3 = {Q3}, IQR = {IQR}")
    print(f"Borne inf = {lower_bound}, Borne sup = {upper_bound}")
    print(f"Nombre d’outliers = {outliers.shape[0]}")
    print("\n\n")
    
    return outliers_idx


def correlation_filter(corr_matrix, targets, threshold):
    """
        Fonction qui retourne une liste de colonne à garder selon un seuil de corrélation défini sur une matrice de corrélation

        parameters:
        -----------------------
        corr_matrix: Matrice de corrélation
        targets: liste des variables ou de la variable sur laquelle les corrélations se font
        threshold: Le seuil de corrélation à respecter
    """
    corr = dict()
    for target in targets:
        selected = corr_matrix[target].abs()
        selected = selected[selected >= threshold].index.tolist()
        #selected = [col for col in selected if col != target]
        corr[target] = selected
        print(f"Les colonnes corrélées au seuil de {threshold} avec {target} sont: {selected} \n")

    return corr
        
        
        
