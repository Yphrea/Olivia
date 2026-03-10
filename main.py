from spellCollection import spellCollection
from latexWrapper import *

myCollection = spellCollection.from_yaml("Olivia_spells.yaml")

for i, item in enumerate(myCollection.tomes):
    print(item.to_tikz())

OliviaTex = latexDocument('Olivia.tex')
OliviTex.add_content('\\section*{{Tomes}}\n')
OliviaTex.add_content(latexEnvironment('multicols', requires='2'))
OliviaTex.add_content(latexEnvironment)

