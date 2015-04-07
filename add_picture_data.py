from app import db, models
import os


def main():
    staticimagespath = "/static/images/"
    curdir = "/home/elementalists/cs373-idb/app" + staticimagespath
    default = "default"
    for i in range(1, 119):
        firstImageInFolder = True
        e = models.Element.query.get(i)
        element_name = e.element
        element_dir_name = ''
        for filename in os.listdir(curdir):
            if filename.lower().startswith(element_name.lower()):
                element_dir_name = filename
        if element_dir_name != '':
            for imagefilename in os.listdir(curdir+element_dir_name):
                path = staticimagespath + imagefilename
                imageType = None
                if firstImageInFolder:
                    imageType = default
                    firstImageInFolder = False
                picture = models.Pcitures(image_path=path, element_number=i, image_type=imageType)
                db.session.add(picture)
        else:
            print("Could not find image folder for " + element_name)
        db.session.commit()


if __name__ == "__main__":
    main()
