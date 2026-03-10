class latexEnvironment():
    def __init__(self, str::environmentName, list::required = '', list::optional = ''):
        self.begin = f"\\begin[optional]{{environmentName}}{{required}}\n"
        self.end = f"\\end{environmentName}\n"
        self.content = []

    def add_content(self, content):
        #TODO: assert content is string, latexEnvironment or list of those
        #TODO: assert/fix formatting with newlines and such
        self.content.append(content)

    def __str__(self):
        ret_str = self.begin
        for item in self.content:
            ret_str += item + '\n'*(not ret_str.endswith('\n'))
        ret_str += self.end
        return ret_str
                

class latexDocument(latexEnvironment):
    def __init__(self, str::documentName):
        self.documentName = document.Name+'.tex'*('.tex' not in documentName)
        self.documentSetup = f"""\\documentclass[12pt]{{article}}
        \\usepackage{{graphicx}} % Required for inserting images
        \\usepackage[margin=0.3in]{{geometry}}
        \\usepackage{{multicol}}
        \\usepackage{{tikz}}
        \n"""
        super().__init__('document')
        #self.openEnvironment = self
        
    def write():
        with open(self.documentName, 'w') as latexFile:
            latexFile.write(self)

    def __str__(self):
        return self.documentSetup += super().__str__()

    def compile(self):
        print("Compilation not implemented")

        
            
                
