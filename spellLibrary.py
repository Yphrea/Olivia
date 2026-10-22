import yaml
from latexWrapper import latexEnvironment as texEnv
from spellObj import baseSpell, tome, spellPage
import os

class spellLibrary():

    def __init__(self, check_duplicates = False, **kwargs):
        self._libraryContent = dict(kwargs)
        self._librarySpellDicts = []
        for section in self._libraryContent.keys():
            for i, spell in enumerate(self._libraryContent[section]):
                self._libraryContent[section][i]['section'] = section
                self._librarySpellDicts.append(self._libraryContent[section][i])
                
        if check_duplicates:
            self.check_duplicates()
            
        self.librarySpells = []
        for spellDict in self._librarySpellDicts:
            self.librarySpells.append(baseSpell(**spellDict))
                
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

    def print(self):
        for spell in self._librarySpellDicts:
            print(spell)

class masterLibrary(spellLibrary):
    def __init__(self, **kwargs):
        spellLibrary.__init__(self, check_duplicates = True, **kwargs)


class spellCollection(spellLibrary):
    def __init__(self, **kwargs):
        spellLibrary.__init__(self, check_duplicates = False, **kwargs)
