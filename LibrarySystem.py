from abc import ABC, abstractmethod
# Classe Utilisateur
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
        return self.__nombre_exemplaires > 0

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
    def get_details(self):
        pass


# Classe Livre (hérite de Document)
class Livre(Document):
    def __init__(self, titre, auteur, id_document, nombre_pages, nombre_exemplaires):
        super().__init__(titre, auteur, id_document, nombre_exemplaires)
        self.__nombre_pages = nombre_pages

    def get_nombre_pages(self):
        return self.__nombre_pages


# Classe Magazine (hérite de Document)
class Magazine(Document):
    def __init__(self, titre, auteur, id_document, numero, date_publication, nombre_exemplaires):
        super().__init__(titre, auteur, id_document, nombre_exemplaires)
        self.__numero = numero
        self.__date_publication = date_publication

    def get_numero(self):
        return self.__numero

    def get_date_publication(self):
        return self.__date_publication


# Classe DVD (hérite de Document)
class DVD(Document):
    def __init__(self, titre, auteur, id_document, duree, nombre_exemplaires):
        super().__init__(titre, auteur, id_document, nombre_exemplaires)
        self.__duree = duree

    def get_duree(self):
        return self.__duree


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


# Classe Lecteur (hérite de Utilisateur)
class Lecteur(Utilisateur):
    def __init__(self, nom, id_number, max_emprunts=3):
        super().__init__(nom, id_number)
        self.__emprunts = Emprunts(self, max_emprunts)

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


# Classe Bibliothécaire
class Bibliothecaire(Utilisateur):
    def __init__(self, nom, id_number):
        super().__init__(nom, id_number)
        self.__documents = []  # Liste de tous les documents dans la bibliothèque

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



# Création d'un bibliothécaire

bibliothecaire = Bibliothecaire("Mme Majdouline", 101)


# Création des documents

livre1 = Livre("Le Pain Nu", "Mohamed Choukri", "123456789", 328, 2)

magazine1 = Magazine("MaTourist", "Agence", 2024, 2, "2022-01-01", 5)

dvd1 = DVD("Interstellar", "Christopher Nolan", 3, "2h30min", 1)

livre2 = Livre("Le Prince", "Mekiaveli", "987654321", 128, 1)

print(bibliothecaire.ajouter_document(livre1))
print(bibliothecaire.ajouter_document(magazine1))
print(bibliothecaire.ajouter_document(dvd1))
print(bibliothecaire.ajouter_document(livre2))

print(bibliothecaire.afficher_documents())

lecteur1 = Lecteur("Adam Elmekadem", 1)

print(lecteur1.emprunter_document(livre1))
print(lecteur1.emprunter_document(magazine1))
print(lecteur1.emprunter_document(dvd1))
print(lecteur1.afficher_emprunts_actuels())
print(lecteur1.emprunter_document(livre2))

print(lecteur1.rendre_document(magazine1))
print(lecteur1.rendre_document(livre1))

print(lecteur1.afficher_historique())

