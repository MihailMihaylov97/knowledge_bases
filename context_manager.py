from rdfs import *

class Context_Manager:
    def __init__(self):
        self.properties = {}
        self.classes = {}        
        self.statements = {}      
        self.add_defaults()

    def add_statement(self, statement):
        if statement.get_predicate_name() == RDFProperties.Type.value:
            self.rdf_type(statement)
        elif statement.get_predicate_name() == RDFProperties.SubClassOf.value:
            self.rdf_subclass(statement)
        elif statement.get_predicate_name() == RDFProperties.Domain.value:
            self.handle_rdf_domain(statement)
        else:
            self.add_statement_if_not_present(statement)

    def add_statement_if_not_present(self, stmt):
        rdf_domain = self.get_relation_subject(RDFProperties.Domain.value, self.properties[stmt.predicate_name])
        rdf_range = self.get_relation_subject(RDFProperties.Range.value, self.properties[stmt.predicate_name])
            
        if rdf_domain and not all(self.is_instance_of(stmt.get_subject(), x) for x in rdf_domain): 
            print("Please check your ontology for domain mistakes.")
            return
        if rdf_range and not all(self.is_instance_of(stmt.get_object(), x) for x in rdf_range):
            print("Please check your ontology for range mistakes.")
            return
        if stmt.get_predicate_name() not in self.statements:
            self.statements[stmt.get_predicate_name()] = list()
        self.statements[stmt.get_predicate_name()].append(stmt)

    def handle_rdf_domain(self, statement):
        if self.is_class_in_ctxt(statement.get_object().id) and self.is_property(statement.get_subject()):
            self.add_statement_if_not_present(statement)
        else:
            print("Please check your ontology for mistakes.")
        

    def rdf_type(self, statement):
        if self.is_class_in_ctxt(statement.get_object().id):
            if statement.get_object().id == RDFResources.Property.value:
                self.add_prop(statement.get_subject())
            elif statement.get_object().id == RDFResources.Class.value:
                self.add_class(statement.get_subject())
            else:
                self.add_statement_if_not_present(statement)
        else:
            print(statement.get_object(), "Does not exist as a class. Please add it as a class first.")

    def rdf_subclass(self, statement):

        if self.is_class_in_ctxt(statement.get_object().id) and self.is_class_in_ctxt(statement.get_subject().id):
            self.add_statement_if_not_present(statement)
        else:
            print(f"{statement.get_object()} and {statement.get_subject()} if you want to handle subclasses.")

    def add_prop(self, prop):
        if prop.id not in self.properties:
            self.properties[prop.id] = prop
        else:
            print("This property already exists: ", prop.id)

    def get_instances_of_class(self, class_id):
        if class_id not in self.classes:
            print("Sorry, but this class is not present in the knowledge base: ", class_id)
            return []
        else:
            all_instances = self.get_relation_object(RDFProperties.Type.value, Class(class_id))
            for _, c in self.classes.items():
                if c.id != class_id and self.is_subtype_of(c, Resource(class_id)):
                    all_instances = all_instances + self.get_relation_object(RDFProperties.Type.value, c)
            return all_instances
                                
    def check_predicate_in_context(self, prop_id, obj_id, subj_id):
        statements = self.statements[prop_id]
        for s in statements:
            if s.obj.id == obj_id and s.subj_id == subj_id:
                return True
        return False

    def is_class_in_ctxt(self, class_id):
        return class_id in self.classes
    
    def is_property(self, prop):
        return prop.id in self.properties

    def is_instance_of(self, subj, obj):
        return subj in self.get_instances_of_class(obj.id)

    def add_class(self, class_obj):
        if class_obj.id not in self.classes:
            self.classes[class_obj.id] = class_obj

    def get_all_statements_of_property(self, prop):
        if prop not in self.properties:
            return None
        else:
            result = []
            for triple in self.statements[prop]:
                result.append( (triple.object, triple.subject) )
            return result

    def get_relation_object(self, prop, obj):
        if prop not in self.properties:
            print("This property is not in the system: ", prop)
            return None
        else:
            result = []

            for triple in self.statements[prop]:
                if triple.object == obj:
                    result.append( triple.subject )
            return result

    def get_relation_subject(self, prop, subject):
        if prop not in self.properties:
            print("This property is not in the system: ", prop)
            return None
        elif prop in self.statements:
            result = []
            for triple in self.statements[prop]:
                if triple.subject == subject:
                    result.append( triple.object )
            return result
        return []

    def is_subtype_of(self, subj, obj):
        if subj == obj: 
            return True
        superTypes = self.get_relation_object(RDFProperties.SubClassOf.value, obj)
        if not superTypes:
            return False 
        else:
            return any(x == subj or self.is_subtype_of(subj, x) for x in superTypes)

    def add_defaults(self):
        for cl in RDFResources:
            cobj = Class(cl.value)
            self.add_class(cobj)
        for pr in RDFProperties:
            prop = Property(pr.value)
            self.add_prop(prop)
        self.statements[RDFProperties.Domain.value] = [Statement(RDFProperties.Domain.value, Class(RDFResources.Property.value), Class(RDFResources.Class.value))]
