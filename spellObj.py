import yaml
from latexWrapper import latexEnvironment as texEnv
import os

class baseSpell():
    def __init__(self, **kwargs):
        self._spellSpecs = dict(kwargs)
        for key, item in self._spellSpecs.items():
            setattr(self, key, item)
        self.title = self.title.lower()

    def toTikzpicture(self):
        self.tp = texEnv('tikzpicture')
        self.tp.add_content(self.to_tikz())

    def __repr__(self):
        return f"{self.__class__.__name__}({self._spellSpecs})"

    def toTikz(self):
        props = self._spellSpecs#= getattr(self, "_spellSpecs", {})
        
        # Title handling
        title = str(props.get("title", "Unknown"))
        title_tex = title.title()
        image_file = 'spell_thumbnails/'+title.replace(" ", "_").lower() + ".png"
        try:
            print(image_file)
            assert os.path.isfile(image_file)
        except AssertionError:
            image_file = "spell_thumbnails/make_tea.png"
        
        # Collect property lines (skip title)
        lines = []
        loopoverKeys = [key for key in list(props.keys()) if key not in ['title', 'description', 'tags']]+['description', 'tags']
        for key in loopoverKeys:
            try:
                value = props[key]
            except KeyError:
                continue
            
            # Convert lists nicely
            if isinstance(value, list): #why?
                value = ", ".join(map(str, value))

            # Normalize key formatting; title() capitalizes first letter in word
            key_tex = key.replace("_", " ").title()
            lines.append(f"\\textbf{{{key_tex}}}: {value}\\\\")

        #lines.append("Charges: ")

        properties_block = "\n    ".join(lines)

        latex = f"""\\node[anchor=north west, draw=none, text width=\\columnwidth, inner sep=0] (origin) at (0,0) {{\\vspace{{6pt}}}};
\\draw[very thick] (origin.west) -- (origin.east);
\\node[anchor=north west, inner sep=0] at (origin.south west) {{\\includegraphics[width=.28\\columnwidth]{{{image_file}}}}};
\\node[anchor=north east, inner sep=0, text width=0.70\\columnwidth] at (origin.south east) {{\\isCarriedCircle\\ \\textbf{{{title_tex}}}\n
{properties_block}}};\n"""

        return latex

    
class spellPage(baseSpell):
    pass


class tome(baseSpell):
    pass
