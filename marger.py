from PIL import Image

def merge_images_horizontally(imgs):
    '''
    This function merges images horizontally.
    '''
    imgs = [Image.open(i) for i in imgs]
    #create two lists - one for heights and one for widths
    widths, heights = zip(*(i.size for i in imgs))
    width_of_new_image = sum(widths)
    height_of_new_image = min(heights) #take minimum height
    # create new image
    new_im = Image.new('RGB', (width_of_new_image, height_of_new_image))
    new_pos = 0
    for im in imgs:
        new_im.paste(im, (new_pos,0))
        new_pos += im.size[0] #position for the next image
    filename = 'final.jpg'
    new_im.save(filename) #change the filename if you want
    return filename