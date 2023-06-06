import PIL
import PIL.Image, PIL.ImageTk


im = PIL.Image.open('crop.jpg').convert('L')
im = im.crop((185, 33, 327, 94))
im.save('cated.jpg')
