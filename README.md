## Présentation

A partir d'un fichier de PPN et de zones bibliographiques MarcXML indiquées au lancement du script en ligne de commande, 
ce script interroge le SUDOC et récupère, *pour chaque PPN*, le contenu des zones souhaitées. 

En complément, utiliser [ce script](https://github.com/m-salvadori/ppn_where) pour récupérer
des informations sur la localisation des PPN.

## Mode d'emploi

Depuis le terminal, lancer le script suivi du chemin vers le fichier qui contient les PPN (1 PPN par ligne) et des zones bibliographiques MarcXML à interroger.

Exemple pour lancer le script à partir d'un dossier qui contient à la fois le script et le fichier de PPN :

```bash
./ppn_what.py ppn_sample.txt -z 010 200
```
ou (selon votre configuration) :

```powershell
python ppn_what.py ppn_sample.txt -z 010 200
```

### Prérequis

Python 3 + request library

### Limitations

La disctinction entre zones et sous-zones fonctionne à l'heure actuelle plutôt mal que bien : il est pour l'instant impossible de restreindre
la récupération précise du contenu situé entre deux balises *subfields*. Entrer 200$a en ligne de commande conduira de fait aux mêmes résultats que 200.

Il est recommandé de limiter à quelques centaines le nombre de PPN sur lesquels faire porter la requête.

Le script se fonde sur [ce webservice](https://documentation.abes.fr/sudoc/manuels/administration/aidewebservices/index.html#SudocMarcXML) de l'ABES
et partage donc ses particularités (déviations par rapport au format UNIMARC) et ses limitations (sur les ressources continues).

## To-do

- [ ] régler le problème d'extraction précise des subfields
- [ ] transformer le *for loop* en suite de fonctions
- [ ] clarifier le nom de certaines variables
