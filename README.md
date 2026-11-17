# EDF Hydro — Le Journal

Version statique compatible avec **GitHub Pages**. Le site est une page HTML/CSS/JavaScript qui affiche les publications contenues dans `docs/articles.json`. Un workflow GitHub Actions exécute chaque jour `collector.py`, collecte des flux RSS et met à jour ce fichier JSON.

## Installation dans le dépôt Newsletter-Hydro

1. Décompresser le projet.
2. Copier tous les fichiers et dossiers dans la racine du dépôt GitHub `Newsletter-Hydro` (remplacer l'ancien `README.md` si besoin).
3. Faire un commit et pousser les changements.
4. Dans GitHub : **Settings → Pages → Build and deployment**.
5. Choisir **Deploy from a branch**, branche `main` (ou votre branche principale), dossier **/docs**, puis Save.
6. Dans **Settings → Actions → General → Workflow permissions**, choisir **Read and write permissions**.
7. Ouvrir **Actions → Collecte du journal EDF Hydro → Run workflow** pour lancer une première collecte.
8. Recharger le site GitHub Pages. Les collectes suivantes sont planifiées chaque jour à 05:17 UTC.

## Important

GitHub Pages héberge uniquement des fichiers statiques. Il ne peut pas exécuter directement Python, Streamlit ou une base SQLite. Ici, GitHub Actions exécute le collecteur côté serveur et met à jour `docs/articles.json`; GitHub Pages affiche ensuite les données dans le journal.

Les flux RSS ne couvrent pas toute la presse ni toutes les pages régionales EDF. La liste `SOURCES` de `collector.py` est personnalisable. Les flux Google Actualités sont des résultats d'indexation, pas une garantie d'exhaustivité. Le filtre par mots-clés peut manquer des articles ou retenir des faux positifs. Vérifier les conditions d'utilisation des sources avant d'ajouter du scraping de pages web.

## Ajouter une source

Ajouter une ligne `( "Nom de la source", "URL_DU_FLUX_RSS" )` dans la liste `SOURCES` de `collector.py`.
