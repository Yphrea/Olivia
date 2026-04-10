from spellCollection import spellCollection
from latexWrapper import *

myCollection = spellCollection.from_yaml("Olivia_spells.yaml")

#for i, item in enumerate(myCollection.tomes):
#    print(item.to_tikz())

OliviaTex = latexDocument('Olivia.tex')

#Tomes section
OliviaTex.addContent("""\\section*{Tomes}\n
\\scriptsize\n""")
tomeMulticol = latexEnvironment('multicols*', required='3')
OliviaTex.addContent(tomeMulticol, setParent=True)
for i, item in enumerate(myCollection.tomes):
    tikz = latexEnvironment('tikzpicture')
    tikz.addContent(item.toTikz())
    tomeMulticol.addContent(tikz, setParent=True)

OliviaTex.addContent("\\normalfont\n")

#Spellpages section
OliviaTex.addContent("""\\section*{spellpages}\n
\\scriptsize\n""")
tomeMulticol = latexEnvironment('multicols*', required='3')
OliviaTex.addContent(tomeMulticol, setParent=True)
for i, item in enumerate(myCollection.spellpages):
    tikz = latexEnvironment('tikzpicture')
    tikz.addContent(item.toTikz())
    tomeMulticol.addContent(tikz, setParent=True)

OliviaTex.addContent("\\normalfont\n")


#compilation
OliviaTex.compile()


