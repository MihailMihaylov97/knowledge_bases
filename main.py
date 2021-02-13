from context_manager import Context_Manager
from doc_parser import Doc_Parser
from querry_manager import QueryExecutor

from rdfs import *


if __name__ == "__main__":
    context = Context_Manager()
    print("Loading data from file...")
    parser = Doc_Parser()
    triplets = parser.read_from_file()
    for subj, pred, obj in triplets:
        if isinstance(obj, Literal):
            statement = Statement(RDFProperties.Type.value, obj, Resource(RDFResources.Literal.value))
            context.add_statement(statement)
        statement = Statement(pred, subj, obj)
        context.add_statement(statement)
    print("classes: ",context.classes)
    print("properties: ",context.properties)
    print("statements: ",context.statements)
    qe = QueryExecutor(context)
    qe.run()


