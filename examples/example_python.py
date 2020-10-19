from sbgnrender import renderSBGN

renderSBGN("Reaction_Species.xml", "network.png")
renderSBGN("Reaction_Species.xml", "network.svg", format="svg")
renderSBGN("Reaction_Species.xml", "network_white_bg.png", bg="#fff")
