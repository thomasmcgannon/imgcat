import glob, os, sys
from PIL import Image, ImageDraw
from resizeimage import resizeimage

path = 'orig'
newpath = 'new'
maxHeight = 200
cornerRadius = 10
seperator = 2
outputName = 'output'
outputFormat = 'png'
bgColour = (255,255,255)

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

def join_images(images, sep = 0, rad = 0):
 "Joins passed images with the passed seperating value in pixels and rounded cornrs"
 widths, heights = zip(*(i.size for i in images))
 totalWidth = sum(widths) + len(widths) * sep
 totalHeight = max(heights)
 # Prepare new blank image of the right size
 if outputFormat.lower() == 'png':
  new_im = Image.new('RGBA', (totalWidth, totalHeight), (255,0,0,0))
 elif outputFormat.lower() == 'jpg':
  new_im = Image.new('RGB', (totalWidth, totalHeight), bgColour)
 else:
  print "Unsupported file format"
  exit()

 x_offset = 0
 for im in images:
   im = add_corners(im,rad)
   new_im.paste(im, (x_offset,0))
   x_offset += im.size[0] + sep
 return new_im

# Resize images
inputFiles = list()
resizedImages = list()
for filename in glob.glob(os.path.join(path, '*.jpg')):
 inputFiles.append(filename)

for inputFile in inputFiles:
 original = open(inputFile, 'r')
 origImg = Image.open(original)
 resizedImage = resizeimage.resize_height(origImg, maxHeight)
 resizedImages.append(resizedImage)
 original.close()

# Join images
new_im = join_images(resizedImages, seperator, cornerRadius)

# Save new output file

if outputFormat.lower() == 'jpg':
 new_im.save(outputName + '.jpg','JPEG',subsampling=0,quality=100)
elif outputFormat.lower() == 'png':
 new_im.save(outputName + '.png','PNG',optimize=1)
else:
 print "Unsupported file format"


# Print the dimensions of the newly joined image
print 'x'.join(str(dim) for dim in new_im.size)
