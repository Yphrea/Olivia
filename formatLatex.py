import yaml

class spellCollection():
    def __init__(self, **kwargs):
        self.contents = dict(kwargs)
        for spellType, spells in self.contents.items():
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
        return f"{self.__class__.__name__}(contents={dict(self.contents)})"

    
class spell:
    def __init__(self, **kwargs):
        self.contents = dict(kwargs)

    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_tikz(self, obj_key):
        """
        Represent a top-level object (like 'tome') as a LaTeX tikzpicture string.
        obj_key: the key of the object inside self.properties (e.g., 'tome')
        """
        if obj_key not in self.properties:
            raise ValueError(f"Object key '{obj_key}' not found in properties")

        obj = self.properties[obj_key]

        # Get image path if exists, else empty string
        image_path = obj.get("image_file_path", "")

        # Build the LaTeX lines for all properties except image_file_path
        lines = []
        for k, v in obj.items():
            if k == "image_file_path":
                continue
            # Replace newlines in description with LaTeX line breaks
            if isinstance(v, str) and "\n" in v:
                v = v.replace("\n", " ")
            lines.append(f"{k.capitalize()}: {v}")

        properties_str = "\\\\\n            ".join(lines)

        tikz_str = f"""\\noindent\\begin{{tikzpicture}}
    \\node[anchor=north west, draw=none, text width=\\columnwidth, inner sep=0] (origin) at (0,0) {{\\vspace{{6pt}}}};
    \\draw[very thick] (origin.west) -- (origin.east);
    \\node[anchor=north west, inner sep=0] at (origin.south west) {{\\includegraphics[width=.33\\columnwidth]{{{image_path}}}}};
    \\node[anchor=north east, inner sep=0, text width=0.65\\columnwidth] at (origin.south east) {{\\textbf{{{obj.get('title', obj_key)}}}
            {properties_str}}};
\\end{{tikzpicture}}"""

        return tikz_str
    

    def __repr__(self):
        return f"{self.__class__.__name__}({self.contents})"

    
class tome(spell):
    def __init__(self, **kwargs):
        self.spelltype='tome'
        super().__init__(**kwargs)

    
    def to_tikz(self):
        props = getattr(self, "contents", {})
        
        # Title handling
        title = str(props.get("title", "Unknown"))
        title_tex = title.title()
        image_file = title.replace(" ", "_") + ".png"
        
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
    
        # Example placeholder property if not present
        if "charges" not in props:
            lines.append("Charges: ?")

        properties_block = "\n    ".join(lines)

        latex = f"""\\noindent\\begin{{tikzpicture}}
        \\node[anchor=north west, draw=none, text width=\\columnwidth, inner sep=0] (origin) at (0,0) {{\\vspace{{6pt}}}};
        \\draw[very thick] (origin.west) -- (origin.east);
        \\node[anchor=north west, inner sep=0] at (origin.south west) {{\\includegraphics[width=.33\\columnwidth]{{{image_file}}}}};
        \\node[anchor=north east, inner sep=0, text width=0.65\\columnwidth] at (origin.south east) {{\\textbf{{{title_tex}}}
        {properties_block}}};
        \\end{{tikzpicture}}"""

        return latex
