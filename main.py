import formatLatex as spell

myCollection = spell.spellCollection.from_yaml("flickering_wood_imbuement.yaml")

for i, item in enumerate(myCollection.tomes):
    print(item.to_tikz())

