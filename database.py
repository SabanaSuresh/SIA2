import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # ton utilisateur MySQL
            password="",  # ton mot de passe MySQL (123soleil)
            database="airblio"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def get_interventions(self):
        self.cursor.execute("SELECT * FROM interventions")
        return self.cursor.fetchall()

    def add_intervention(self, id, reference_demande, intitule, date_intervention, lieu, statut, importance, equipement, membre, description, cout):
        query = """
            INSERT INTO interventions (
                id, reference_demande, intitule, date_intervention, lieu, statut, importance,
                equipement, membre, description, cout
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (id, reference_demande, intitule, date_intervention, lieu, statut, importance,
                equipement, membre, description, cout)
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_demandes(self): 
        query = "SELECT * FROM demandes"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_equipements(self):
        query = "SELECT * FROM equipements"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_projets(self):
        query = "SELECT * FROM projets"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def verifier_utilisateur(self, email, mot_de_passe):
        query = "SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s"
        self.cursor.execute(query, (email, mot_de_passe))
        result = self.cursor.fetchone()
        return result is not None

    def delete_demande(self, demande_id):
        try:
            query = "DELETE FROM demandes WHERE numero_demande = %s"
            self.cursor.execute(query, (demande_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression de la demande {demande_id} : {e}")



    def close(self):
        self.cursor.close()
        self.conn.close()
