from sbgnrender import renderSBGN

renderSBGN("Reaction_Species.xml", "machin.png", verbose=True)
renderSBGN("Reaction_Species.xml", "machin.svg", format="svg")
renderSBGN("Reaction_Species.xml", "machin2.png", bg="#f00")
# renderSBGN("Reaction_Species.xml", "machin3.png", bg="#f00", layout=True) // Layout is not working
# renderSBGN("Reaction_Species.xml", "machin2.svg", format="svg", bg="#f00") // Here something is wrong, all the image is red
