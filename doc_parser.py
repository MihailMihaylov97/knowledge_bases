from rdfs import RDFProperties, Literal, Resource

class Doc_Parser:
    def read_from_file(self, filename = "data.ttl"):
        f = open(filename, "r")
        text = self.uniform_whitespace(f.read())
        i = 0 
        triplets = []
        while(i < len(text)):
            i = self.skip_whitespaces(text, i) 
            subj, i = self.read_input(text, i)
            i = self.skip_whitespaces(text, i)
            pred, i = self.parse_property_from_text(text, i)
            i = self.skip_whitespaces(text, i)          
            obj, i = self.read_input(text, i)
            i = self.skip(text, i) 
            i = self.skip_whitespaces(text, i)
            triplets.append((subj, pred, obj))
        return triplets

    def read_input(self, text, i):
        if i >= len(text)-1:
            return None, i + 1
        if text[i] == '"':
            tmp_i = text.find('"', i+1)
            if tmp_i > 0:
                return Literal(text[i+1:tmp_i]), tmp_i + 1
        elif text[i] == "<":
            tmp_i = text.find(">", i+1)
            if tmp_i > 0 and i < len(text):
                return Resource(text[i+1:tmp_i]), tmp_i + 1
        elif text[i] != '"' and text[i] != "<":
            tmp_i = text.find(" ", i+1)
            return Resource(text[i:tmp_i]), tmp_i + 1
        else:
            return None, i

    def parse_property_from_text(self, text, i):
        if i >= len(text)-1:
            return None, i + 1
        tmp_i = text.find(" ", i+1)
        pred = text[i:tmp_i]
        if text[i] == "<":
            pred = text[i+1:tmp_i-1]
        if pred == "a":
            pred = RDFProperties.Type.value
        return pred, tmp_i

    def skip_whitespaces(self, text, i):
        while (i < len(text) and (text[i] == " " or text[i] == "\n")):
            i += 1
        return i

    def skip(self, text, i):
        while (i < len(text) and text[i] != "."):
            i += 1
        return i + 1

    def uniform_whitespace(self, text):
        return ' '.join(text.split())