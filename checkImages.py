from PIL import Image

jarrito = Image.open("jarritos.jpg")

img_added = Image.open("0001.jpg")
width = img_added.width
height = img_added.height

print(width,height)


jarrito = jarrito.resize((width,height))
jarrito.save('jarritos_saved.png',"PNG")
print(jarrito.size)

jarrito = Image.open("jarritos_saved.png")

img_added.paste(jarrito, (0, 0), jarrito)
img_added.save('test.png',"PNG")