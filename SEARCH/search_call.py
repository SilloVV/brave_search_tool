import requests
from typing import Dict, List, Any, Optional
from LLM.env_variable_loader import load_var_env

def brave_search(query: str, count: int = 8) -> Dict[str, Any]:
    """
    Effectue une recherche web via l'API Brave Search.
    
    Args:
        query (str): La requête de recherche.
        count (int, optional): Nombre de résultats à retourner. Par défaut à 10.
        
    Returns:
        Dict[str, Any]: Les résultats de recherche sous forme de dictionnaire.
    """
    # Charger la clé API Brave Search depuis les variables d'environnement
    api_key = load_var_env("BRAVE_API_KEY")
    
    # URL de l'API Brave Search
    url = "https://api.search.brave.com/res/v1/web/search"
    
    # En-têtes de la requête
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    # Paramètres de la requête
    params = {
        "q": query,
        "count": count
    }
    
    # Effectuer la requête
    response = requests.get(url, headers=headers, params=params)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur lors de la recherche Brave: {response.status_code} - {response.text}")

def extract_search_results(search_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extrait les informations pertinentes des résultats de recherche Brave.
    
    Args:
        search_data (Dict[str, Any]): Les données de recherche brutes.
        
    Returns:
        List[Dict[str, str]]: Liste des résultats de recherche avec titre, description et URL.
    """
    results = []
    
    if "web" in search_data and "results" in search_data["web"]:
        for item in search_data["web"]["results"]:
            result = {
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "url": item.get("url", "")
            }
            results.append(result)
    
    return results


if __name__ == "__main__":
    # Exemple d'utilisation
    search_query = "personne morale SARL"
    raw_results = brave_search(search_query, count=5)
    results = extract_search_results(raw_results)
    
    print(f"Résultats pour la recherche: '{search_query}'")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['description']}")
        print(f"   URL: {result['url']}")