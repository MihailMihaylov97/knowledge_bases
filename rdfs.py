from enum import Enum

class Statement:
    def __init__(self, predicate_name, subj, obj):
        self.predicate_name = predicate_name
        self.subject = subj
        self.object = obj
    def get_predicate_name(self):
        return self.predicate_name

    def get_subject(self):
        return self.subject
    
    def get_object(self):
        return self.object

    def __str__(self):
        return f"{self.subject} - {self.predicate_name} - {self.object}"

class Resource:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id

class Property(Resource):
    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return self.id

class Class(Resource):
    def __init__(self, id):
        super().__init__(id)
        

class RDFResources(Enum):
    Class = "rdfs:Class"
    Literal = "rdfs:Literal"
    Resource = "rdfs:Resource"
    Property = "rdf:Property"
    Description = "rdf:Description"

class RDFProperties(Enum):
    SubClassOf = "rdfs:subClassOf"
    Type = "rdf:type"
    SubPropertyOf = "rdfs:subPropertyOf"
    Domain = "rdfs:domain"
    Range = "rdfs:range"


def DataType(Resource):
    def __init__(self, id):
        super().__init__(id)


class Literal(Class):
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, Literal)
