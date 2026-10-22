import yaml
from latexWrapper import latexEnvironment as texEnv
from spellObj import baseSpell, tome, spellPage, templateSpell
import os

class spellLibrary():

    def __init__(self, **kwargs):
        self._libraryContent = dict(kwargs)
        self._librarySpellDicts = []
                
    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def joinLibraries(cls, libraries):
        jointLibraryContent = {}
        for library in libraries:
            jointLibraryContent = {**jointLibraryContent, **library._libraryContent}
        return cls(**jointLibraryContent)

    def check_duplicates(self):
        titles = [spell['title'].lower() for spell in self._librarySpellDicts]
        duplicatedTitles = titles
        for title in set(titles):
            duplicatedTitles.remove(title)
        assert len(duplicatedTitles) == 0, "There are duplicated spells in your library."
    
    def __iter__(self):
        return iter(self.librarySpells)

    def __repr__(self):
        spellstr = ""
        for spell in self._librarySpellDicts:
            spellstr += str(spell)+'\n'
        return spellstr

    def print(self):
        for spell in self.librarySpells:
            print(spell)
    

class masterLibrary(spellLibrary):
    def __init__(self, **kwargs):
        spellLibrary.__init__(self, **kwargs)
        for section in self._libraryContent.keys():
            for i, spell in enumerate(self._libraryContent[section]):
                self._libraryContent[section][i]['section'] = section
                self._librarySpellDicts.append(self._libraryContent[section][i])
                
        self.check_duplicates()
            
        self.librarySpells = []
        for spellDict in self._librarySpellDicts:
            self.librarySpells.append(baseSpell(**spellDict))

    def find_spell(self, spell):
        if 'imbuement' in spell.title:
            aux_title = " ".join([spell.title.split()[0], "_", spell.title.split()[2]])
        else:
            aux_title = spell.title
        for libSpell in self.librarySpells:
            if libSpell.title == aux_title:
                return libSpell
        return None
    
class spellCollection(spellLibrary):
    def __init__(self, **kwargs):
        spellLibrary.__init__(self, **kwargs)
        for spellType in self._libraryContent.keys():
            for i, spell in enumerate(self._libraryContent[spellType]):
                self._libraryContent[spellType][i]['spellType'] = spellType
                self._librarySpellDicts.append(self._libraryContent[spellType][i])
            
        self.librarySpells = []
        for spellDict in self._librarySpellDicts:
            self.librarySpells.append(templateSpell(**spellDict))
        self.previouslyRequested = []

    def populate_spells(self, masterLib):
        for s, spell in enumerate(self.librarySpells):
            masterSpell = masterLib.find_spell(spell)
            if masterSpell:
                self.librarySpells[s].fill_properties(masterSpell)
                
    def get(self, spellType, *args):
        targetSpells = [spell for spell in self.librarySpells if spell.spellType == spellType]
        for spell in self.librarySpells:
            print(spell.spellType, spellType)
        print(targetSpells)
        aux = []
        for key in args:
            if key == 'remaining':
                for spell in targetSpells:
                    print(spell)
                    addSpell = True
                    for prevReq in self.previouslyRequested:
                        print('\t', prevReq)
                        if spell is prevReq:
                            addSpell = False
                            break
                    if addSpell:
                        aux.append(spell)
            else:
                key = key[0:-1] if key[-1] == 's' else key
                for spell in targetSpells:
                    try:
                        if key.lower() in getattr(spell, 'tags'):
                            aux.append(spell)
                    except (AttributeError, TypeError):
                        pass
                    if key.lower() in getattr(spell, 'title'):
                        aux.append(spell)
            targetSpells = [spell for spell in aux]
            aux = []
        self.previouslyRequested += targetSpells
        return targetSpells

