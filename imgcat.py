import glob, os, sys
from PIL import Image, ImageDraw
from resizeimage import resizeimage

path = 'orig'
newpath = 'new'
maxHeight = 200
cornerRadius = 10
seperator = 2

def add_corners(im, rad):
 circle = Image.new('L', (rad * 2, rad * 2), 0)
 draw = ImageDraw.Draw(circle)
 draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
 alpha = Image.new('L', im.size, 255)
 w, h = im.size
 alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
 alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
 alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
 alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
 im.putalpha(alpha)
 return im

# Resize images
inputFiles = list()
for filename in glob.glob(os.path.join(path, '*.jpg')):
 inputFiles.append(filename)

for inputFile in inputFiles:
 original = open(inputFile, 'r')
 origImg = Image.open(original)
 origImg = resizeimage.resize_height(origImg, maxHeight)
 origImg.save(newpath + "/" + str(maxHeight) + "_" + os.path.basename(inputFile), origImg.format, subsampling=0, quality=100)
 original.close()


# Join images
resizedFiles = list()
for filename in glob.glob(os.path.join(newpath, '*.jpg')):
 resizedFiles.append(filename)

images = map(Image.open, resizedFiles)
widths, heights = zip(*(i.size for i in images))
totalWidth = sum(widths) + len(widths) * seperator
new_im = Image.new('RGBA', (totalWidth, maxHeight),(255,0,0,0))

x_offset = 0
for im in images:
  im = add_corners(im,cornerRadius)
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0] + seperator

new_im.save('output.png','PNG')

print str(totalWidth) + "px wide"
