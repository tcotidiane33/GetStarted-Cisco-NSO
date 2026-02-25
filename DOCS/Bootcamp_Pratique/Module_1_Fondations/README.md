# Module 1 : Les Fondations (YANG)

Dans NSO, tout commence par un modèle de données YANG. Ce langage décrit l'intention ou la configuration réseau de manière hiérarchique et typée.

## 🎯 Exercice Pratique : Comprendre et Valider un Modèle YANG

Nous allons utiliser `pyang` (l'outil open source standard de l'IETF) pour valider et visualiser un modèle YANG qui représente la configuration d'un VLAN, similaire à ce que NSO utiliserait en interne pour générer son interface utilisateur (CLI ou web).

### 🛠 Pré-requis
1. Avoir Python 3 installé.
2. Installer `pyang` :
   ```bash
   pip3 install pyang
   ```

### 📝 Cas Pratique
Ouvrez le fichier `simple-vlan.yang` inclus dans ce dossier. Observez sa structure :
- Un `container` pour le service.
- Une `list` des vlans.
- Des "feuilles" (`leaf`) avec des types strictement définis (un VLAN ID ne peut aller que de 1 à 4094).

**Étape 1 : Valider la syntaxe du modèle**
```bash
pyang simple-vlan.yang
```
*(S'il n'y a pas de sortie texte, c'est que la syntaxe est parfaite !)*

**Étape 2 : Visualiser le modèle en arbre (Tree)**
NSO fait exactement cela pour construire sa CLI.
```bash
pyang -f tree simple-vlan.yang
```
**Résultat attendu :**
Vous devriez voir un arbre hiérarchique avec `+--rw vlan* [vlan-id]` montrant que `vlan-id` est la clé principale.

### 🧪 Pour aller plus loin (Test)
Modifiez le fichier `simple-vlan.yang`.
- Changez la limite (range) du `vlan-id` pour aller de `100..200`.
- Relancez la validation `pyang` avec une fausse donnée ou observez simplement comment la contrainte de type garantit qu'aucune mauvaise saisie ne sera envoyée aux équipements réseau !
