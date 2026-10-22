from spellCollection import spellCollection, imbuementLevels
from latexWrapper import *

myCollection = spellCollection.from_yaml("spellbook.yaml")
OliviaCollection = spellCollection.from_yaml("Olivia_spells.yaml")

#for sType in spellCollection.spellTypes:
#    spells = getattr(OliviaCollection, sType)

#    for i, spell in enumerate(spells):
#        spells[i] = myCollection.findInCollection(
#            title=spell.spellSpecs['title']
#        )

#    print(f"{sType}: {getattr(OliviaCollection, sType)}")

#print("After loop:")
#print("tomes:", OliviaCollection.tomes)
#print("spellpages:", OliviaCollection.spellpages)
#exit()

for key,spells in OliviaCollection.spellSpecs.items():
    print(key)
    for spell in spells:
        print('\t', spell)

for sType in spellCollection.spellTypes:
    spells = getattr(OliviaCollection, sType)
    for i, spell in enumerate(spells):
        fullspell = myCollection.findInCollection(title=spell.spellSpecs['title'])
        if fullspell:
            spells[i] = fullspell

    setattr(OliviaCollection, sType, spells)
    OliviaCollection.spellSpecs[sType] = spells
for key,spells in OliviaCollection.spellSpecs.items():
    print(key)
    for spell in spells:
        print('\t', spell)

myCollection = OliviaCollection
#for entry in myCollection.get('tomes'):
#    if type(entry.spellSpecs['difficulty']) == type('hej'):
#        try:
#            print(entry.spellSpecs['title'], entry.spellSpecs['description'])
#        except:
#            print(entry.spellSpecs['title'])

#for i, item in enumerate(myCollection.tomes):
#    print(item.to_tikz())

OliviaTex = latexDocument('Olivia.tex')

subsections = ['Heal', 'Mend', 'Imbuements', 'Other']
#Tomes section
OliviaTex.addContent("""\\section*{Tomes}\n
\\scriptsize\n""")
tomeMulticol = latexEnvironment('multicols*', required='3')
OliviaTex.addContent(tomeMulticol, setParent=True)
for subsection in subsections:
    #OliviaTex.addContent(f"""\\subsection*{{{subsection}}}\n
    #\\scriptsize\n""")
    subsectionSpells = myCollection.get('tomes', subsection)
    #subsectionSpells.sort(key = lambda x: x.spellSpecs['difficulty'])
    print(subsectionSpells)
    if 'imbuement' in subsection.lower():
        types = [imbuement.spellSpecs['title'].split()[1].lower() for imbuement in subsectionSpells]
        subsectionSpells.sort(key = lambda x:imbuementLevels.index(x.spellSpecs['title'].split()[0].lower()))
        subsectionSpells.sort(key = lambda x:types.index(x.spellSpecs['title'].split()[1].lower()))
    elif 'other' in subsection.lower():
        subsectionSpells = myCollection.get('tomes', 'remaining')
    for i, item in enumerate(subsectionSpells):
        tikz = latexEnvironment('tikzpicture')
        tikz.addContent(item.toTikz())
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
    subsectionSpells = myCollection.get('spellpages', subsection)
    print("hej")
    for s, spell in enumerate(subsectionSpells):
        try:
            spell.spellSpecs['difficulty']
        except KeyError:
            subsectionSpells[s].spellSpecs['difficulty'] = -1
        print(spell.spellSpecs['title'], spell.spellSpecs['difficulty'])
    subsectionSpells.sort(key = lambda x: x.spellSpecs['difficulty'])
    if 'imbuement' in subsection.lower():

        print("hej")
        for spell in subsectionSpells:
            print(spell.spellSpecs['title'], spell.spellSpecs['difficulty'])
        types = [imbuement.spellSpecs['title'].split()[1].lower() for imbuement in subsectionSpells]
        subsectionSpells.sort(key = lambda x:imbuementLevels.index(x.spellSpecs['title'].split()[0].lower()))
        subsectionSpells.sort(key = lambda x:types.index(x.spellSpecs['title'].split()[1].lower()))
        print("hej")
        for spell in subsectionSpells:
            print(spell.spellSpecs['title'], spell.spellSpecs['difficulty'])
        #exit()
    elif 'other' in subsection.lower():
        subsectionSpells = myCollection.get('spellpages', 'remaining')
    for i, item in enumerate(subsectionSpells):
        tikz = latexEnvironment('tikzpicture')
        tikz.addContent(item.toTikz())
        tomeMulticol.addContent(tikz, setParent=True)
        
OliviaTex.addContent("\\normalfont\n")


#compilation
OliviaTex.compile()


