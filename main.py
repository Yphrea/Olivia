#from spellCollection import spellCollection, imbuementLevels

from spellLibrary import spellLibrary, masterLibrary, spellCollection
from latexWrapper import *

imbuementLevels = ['dim', 'flickering', 'shining']

Libraries = []
LibraryPaths = ["library/imbuements_and_heals.yaml", "library/other.yaml"]
for path in LibraryPaths:
    Libraries.append(masterLibrary.from_yaml(path))
    
completeLibrary = masterLibrary.joinLibraries(Libraries)
OliviaCollection = spellCollection.from_yaml("Olivia_spells.yaml")
OliviaCollection.populate_spells(completeLibrary)
OliviaCollection.print()

myCollection = OliviaCollection

OliviaTex = latexDocument('Olivia.tex')

subsections = ['Heal', 'Mend', 'Imbuements', 'Other']
#Tomes section
OliviaTex.addContent("""\\section*{Tomes}\n
\\scriptsize\n""")
tomeMulticol = latexEnvironment('multicols*', required='3')
OliviaTex.addContent(tomeMulticol, setParent=True)
for subsection in subsections:
    subsectionSpells = myCollection.get('tome', subsection)
    if 'imbuement' in subsection.lower():
        types = [imbuement.title.split()[1] for imbuement in subsectionSpells]
        subsectionSpells.sort(key = lambda x:imbuementLevels.index(x.title.split()[0]))
        subsectionSpells.sort(key = lambda x:types.index(x.title.split()[1]))
    elif 'other' in subsection.lower():
        subsectionSpells = myCollection.get('tome', 'remaining')
    for i, spell in enumerate(subsectionSpells):
        tikz = latexEnvironment('tikzpicture')
        tikz.addContent(spell.toTikz())
        tomeMulticol.addContent(tikz, setParent=True)
OliviaTex.addContent("\\normalfont\n")

#OliviaTex.compile()
#exit()

#Spellpages section
OliviaTex.addContent("""\\section*{Spellpages}\n
\\scriptsize\n""")
tomeMulticol = latexEnvironment('multicols*', required='3')
OliviaTex.addContent(tomeMulticol, setParent=True)
for subsection in subsections:
    subsectionSpells = myCollection.get('spellpage', subsection)
    print("hej")
    for s, spell in enumerate(subsectionSpells):
        try:
            spell.difficulty
        except AttributeError:
            subsectionSpells[s].difficulty = -1
        print(spell.title, spell.difficulty)
    subsectionSpells.sort(key = lambda x: x.difficulty)
    if 'imbuement' in subsection.lower():

        print("hej")
        for spell in subsectionSpells:
            print(spell.title, spell.difficulty)
        types = [imbuement.title.split()[1].lower() for imbuement in subsectionSpells]
        subsectionSpells.sort(key = lambda x:imbuementLevels.index(x.title.split()[0].lower()))
        subsectionSpells.sort(key = lambda x:types.index(x.title.split()[1].lower()))
        print("hej")
        for spell in subsectionSpells:
            print(spell.title, spell.difficulty)
        #exit()
    elif 'other' in subsection.lower():
        subsectionSpells = myCollection.get('spellpage', 'remaining')
    for i, item in enumerate(subsectionSpells):
        tikz = latexEnvironment('tikzpicture')
        tikz.addContent(item.toTikz())
        tomeMulticol.addContent(tikz, setParent=True)
        
OliviaTex.addContent("\\normalfont\n")


#compilation
OliviaTex.compile()


