from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List

print("🛡️ NSO Validation Callback Simulator (Python/Pydantic)")
print("-" * 50)

# Définition du modèle de données de notre "Service" (Simule YANG avec des règles Python complexes)
class VlanService(BaseModel):
    vlan_id: int = Field(..., gt=0, lt=4095, description="ID du VLAN (1-4094)")
    name: str = Field(..., description="Nom du VLAN")
    devices: List[str] = Field(..., min_length=1, description="Liste des équipements cibles")

    # Règle Métier 1: Le VLAN ID doit être Pair !
    @field_validator('vlan_id')
    @classmethod
    def check_vlan_is_even(cls, value):
        if value % 2 != 0:
            raise ValueError(f"Transaction bloquée: L'entreprise exige que les VLANs soient des nombres pairs. {value} est impair.")
        return value

    # Règle Métier 2: Le nom du VLAN doit respecter la convention
    @field_validator('name')
    @classmethod
    def check_name_convention(cls, value):
        if not (value.startswith("PROD_") or value.startswith("DEV_")):
            raise ValueError(f"Transaction bloquée: Le nom '{value}' est invalide. Il DOIT commencer par 'PROD_' ou 'DEV_'.")
        return value

# ==========================================
# TEST: L'opérateur essaie de valider un service
# ==========================================

print("📥 Un opérateur DevOps tente de créer un service VLAN: VENTES (ID: 101) sur ex0")

intentional_data = {
    "vlan_id": 101,          # Faux ! Impair
    "name": "VENTES",        # Faux ! Pas de préfixe PROD/DEV
    "devices": ["ex0"]
}

try:
    # NSO vérifie la donnée *avant* d'appliquer
    service = VlanService(**intentional_data)
    print("✅ Validation NSO réussie ! Le commit peut s'exécuter.")

except ValidationError as e:
    print("❌ ERREUR LORS DU COMMIT (FASTMAP ABORT) :")
    for error in e.errors():
        print(f"  -> {error['msg']}")

print("\n💡 En changeant la donnée dans le script (ex: ID=100, name='PROD_VENTES'), le commit passera !")
