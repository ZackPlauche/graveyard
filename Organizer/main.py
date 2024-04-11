from config.organizer import Organizer

o = Organizer('E:/')

o.clean_folders()
o.move_files('Photos', ('.png', '.jpg', '.jpeg'))
print('Photos organized!')
o.move_files('GIFs', ('.gif',))
print('Gifs organized!')
o.move_files('Videos', ('.mp4', '.mov'))
print('Videos organized!')
o.remove_files(('.HEIC', '.json'))
o.clean_folders()