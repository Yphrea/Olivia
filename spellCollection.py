import yaml
from latexWrapper import latexEnvironment as texEnv

class spellCollection():
    def __init__(self, **kwargs):
        self.spellSpecs = dict(kwargs)
        for spellType, spells in self.spellSpecs.items():
            setattr(self, spellType, self._convertIntoSpellList(spellType, spells))

    def _convertIntoSpellList(self, spellType, spells):
        spellClass = None
        if spellType == 'tomes':
            spellClass = tome
        elif spellType == 'spellpage':
            spellClass = spellPage
        return [spellClass(**s) for s in spells]

    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def __repr__(self):
        return f"{self.__class__.__name__}(spellSpecs={dict(self.spellSpecs)})"

    
class spell:
    def __init__(self, **kwargs):
        self.spellSpecs = dict(kwargs)

    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.spellSpecs})"

    
class tome(spell):
    def __init__(self, **kwargs):
        self.spelltype='tome'
        super().__init__(**kwargs)


    def toTikzpicture(self):
        self.tp = texEnv('tikzpicture')
        self.tp.add_content(self.to_tikz())
        
    def toTikz(self):
        props = getattr(self, "spellSpecs", {})
        
        # Title handling
        title = str(props.get("title", "Unknown"))
        title_tex = title.title()
        image_file = 'spell_thumbnails/'+title.replace(" ", "_") + ".png"
        
        # Collect property lines (skip title)
        lines = []
        for key, value in props.items():
            if key == "title":
                continue

            # Convert lists nicely
            if isinstance(value, list):
                value = ", ".join(map(str, value))

            # Normalize key formatting
            key_tex = key.replace("_", " ").title()

            lines.append(f"{key_tex}: {value}\\\\")
    

        lines.append("Charges: ")

        properties_block = "\n    ".join(lines)

        latex = f"""\\node[anchor=north west, draw=none, text width=\\columnwidth, inner sep=0] (origin) at (0,0) {{\\vspace{{6pt}}}};
\\draw[very thick] (origin.west) -- (origin.east);
\\node[anchor=north west, inner sep=0] at (origin.south west) {{\\includegraphics[width=.28\\columnwidth]{{{image_file}}}}};
\\node[anchor=north east, inner sep=0, text width=0.70\\columnwidth] at (origin.south east) {{\\isCarriedCircle\\ \\textbf{{{title_tex}}}\n
{properties_block}}};\n"""

        return latex
