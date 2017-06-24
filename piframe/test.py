
import db_wrapper
db = db_wrapper.DbWrapper('piframe.db', 'piframe.sql')

db.add_image('/home/jhall2/pics/DSCN5223.JPG')
db.add_image('/home/jhall2/pics/DSCN5224.JPG')
db.add_image('/home/jhall2/pics/DSCN5225.JPG')
db.add_image('/home/jhall2/pics/DSCN5226.JPG')
db.add_image('/home/jhall2/pics/DSCN5227.JPG')
db.add_image('/home/jhall2/pics/DSCN5228.JPG')
db.add_image('/home/jhall2/pics/DSCN5229.JPG')
db.add_image('/home/jhall2/pics/DSCN5230.JPG')
db.add_image('/home/jhall2/pics/DSCN5231.JPG')
db.add_image('/home/jhall2/pics/DSCN5232.JPG')
db.add_image('/home/jhall2/pics/DSCN5233.JPG')
db.add_image('/home/jhall2/pics/DSCN5234.JPG')
db.add_image('/home/jhall2/pics/DSCN5235.JPG')
db.add_image('/home/jhall2/pics/DSCN5236.JPG')

print [ str(i) for i in db.get_n_images_from_folder(5, -887619342744640549)]

#db.add_displayed_images((1, 2))
