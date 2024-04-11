from globals import repos

image_file_types = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'svg', 'ico', 'webp', 'heic', 'heif', 'bpg', 'avif', 'flif']

for repo in repos:
    # Remove all images from each repo
    for file_type in image_file_types:
        for path in repo.rglob(f'*.{file_type}'):
            path.unlink()
            print(f'Deleted image at location {path}')