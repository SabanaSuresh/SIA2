from database import Database

try:
    db = Database()
    print("✅ Connexion réussie à la base de données !")

    # On récupère toutes les interventions pour tester
    interventions = db.get_interventions()
    print("Interventions :", interventions)

    db.close()

except Exception as e:
    print("❌ Erreur lors de la connexion :", e)
