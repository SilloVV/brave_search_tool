from dotenv import load_dotenv
import os
from typing import List, Dict, Any
import json
import sys
from google import genai

# Import des modules personnalisés
from LLM.init_gemini import initialize_gemini, GEMINI_API_KEY
from SEARCH.search_call import brave_search, extract_search_results

# Chargement des variables d'environnement
load_dotenv()

def optimize_search_query(query: str) -> str:
    """
    Utilise Gemini pour reformuler la requête en mots-clés pertinents 
    en éliminant les mots vides.
    """
    try:
        # Initialiser le client Gemini
        model = "gemini-2.0-flash-001"
        client = initialize_gemini(model)
        
        # Préparer le prompt pour Gemini
        prompt = f"""
        Reformule cette question ou phrase en mots-clés de recherche pertinents.
        Ajoute des mots clés pour assurer la recherche sur le droit français.
        Élimine tous les mots vides (articles, prépositions, conjonctions).
        Retourne uniquement les mots-clés, sans phrases complètes ni explications.
        
        Question ou phrase: "{query}"
        """
        
        # Appel au modèle Gemini
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        
        # Récupérer la réponse et la nettoyer
        optimized_query = response.text.strip()
        print(f"Requête d'origine: '{query}'")
        print(f"Requête optimisée: '{optimized_query}'")
        
        return optimized_query
    
    except Exception as e:
        print(f"Erreur lors de l'optimisation de la requête: {e}")
        # En cas d'erreur, retourner la requête originale
        return query

def main(search_query: str = None):
    # Si aucune requête n'est fournie, utiliser une valeur par défaut
    if search_query is None:
        if len(sys.argv) > 1:
            # Utiliser les arguments de ligne de commande s'ils sont disponibles
            search_query = " ".join(sys.argv[1:])
        else:
            search_query = "actualités tech intelligence artificielle"
            print("Aucune requête fournie, utilisation de la requête par défaut.")
    
    # Optimiser la requête avec Gemini
    optimized_query = optimize_search_query(search_query)
    
    # Appel à la fonction de recherche Brave avec la requête optimisée
    search_results = brave_search(optimized_query)
    
    # Extraction et traitement des résultats de recherche
    extracted_results = extract_search_results(search_results)
    
    # Affichage des résultats
    print(f"Résultats de recherche pour '{optimized_query}':")
    for i, result in enumerate(extracted_results, 1):
        print(f"\n--- Résultat {i} ---")
        print(f"Titre: {result.get('title', 'Sans titre')}")
        print(f"URL: {result.get('url', 'Pas d\'URL')}")
        print(f"Description: {result.get('description', 'Pas de description')}")
    
    return extracted_results
 
if __name__ == "__main__":
    query = input("Entrez votre requête de recherche: ")
    main(query)