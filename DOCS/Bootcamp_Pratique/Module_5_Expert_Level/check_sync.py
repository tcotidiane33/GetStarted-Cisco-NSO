import json
from deepdiff import DeepDiff
import sys

print("🔍 Simulateur NSO : devices device routeur_ex0 check-sync")
print("-" * 60)

# 1. Charger la source de vérité (CDB)
try:
    with open("cdb_etat.json", "r") as f:
        cdb_config = json.load(f)
except FileNotFoundError:
    print("Erreur: Impossible de lire cdb_etat.json")
    sys.exit(1)

# 2. Charger ce qui a été vu réellement sur le réseau
try:
    with open("routeur_reel.json", "r") as f:
        real_config = json.load(f)
except FileNotFoundError:
    print("Erreur: Impossible de lire routeur_reel.json")
    sys.exit(1)

# 3. Calculer la différence (Le Hash/Diff NSO)
diff = DeepDiff(cdb_config, real_config, ignore_order=True)

if not diff:
    print("✅ in-sync: L'équipement correspond parfaitement à la base de données NSO.")
else:
    print("❌ out-of-sync: ALERTE ! Modification 'Out Of Band' détectée sur le réseau !")
    print("\nDétail des dérives métier (Diff):")
    
    # Formater la sortie de DeepDiff pour la rendre humainement lisible
    if 'dictionary_item_added' in diff:
        print("\n[+] Ajouts non autorisés sur le routeur :")
        for item in diff['dictionary_item_added']:
            print(f"  - {item}")
            
    if 'dictionary_item_removed' in diff:
        print("\n[-] Configurations supprimées manuellement :")
        for item in diff['dictionary_item_removed']:
            print(f"  - {item}")
            
    if 'values_changed' in diff:
        print("\n[~] Valeurs altérées :")
        for key, changes in diff['values_changed'].items():
            # key ressemble à root['GigabitEthernet1']['ip_address']
            path = key.replace("root", "").replace("'", "")
            print(f"  - {path} | NSO attendait: '{changes['old_value']}' -> Trouvé: '{changes['new_value']}'")

    print("-" * 60)
    print("Dans NSO, vous taperiez maintenant:")
    print("1. 'devices device routeur_ex0 sync-from' -> Pour accepter le changement (L'humain a raison).")
    print("2. 'devices device routeur_ex0 sync-to'   -> Pour écraser le changement (NSO a raison).")
