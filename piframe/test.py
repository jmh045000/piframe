
import db_wrapper

db = db_wrapper.DbWrapper("piframe.db", "piframe.sql")

db.add_images(
    "/home/jhall2/pics/DSCN5223.JPG",
    "/home/jhall2/pics/DSCN5224.JPG",
    "/home/jhall2/pics/DSCN5225.JPG",
    "/home/jhall2/pics/DSCN5226.JPG",
    "/home/jhall2/pics/DSCN5227.JPG",
    "/home/jhall2/pics/DSCN5228.JPG",
    "/home/jhall2/pics/DSCN5229.JPG",
    "/home/jhall2/pics/DSCN5230.JPG",
    "/home/jhall2/pics/DSCN5231.JPG",
    "/home/jhall2/pics/DSCN5232.JPG",
    "/home/jhall2/pics/DSCN5233.JPG",
    "/home/jhall2/pics/DSCN5234.JPG",
    "/home/jhall2/pics/DSCN5235.JPG",
    "/home/jhall2/pics/DSCN5236.JPG",
)

print([str(i) for i in db.get_n_images_from_folder(20, -887619342744640549)])

db.clear_displayed_images()

print([str(i) for i in db.get_n_images_from_folder(20, -887619342744640549)])

# db.add_displayed_images((1, 2))
