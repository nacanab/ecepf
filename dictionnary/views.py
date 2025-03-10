# import requests
# from django.shortcuts import render

# def word(request):
#     search = request.GET.get('search', '').strip()  # Nettoie l'entrée utilisateur
#     context = {
#         'search': search,
#         'meaning': "Définition non trouvée.",
#         'synonyms': ["Aucun synonyme trouvé"],
#         'antonyms': ["Aucun antonyme trouvé"]
#     }

#     if search:
#         # 🔹 1. Récupération des définitions via l'API de Wiktionary
#         try:
#             wiktionary_url = "https://fr.wiktionary.org/w/api.php"
#             wiktionary_params = {
#                 "action": "query",
#                 "format": "json",
#                 "titles": search,
#                 "prop": "extracts",
#                 "exintro": True,
#                 "explaintext": True,
#             }
#             response = requests.get(wiktionary_url, params=wiktionary_params, timeout=5)
#             response.raise_for_status()
#             data = response.json()
#             pages = data.get("query", {}).get("pages", {})

#             for page_id, page_data in pages.items():
#                 if int(page_id) > 0:  # Vérifie si la page existe
#                     context['meaning'] = page_data.get("extract", "Définition non trouvée.")
#                     break
#         except requests.RequestException:
#             context['meaning'] = "Erreur lors de la récupération de la définition."

#         # 🔹 2. Récupération des synonymes et antonymes via Datamuse (en filtrant les mots en français)
#         try:
#             datamuse_url = "https://api.datamuse.com/words"

#             # Synonymes (on ajoute "topics=francais" pour améliorer la langue)
#             response_synonyms = requests.get(datamuse_url, params={"rel_syn": search, "topics": "francais"}, timeout=5)
#             response_synonyms.raise_for_status()
#             synonyms_data = response_synonyms.json()
#             context['synonyms'] = [synonym['word'] for synonym in synonyms_data[:5]] if synonyms_data else ["Aucun synonyme trouvé"]

#             # Antonymes (on ajoute "topics=francais" pour améliorer la langue)
#             response_antonyms = requests.get(datamuse_url, params={"rel_ant": search, "topics": "francais"}, timeout=5)
#             response_antonyms.raise_for_status()
#             antonyms_data = response_antonyms.json()
#             context['antonyms'] = [antonym['word'] for antonym in antonyms_data[:5]] if antonyms_data else ["Aucun antonyme trouvé"]

#         except requests.RequestException:
#             context['synonyms'] = ["Erreur lors de la récupération des synonymes"]
#             context['antonyms'] = ["Erreur lors de la récupération des antonymes"]

#     return render(request, 'dictionnary/word.html', context)
import requests
from django.shortcuts import render

# Clé API pour SerpAPI (Google Search)
SERPAPI_KEY = "360d3b96b2bb33f40319321a14b75708b7bd2fb6ea24a0f1b522ee02987048db"  # Remplace par ta clé API

def get_google_definition(word):
    """Cherche une définition sur Google en cas d'échec de Wiktionary."""
    try:
        google_url = "https://serpapi.com/search"
        params = {
            "q": f"définition {word}",
            "hl": "fr",
            "gl": "fr",
            "api_key": SERPAPI_KEY
        }
        response = requests.get(google_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Vérifier si la réponse contient des résultats
        if "organic_results" in data and data["organic_results"]:
            for result in data["organic_results"]:
                if "snippet" in result and result["snippet"].strip():
                    return result["snippet"]  # Retourne la première définition trouvée

        return "Définition non trouvée."
    except requests.RequestException:
        return "Erreur lors de la récupération de la définition via Google."

def get_wiktionary_definition(word):
    """Cherche une définition sur Wiktionary."""
    try:
        wiktionary_url = "https://fr.wiktionary.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": word,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
        }
        response = requests.get(wiktionary_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        for page_id, page_data in pages.items():
            if int(page_id) > 0 and "extract" in page_data:
                return page_data["extract"]  # Retourne la définition trouvée

        return None  # Retourne None si aucune définition trouvée
    except requests.RequestException:
        return None  # Retourne None en cas d'erreur

def word(request):
    search = request.GET.get('search', '').strip().lower()  # Nettoie et met en minuscule
    context = {
        'search': search,
        'meaning': "Définition non trouvée.",
        'synonyms': ["Aucun synonyme trouvé"],
        'antonyms': ["Aucun antonyme trouvé"]
    }

    if search:
        # 🔹 1. Recherche sur Wiktionary
        meaning = get_wiktionary_definition(search)
        
        # Si Wiktionary ne trouve rien, on cherche sur Google
        if not meaning:
            meaning = get_google_definition(search)

        context['meaning'] = meaning

        # 🔹 2. Récupération des synonymes et antonymes via Datamuse
        try:
            datamuse_url = "https://api.datamuse.com/words"

            # Synonymes
            response_synonyms = requests.get(datamuse_url, params={"rel_syn": search, "topics": "francais"}, timeout=5)
            response_synonyms.raise_for_status()
            synonyms_data = response_synonyms.json()
            context['synonyms'] = [synonym['word'] for synonym in synonyms_data[:5]] if synonyms_data else ["Aucun synonyme trouvé"]

            # Antonymes
            response_antonyms = requests.get(datamuse_url, params={"rel_ant": search, "topics": "francais"}, timeout=5)
            response_antonyms.raise_for_status()
            antonyms_data = response_antonyms.json()
            context['antonyms'] = [antonym['word'] for antonym in antonyms_data[:5]] if antonyms_data else ["Aucun antonyme trouvé"]

        except requests.RequestException:
            context['synonyms'] = ["Erreur lors de la récupération des synonymes"]
            context['antonyms'] = ["Erreur lors de la récupération des antonymes"]

    return render(request, 'dictionnary/word.html', context)