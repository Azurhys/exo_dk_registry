# Projet de Scraping et Analyse de Données de Crypto-Monnaies
Ce projet consiste à scraper les données des crypto-monnaies à partir d'un site web et à les analyser. Le code est écrit en Python et utilise les bibliothèques BeautifulSoup pour le scraping web et matplotlib pour l'analyse des données.

## Contenu du Projet
Le projet comprend les fichiers suivants :

**Crypto_Scrap.py:** Ce fichier contient le code Python pour scraper les données des crypto-monnaies à partir d'un site web, les filtrer et les insérer dans une base de données MySQL.

**README.md:** Ce fichier contient la documentation du projet, expliquant comment utiliser le code et fournissant des informations sur son fonctionnement.

## Installation
Pour exécuter ce projet, vous aurez besoin d'installer Python ainsi que les bibliothèques BeautifulSoup et matplotlib. Vous aurez également besoin d'un serveur MySQL pour stocker les données.

Assurez-vous d'avoir Python installé sur votre système. Vous pouvez le télécharger depuis le site officiel de Python.

Installez les bibliothèques requises en exécutant la commande suivante dans votre terminal :

```
pip install bs4 matplotlib mysql-connector-python
```

Assurez-vous d'avoir un serveur MySQL en cours d'exécution. Vous pouvez installer MySQL depuis MySQL Downloads.

## Utilisation
Exécutez le script scrap_cryptos.py pour scraper les données des crypto-monnaies, les filtrer et les insérer dans la base de données MySQL. Assurez-vous de modifier les informations de connexion MySQL dans le script selon vos paramètres. Ce script tracera aussi la corrélation entre la capitalisation boursière et le prix du token.

```
python Crypto_Scrap.py
```

Vous pouvez également explorer les autres parties du code pour personnaliser ou étendre les fonctionnalités du projet selon vos besoins.

