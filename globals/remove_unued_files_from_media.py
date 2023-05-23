# import os
# from myapp.models import Product
#
# media_path = '/path/to/media/directory/'
#
# # Get the filenames of the images in the media directory
# media_files = os.listdir(media_path)
#
# # Get the filenames of the images in the database
# db_files = [p.image.name for p in Product.objects.all()]
#
# # Find the filenames that are in the media directory but not in the database
# unused_files = set(media_files) - set(db_files)
#
# for filename in unused_files:
#     os.remove(os.path.join(media_path, filename))