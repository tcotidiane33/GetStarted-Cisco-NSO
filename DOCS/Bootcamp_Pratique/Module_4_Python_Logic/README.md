# Module 4 : Puissance et Logique Python

Bien que le XML et YANG fassent 90% du travail dans NSO, certains besoins métiers nécessitent du code.
Exemples réels :
- Calculer une adresse IP libre dans un sous-réseau.
- Vérifier qu'un nom de VPN respecte la convention de nommage de l'entreprise.
- Appeler une API ServiceNow pour vérifier qu'un ticket de changement (CHG) est bien ouvert avant d'autoriser la configuration.

## 🎯 Exercice Pratique : Valider des données métier avec Python

Dans NSO, ce processus s'appelle un **Validation Callback**. Avant même que NSO n'essaie de générer la configuration CLI, il exécute un script Python qui a le droit de dire "Non, ces données d'entrées sont invalides".

Pour simuler cela sans NSO, nous allons utiliser `Pydantic`, la librairie Python standard pour la validation de données (utilisée par FastAPI par exemple).

### 🛠 Pré-requis
1. Python 3
2. Installer Pydantic :
   ```bash
   pip3 install pydantic
   ```

### 📝 Cas Pratique
Ouvrez le script `validation_nso.py`. 
Ce script simule un modèle YANG mais avec la puissance de Python pour ajouter des règles impossibles à décrire en pur YANG.

**Règles d'entreprise simulées :**
1. L'ID du VLAN doit être obligatoirement pair.
2. Le nom du VLAN doit absolument commencer par `PROD_` ou `DEV_`.

**Étape 1 : Analyser le code**
Lisez comment les validateurs `@field_validator` sont construits en Python. C'est exactement la logique d'un code NSO.

**Étape 2 : Exécuter le test**
```bash
python3 validation_nso.py
```
**Résultat attendu :**
Le script va volontairement essayer de créer un VLAN invalide ("VENTES" au lieu de "PROD_VENTES" avec un ID impair "101"). Le script Python doit intercepter l'erreur, la lever proprement, et bloquer la "transaction", exactement comme le ferait NSO avec un message d'erreur rouge dans son interface web.
