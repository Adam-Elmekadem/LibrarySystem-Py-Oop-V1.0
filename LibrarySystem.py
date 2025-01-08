from abc import ABC, abstractmethod

# Classe abstraite Utilisateur
class Utilisateur(ABC):
    def __init__(self, nom, id_number):
        self.__nom = nom
        self.__id_number = id_number

    def get_nom(self):
        return self.__nom

    def get_id(self):
        return self.__id_number

    @abstractmethod
    def role(self):
        pass


# Classe abstraite Document
class Document(ABC):
    def __init__(self, titre, auteur, id_document, nombre_exemplaires):
        self.__titre = titre
        self.__auteur = auteur
        self.__id_document = id_document
        self.__nombre_exemplaires = nombre_exemplaires

    def get_titre(self):
        return self.__titre

    def get_auteur(self):
        return self.__auteur

    def get_id(self):
        return self.__id_document

    def is_disponible(self):
        return ("Disponible" if self.__nombre_exemplaires > 0 else "Indisponible")

    def emprunter(self, lecteur):
        if self.is_disponible():
            self.__nombre_exemplaires -= 1
            return f"{lecteur.get_nom()} a emprunté '{self.__titre}'."
        else:
            return f"Le document '{self.__titre}' n'est pas disponible."

    def render_document(self):
        self.__nombre_exemplaires += 1
        return f"Le document '{self.__titre}' a été rendu."

    @abstractmethod
    def description(self):
        pass


# Sous-classes concrètes pour Document
class Livre(Document):
    def __init__(self, titre, auteur, id_document, nombre_pages, nombre_exemplaires):
        super().__init__(titre, auteur, id_document, nombre_exemplaires)
        self.__nombre_pages = nombre_pages

    def get_nombre_pages(self):
        return self.__nombre_pages

    def description(self):
        return f"Livre: {self.get_titre()} ({self.get_auteur()}), Pages: {self.__nombre_pages}"


class Magazine(Document):
    def __init__(self, titre, auteur, id_document, numero, date_publication, nombre_exemplaires):
        super().__init__(titre, auteur, id_document, nombre_exemplaires)
        self.__numero = numero
        self.__date_publication = date_publication

    def get_numero(self):
        return self.__numero

    def get_date_publication(self):
        return self.__date_publication

    def description(self):
        return f"Magazine: {self.get_titre()} (N°{self.__numero}), Date: {self.__date_publication}"


class DVD(Document):
    def __init__(self, titre, auteur, id_document, duree, nombre_exemplaires):
        super().__init__(titre, auteur, id_document, nombre_exemplaires)
        self.__duree = duree

    def get_duree(self):
        return self.__duree

    def description(self):
        return f"DVD: {self.get_titre()} ({self.get_auteur()}), Durée: {self.__duree}"

# Classe Emprunts
class Emprunts:
    def __init__(self, lecteur, max_emprunts=3):
        self.lecteur = lecteur
        self.__emprunts_actuels = []
        self.__historique = []
        self.__max_emprunts = max_emprunts

    def get_emprunts_actuels(self):
        return self.__emprunts_actuels

    def get_historique(self):
        return self.__historique

    def emprunter(self, document):
        if len(self.__emprunts_actuels) >= self.__max_emprunts:
            return f"{self.lecteur.get_nom()} a atteint la limite maximale d'emprunts ({self.__max_emprunts})."
        if document.is_disponible():
            self.__emprunts_actuels.append(document)
            self.__historique.append(document)
            return document.emprunter(self.lecteur)
        else:
            return f"Le document '{document.get_titre()}' n'est pas disponible."

    def rendre(self, document):
        if document in self.__emprunts_actuels:
            self.__emprunts_actuels.remove(document)
            return document.render_document()
        else:
            return f"{self.lecteur.get_nom()} n'a pas emprunté le document '{document.get_titre()}'."

    def afficher_historique(self):
        historique = [doc.get_titre() for doc in self.__historique]
        return f"Historique des emprunts de {self.lecteur.get_nom()}: {', '.join(historique) if historique else 'Aucun emprunt.'}"

    def afficher_emprunts_actuels(self):
        emprunts = [doc.get_titre() for doc in self.__emprunts_actuels]
        return f"Emprunts actuels de {self.lecteur.get_nom()}: {', '.join(emprunts) if emprunts else 'Aucun emprunt en cours.'}"


# Sous-classes concrètes pour Utilisateur
class Lecteur(Utilisateur):
    def __init__(self, nom, id_number, max_emprunts=3):
        super().__init__(nom, id_number)
        self.__emprunts = Emprunts(self, max_emprunts)

    def role(self):
        return "Lecteur"

    def get_emprunts(self):
        return self.__emprunts

    def emprunter_document(self, document):
        return self.__emprunts.emprunter(document)

    def rendre_document(self, document):
        return self.__emprunts.rendre(document)

    def afficher_historique(self):
        return self.__emprunts.afficher_historique()

    def afficher_emprunts_actuels(self):
        return self.__emprunts.afficher_emprunts_actuels()


class Bibliothecaire(Utilisateur):
    def __init__(self, nom, id_number):
        super().__init__(nom, id_number)
        self.__documents = []  # Liste de tous les documents dans la bibliothèque

    def role(self):
        return "Bibliothécaire"

    def ajouter_document(self, document):
        self.__documents.append(document)
        return f"Document '{document.get_titre()}' ajouté par {self.get_nom()}."

    def supprimer_document(self, id_document):
        for document in self.__documents:
            if document.get_id() == id_document:
                self.__documents.remove(document)
                return f"Document '{document.get_titre()}' supprimé par {self.get_nom()}."
        return f"Aucun document avec l'ID '{id_document}' trouvé."

    def afficher_documents(self):
        if not self.__documents:
            return "Aucun document dans la bibliothèque."
        return "Documents disponibles :\n" + "\n".join(
            [f"{doc.get_titre()} ({doc.get_auteur()}) - Exemplaires : {doc.is_disponible()}" for doc in self.__documents]
        )

    def get_document_par_id(self, id_document):
        for document in self.__documents:
            if document.get_id() == id_document:
                return document
        return None

# Création d'un bibliothécaire

bibliothecaire = Bibliothecaire("Mme Majdouline", 101)

def ajouterDocument():
    print("\nQue voullez-vous ajouter ?")
    print("1. Livre")
    print("2. Magazine")
    print("3. DVD")

    choix = input("Entrez le numéro de votre choix : ")

    if choix == "1":
        titre = input("Entrez le titre du livre : ")
        auteur = input("Entrez l'auteur du livre : ")
        id_document = input("Entrez l'ID du document : ")
        nombre_pages = int(input("Entrez le nombre de pages : "))
        nombre_exemplaires = int(input("Entrez le nombre d'exemplaires : "))
        livre = Livre(titre, auteur, id_document, nombre_pages, nombre_exemplaires)
        print(bibliothecaire.ajouter_document(livre))

    elif choix == "2":
        titre = input("Entrez le titre du magazine : ")
        auteur = input("Entrez l'auteur du magazine : ")
        id_document = input("Entrez l'ID du document : ")
        nombre_pages = int(input("Entrez le nombre de pages : "))
        nombre_exemplaires = int(input("Entrez le nombre d'exemplaires : "))
        date_publication = input("Entrez la date de publication (YYYY-MM-DD) : ")
        magazine = Magazine(titre, auteur, id_document, date_publication, nombre_exemplaires)
        print(bibliothecaire.ajouter_document(magazine))

    elif choix == "3":
        titre = input("Entrez le titre du DVD : ")
        auteur = input("Entrez l'auteur du DVD : ")
        id_document = input("Entrez l'ID du document : ")
        nombre_pages = int(input("Entrez le nombre de pages : "))
        nombre_exemplaires = int(input("Entrez le nombre d'exemplaires : "))
        duree = input("Entrez la durée du DVD : ")
        dvd = DVD(titre, auteur, id_document, nombre_pages, nombre_exemplaires, duree)
        print(bibliothecaire.ajouter_document(dvd))

    else:
        print("choix invalide. Veuillez réessayer.")
        ajouterDocument()

def suprimerDocument():
    print("\nQue voullez-vous supprimer ?")
    print("1. Livre")
    print("2. Magazine")
    print("3. DVD")
    choix = input("Entrez le numéro de votre choix : ")
    if choix == "1":
        id_document = input("Entrez l'ID du document à supprimer : ")
        print(bibliothecaire.supprimer_document(id_document))
    elif choix == "2":
        id_document = input("Entrez l'ID du document à supprimer : ")
        print(bibliothecaire.supprimer_document(id_document))
    elif choix == "3":
        id_document = input("Entrez l'ID du document à supprimer : ")
        print(bibliothecaire.supprimer_document(id_document))
    else:
        print("choix invalide. Veuillez réessayer.")
        suprimerDocument()

def afficherDocuments():
    print(bibliothecaire.afficher_documents())

def Login_admin():
    print("\nBienvenue dans le système de gestion de la bibliothèque")
    print("Veuillez entrer votre nom d'utilisateur et votre mot de passe pour accéder à l'interface d'administration.\n")

    while True:
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")

        if password == "admin":

            while True:
                print("\nMenu Administrateur :")
                print("1. Ajouter un document")
                print("2. Supprimer un document")
                print("3. Afficher les documents")
                print("4. Retour au menu principal")

                choix_menu = input("Entrez le numéro de votre choix : ")
                if choix_menu == "1":
                    ajouterDocument()
                elif choix_menu == "2":
                    suprimerDocument()
                elif choix_menu == "3":
                    afficherDocuments()
                elif choix_menu == "4":
                    break
                else:
                    print("Choix invalide. Veuillez réessayer.")
            break  # Sortir du login après le menu
        else:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")

def Login_lecteur():
    print("\nBienvenue dans le système de gestion de la bibliothèque")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe (au moins 8 caractères) : ")

    if len(password) >= 8:
        lecteur = Lecteur(username, 123)  # Remplacez 123 par un identifiant unique
    else:
        print("Le mot de passe doit contenir au moins 8 caractères.")
        return

    while True:
        print("\nMenu Lecteur :")
        print("1. Emprunter un document")
        print("2. Rendre un document")
        print("3. Afficher historique des emprunts")
        print("4. Afficher emprunts actuels")
        print("5. Retour au menu principal")

        choix = input("Entrez le numéro de votre choix : ")
        if choix == "1":
            id_document = input("Entrez l'ID du document à emprunter : ")
            document = bibliothecaire.get_document_par_id(id_document)
            if document:
                print(lecteur.emprunter_document(document))
            else:
                print(f"Aucun document trouvé avec l'ID '{id_document}'.")
        elif choix == "2":
            id_document = input("Entrez l'ID du document à rendre : ")
            document = bibliothecaire.get_document_par_id(id_document)
            if document:
                print(lecteur.rendre_document(document))
            else:
                print(f"Aucun document trouvé avec l'ID '{id_document}'.")
        elif choix == "3":
            print(lecteur.afficher_historique())
        elif choix == "4":
            print(lecteur.afficher_emprunts_actuels())
        elif choix == "5":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")



def main_menu():
    print("Bienvenue dans le système de gestion de la bibliothèque")
    while True:
        print("\nMenu principal :")
        print("1. Connexion en tant qu'administrateur")
        print("2. Connexion en tant que lecteur")
        print("3. Quitter")

        choix = input("Entrez le numéro de votre choix : ")

        if choix == "1":
            Login_admin()
        elif choix == "2":
            Login_lecteur()
        elif choix == "3":
            print("Merci d'avoir utilisé le système. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main_menu()


