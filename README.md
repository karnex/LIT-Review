# LITReview
***********************************************************************************************************************
## Présentation

###### LITReview a pour objectif de commercialiser un produit permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande. 

## Configurer l'application

### Cloner le dépôt distant
1) Dans votre terminal, déplacez-vous dans le dossier de votre choix: cd path_of_your_choice
2) Cloner le dépôt distant vers notre nouveu dossier:<br/> 
```git clone git@github.com:karnex/LIT-Review.git```

### Configuration pour système Windows

5) Céer l'environnement virtuel:<br/> 
```python -m venv env```
6) Activer l'environnement virtuel:<br/> 
```env\Scripts\activate```
7) Installer toutes les dépendances utiles au projet:<br/>
```pip install -r requirements.txt```

### Configuration pour système Unix

5) Créer l'environnement virtuel:<br/> 
```python3 -m venv env```
6) Activer l'environnement virtuel:<br/> 
```source env/bin/activate```
7) Installer toutes les dépendances utiles au projet:<br/> 
```pip3 install -r requirements.txt```

## Exécuter et utiliser l'application

**1) Exécuter l'application**

- Sur un appareil Windows:<br/> 
```python manage.py runserver```
- Sur un appareil Unix:<br/> 
```python3 manage.py runserver```

**2) Accéder à l'application web**

- Par l'intermédiaire du navigateur web de votre choix, accéder à l'URL suivante:<br/>
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

**3) Se connecter avec un compte utilisateur**

Afin de visualiser du contenu et de pouvoir utiliser toutes les possibilités de l'application,<br/>
je vous invite à vous connecter avec le compte suivant:
- Nom d'utilisateur: _bruno_
- Mot de passe: _litreview_

Have fun ! 😏

------------------------------------------------------------
### Utilisation de Flake8

##### Installer Flake8 et son plugin de génération de rapport html

Sur un appareil Windows:<br/>
```pip install flake8 flake8_html```

Sur un appareil Unix:<br/>
```pip3 install flake8 flake8_html```

#### Fichier de configuration

La configuration de flake8 est ici gérée par l'intermédiaire du fichier setup.cfg qui se trouve à la racine du projet.

#### Générer un raport flake8-html

```flake8 --format=html --htmldir=flake8_rapport```

