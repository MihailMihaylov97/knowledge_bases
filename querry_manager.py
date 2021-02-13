from rdfs import Resource
from context_manager import Context_Manager

class QueryExecutor:
    def __init__(self, context):
        self.context = context

    def run(self):        
        cmd = input("> ")
        while (cmd != "exit"):
            self.parse_command(cmd)
            cmd = input("> ")

    
    def parse_command(self, cmd):
        cmd = ' '.join(cmd.split())
        tokens = []
        i = 0
        while i < len(cmd):
            i = self.skip_whitespaces(cmd, i)            
            token, i = self.parse_command_token(cmd, i)
            tokens.append(token)
              
        if len(tokens) == 3:
            if tokens[0][0] == '?':
                self.execute_query_with_object(tokens[0], tokens[1], tokens[2])
            elif tokens[2][0] == '?':
                self.execute_query_with_subject(tokens[0], tokens[1], tokens[2])
            else:
                print("Incorect command.")

    def execute_query_with_object(self, subject_id, pred_name, object_id):
        if object_id[0] == "?":
            print("Incorect command.")
        obj = Resource(object_id)
        subjects = self.context.get_relation_object(pred_name, obj)
        if subjects is not None:
            for s in subjects:
                print(f"\t{s}")


    def execute_query_with_subject(self, subject_id, pred_name, object_id):
        if subject_id[0] == '?':
            print("Incorect command.")
        subj = Resource(subject_id)
        objects = self.context.get_relation_subject(pred_name, subj)
        if objects is not None:
            for o in objects:
                print(f"\t{o}")

        
    def parse_command_token(self, cmd, i):
        if i >= len(cmd):
            return None
        elif cmd[i] == '"':
            closing_quote_index = cmd.find('"', i+1)
            return cmd[i+1:closing_quote_index], closing_quote_index + 1
        elif cmd[i] == '<':
            closing_index = cmd.find(">", i+1)
            return cmd[i+1:closing_index], closing_index + 1
        else:
            whitespace_index = cmd.find(" ", i+1)
            if whitespace_index == -1:
                return cmd[i:], len(cmd)
            else:
                return cmd[i:whitespace_index], whitespace_index
    
    def skip_whitespaces(self, text, i):
        while (i < len(text) and (text[i] == " " or text[i] == "\n")):
            i += 1
        return i