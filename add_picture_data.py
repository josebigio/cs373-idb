from app import db, models
import os


def main():
    staticimagespath = "/static/images/"
    curdir = "/home/elementalists/cs373-idb/app" + staticimagespath
    default = "default"
    for i in range(1, 119):
        firstImageInFolder = True
        e = models.Element.query.get(i)
        element_name = e.element.strip()
        element_dir_name = ''
        print("element: " + element_name)
        for filename in os.listdir(curdir):
            # print("checking : " + filename)
            if filename.lower().startswith(element_name.lower()):
                print("Found Dir: " + curdir+filename)
                element_dir_name = filename
        if element_dir_name != '':
            for imagefilename in os.listdir(curdir+element_dir_name):
                print("--- Examining: " + imagefilename)
                path = staticimagespath + imagefilename
                print(path)
                imageType = None
                if firstImageInFolder:
                    print("-- default --")
                    imageType = default
                    firstImageInFolder = False
                image = models.Image(image_path=path, element_number=i, image_type=imageType)
                db.session.add(image)
                db.session.commit()
        else:
            print("Could not find image folder for " + element_name)

if __name__ == "__main__":
    main()
