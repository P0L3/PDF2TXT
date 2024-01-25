# from pikepdf import Pdf, PdfImage, Name

# # define a function that takes the page number as argument 
# def remove_image(page) :
#     image_name, image = next(iter(page.images.items()))
#     new_image = example.make_stream(b'\xff')
#     new_image.Width, new_image.Height = 1, 1
#     new_image.BitsPerComponent = 1
#     new_image.ImageMask = True
#     new_image.Decode = [0, 1]
#     page.Resources.XObject[image_name] = new_image

# # open your pdf, src.pdf here 
# example = Pdf.open('pdf_with_svg_image-1.pdf')

# # iterate through each page.
# for page in example.pages :
#     remove_image(page)

# # finally save your pdf     
# example.save('pdf_with_svg_imageless-1.pdf')


from pikepdf import Pdf, PdfImage, Name

# define a function that takes the page number as an argument 
def remove_image(page):
    image_name, image = next(iter(page.images.items()))
    new_image = page.make_stream(b'\xff')  # Use page.make_stream instead of example.make_stream
    new_image.Width, new_image.Height = 1, 1
    new_image.BitsPerComponent = 1
    new_image.ImageMask = True
    new_image.Decode = [0, 1]
    page.Resources.XObject[image_name] = new_image

# open your pdf, src.pdf here 
example = Pdf.open('pdf_with_svg_image-1.pdf')

# iterate through each page.
for page in example.pages:
    remove_image(page)

# finally, save your pdf     
example.save('pdf_with_svg_imageless-1.pdf')
