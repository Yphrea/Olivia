class latexEnvironment:
    indentation = "   "
    def __init__(self, environmentName:str, required:list = None, optional:list = None):
        self.environmentName = environmentName
        self.requiredOptions = required
        self.optionalOptions = optional
        self.content = []
        self.updateEnvironmentStrings()
        
    def updateEnvironmentStrings(self):
        options = {'optional':self.optionalOptions, 'required':self.requiredOptions}
        optional_str = ''; required_str = ''
        for key, option in options.items():
            if not type(option) == list:
                options[key] = [option]
            if options[key] != [None]:
                if key == 'optional':
                    optional_str = f"[{','.join(options[key])}]"
                else:
                    required_str = f"{{{','.join(options[key])}}}"
                    
        self.begin = f"\\begin{optional_str}{{{self.environmentName}}}{required_str}\n"
        self.end = f"\\end{{{self.environmentName}}}\n"

    def addContent(self, addition, setParent=False):
        if setParent:
            addition.setParent(self)
        if isinstance(addition, list):
            self.content += addition
        elif isinstance(addition, str) or isinstance(addition, latexEnvironment):
            self.content.append(addition)
        else:
            print(type(self))
            raise TypeError("addition must be list, str or latexEnvironment. You attempted to add %s" % type(addition))
        
    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
        
    def __str__(self):
        ret_str = self.begin
        for item in self.content:
            aux_str = str(item).replace('\n', '\n'+self.indentation).strip(self.indentation)
            ret_str += self.indentation+aux_str
        ret_str += self.end
        return ret_str
                

class latexDocument(latexEnvironment):
    def __init__(self, documentName:str):
        self.documentName = documentName+'.tex'*('.tex' not in documentName)
        self.documentPreamble = f"""\\documentclass[12pt]{{article}}
\\usepackage{{graphicx}} % Required for inserting images
\\usepackage[margin=0.3in]{{geometry}}
\\usepackage{{multicol}}
\\usepackage{{tikz}}
\\usetikzlibrary{{shapes}}
\n
\\setlength\\parindent{{0pt}}
\\newcommand{{\\isCarriedCircle}}{{\\raisebox{{0.5pt}}{{\\tikz{{\\node[draw,scale=6,circle,fill=none](){{}};}}}}}}
\n"""
        super().__init__('document')
        
    def write(self):
        with open(self.documentName, 'w') as latexFile:
            latexFile.write(str(self))

    def __str__(self):
        return self.documentPreamble + super().__str__()


        
            
                
