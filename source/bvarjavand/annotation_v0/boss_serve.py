import pickle
import scipy.misc
from PIL import Image

#TODO: eventually will get mongodb to keep track of what slice

def get_bookmark(bookmark_file):
    bookmark = pickle.load(open(bookmark_file, "rb"))
    return bookmark

def save_bookmark(bookmark, bookmark_file):
    pickle.dump(bookmark, open(bookmark_file, "wb"))

def load_slice(filename, bookmark_file): #expects pickle file
    try:
        data = pickle.load(open(filename, "rb"))
        bookmark = get_bookmark(bookmark_file)

        metadata = data["metadata"]
        cube = data["data"]
        serve = cube[bookmark]
        img_name = str(bookmark) + "_" + metadata["id"] + ".png"

        im = Image.fromarray(serve)
        im.save(img_name, "PNG")
        bookmark += 1
        save_bookmark(bookmark, bookmark_file)
    except:
        raise("oops forgot to load file prob")

def test_load():
    save_bookmark(0, "bookmark.pickle")
    load_slice("01_00_00.pickle", "bookmark.pickle")


if __name__ == '__main__':
    test_load()
