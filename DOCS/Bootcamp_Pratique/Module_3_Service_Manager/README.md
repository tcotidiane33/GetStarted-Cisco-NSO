# Module 3 : Le Service Manager & Le FASTMAP Simulés

C'est le cœur de NSO ! L'utilisateur ne définit qu'une "intention" (ex: "Je veux un VLAN 100 qui s'appelle VENTES sur ex0 et ex1"). NSO génère lui-même la conf finale.

Dans cet exercice, nous allons simuler le **Template XML** de NSO en utilisant Jinja2, un moteur de template Python très populaire.

## 🎯 Exercice Pratique : Générer de la configuration depuis la donnée (Template)

### 🛠 Pré-requis
1. Python 3
2. Installer Jinja2 et YAML :
   ```bash
   pip3 install jinja2 pyyaml
   ```

### 📝 Cas Pratique
Observez les deux fichiers dans ce dossier :
1. `intention-utilisateur.yaml` : Représente ce que le NOC entrerait dans la CLI de NSO (la donnée d'entrée).
2. `vlan-template.j2` : Représente le XML Template de NSO. Il contient des variables pures (`{{ vlan.id }}`).

**Étape 1 : Analyser le moteur (Service Manager)**
Ouvrez le script `service_manager.py`. Ce script lit l'entrée de l'utilisateur et la fusionne avec le template. C'est l'essence même de ce que fait la VM Java interne de NSO.

**Étape 2 : Exécuter la génération (Le "Commit Dry-Run")**
```bash
python3 service_manager.py
```

**Résultat attendu :**
Le script doit lire que vous voulez le VLAN `100` sur `ex0` et `ex1`, et il doit générer et afficher la commande CLI Cisco native :
```cisco
! Configuration pour device: ex0
interface Vlan100
 description VENTES
 no shutdown

! Configuration pour device: ex1
interface Vlan100
 description VENTES
 no shutdown
```
Ceci est un excellent moyen de comprendre l'isolation entre **Modèle de Donnée** et **Template d'Équipement** qui rend NSO si puissant pour le multivendeur.
