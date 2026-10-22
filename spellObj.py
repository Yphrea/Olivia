import yaml
from latexWrapper import latexEnvironment as texEnv
import os, re

class baseSpell():
    def __init__(self, **kwargs):
        self._spellSpecs = dict(kwargs)
        for key, item in self._spellSpecs.items():
            setattr(self, key, item)
        self.title = self.title.lower()

    def toTikzpicture(self):
        self.tp = texEnv('tikzpicture')
        self.tp.add_content(self.to_tikz())

    def spell_propertykeys(self):
        return [key for key in self.__dict__.keys() if key[0] != '_']
    
    def __repr__(self):
        spellstr = '------------------\n'
        for key, item in self.__dict__.items():
            if key[0] != '_':
                if isinstance(item, str) or isinstance(item, (int, float)):
                    spellstr += f"{key}: {item}\n"
                elif isinstance(item ,list):
                    spellstr += f"{key}:\n"
                    for val in item:
                        spellstr += f"  - {val}\n"
                elif item is None:
                    pass
                else:
                    raise TypeError(f"item {key}: {item} has a none recorgnized type {type(item)}")
        return spellstr
        

    def toTikz(self):
        props = self.spell_propertykeys()
        
        # Title handling
        title_tex = self.title.title()
        image_file = 'spell_thumbnails/'+self.title.replace(" ", "_").lower() + ".png"
        try:
            print(image_file)
            assert os.path.isfile(image_file)
        except AssertionError:
            image_file = "spell_thumbnails/make_tea.png"
        
        # Collect property lines (skip title)
        lines = []
        loopoverAttrs = [attr for attr in props if attr not in ['title', 'description', 'tags', 'spellType', 'section']]
        for add_at_end in ['description', 'tags']:
            if add_at_end in props:
                loopoverAttrs.append(add_at_end)
            
        for attr in loopoverAttrs:
            try:
                value = getattr(self, attr)
            except KeyError:
                continue
            
            # Convert lists nicely
            if isinstance(value, list):
                value = ", ".join(map(str, value))

            # Normalize key formatting; title() capitalizes first letter in word
            attr_tex = attr.replace("_", " ").title()
            lines.append(f"\\textbf{{{attr_tex}}}: {value}\\\\")

        #lines.append("Charges: ")

        properties_block = "\n    ".join(lines)

        latex = f"""\\node[anchor=north west, draw=none, text width=\\columnwidth, inner sep=0] (origin) at (0,0) {{\\vspace{{6pt}}}};
\\draw[very thick] (origin.west) -- (origin.east);
\\node[anchor=north west, inner sep=0] at (origin.south west) {{\\includegraphics[width=.28\\columnwidth]{{{image_file}}}}};
\\node[anchor=north east, inner sep=0, text width=0.70\\columnwidth, align=justify] at (origin.south east) {{\\isCarriedCircle\\ \\textbf{{{title_tex}}}\n
{properties_block}}};\n"""

        return latex


class templateSpell(baseSpell):
    def fill_properties(self, spell):
        element = self.title.split()[1] if 'imbuement' in self.title else '_'
        for property in spell.spell_propertykeys():
            if property == 'title': #the titles ought to have the same title already
                continue
            try:
                setattr(self, property, getattr(spell, property).replace('_', element))
            except AttributeError:
                setattr(self, property, getattr(spell, property))

class spellPage(templateSpell):
    pass

class tome(templateSpell):
    pass
