from api.RendererClient import RendererClient

client = RendererClient("localhost", 8081)
client.render("https://navicell.vincent-noel.fr/maps/ce4d6b63-d957-4b42-a865-21c2f421940e/sbgnml.xml", "machin.png")
client.render("https://navicell.vincent-noel.fr/maps/6b63-d957-4b42-a865-21c2f421940e/sbgnml.xml", "chose.png")
client.render("https://navicell.vincent-noel.fr/maps/ce4d6b63-d957-4b42-a865-21c2f421940e/sbgnml.png", "chose.png")
client.close()

client2 = RendererClient("not_localhost", 8081)
client2.close()
