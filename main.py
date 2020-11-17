import sys, time, subprocess, argparse, logging
from os import remove, listdir, makedirs
from os.path import isfile, join, exists
from pdf2image import convert_from_path
from PIL import Image
from time import sleep


def flag():
    logging.info("fino a qui tutto bene")
    sleep(5)


# @author vladignatyev https://gist.github.com/vladignatyev/
# print a progress bar for Loading
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(description='Merge images in pdf')

    # INPUT ARGUMENT DEFINITION
    parser.add_argument('-i', '--image_source_folder', help='Source from which to take image')
    parser.add_argument('-p', '--pdf_source', help='Source from which to take .pdf files')
    parser.add_argument('-o', '--destination_folder', help='Destination where to save .pdf or images files')
    parser.add_argument('-d', '--delete_after_run', help='Choose if delete files after conversion [y/n], DEFAULT: n',
                        default="n")
    parser.add_argument('-r', '--reverse', help='Choose if split pdf in images [y/n], DEFAULT: n', default="n")

    args = parser.parse_args()

    # PARSING ARGS
    if args.destination_folder is None:
        logging.error("Missing arguments! You must write destination folder")
        sleep(5)
        sys.exit(2)

    imagesfolder = args.image_source_folder
    pdfsource = args.pdf_source
    outputfolder = args.destination_folder
    deletion = True if args.delete_after_run in ("y", "Y") else False

    # Destination folder. Create if does not exist
    if not exists(outputfolder):
        makedirs(outputfolder)

    if pdfsource is None and imagesfolder is None:
        logging.error("Error with source path! Invalid arguments")
        sleep(5)
        sys.exit("Invalid PDF path")

    if args.reverse in ("y", "Y"):
        pdf_to_png(pdfsource, outputfolder, deletion)
    else:
        png_to_pdf(imagesfolder, outputfolder, deletion)

    print("\nDONE!")
    subprocess.Popen('explorer ' + outputfolder.replace("/", "\\"))
    sleep(10)


def png_to_pdf(source, dest, delete):
    i = 0
    progress(i, 100, status="\nExtracting images from: " + source)

    # Extracting images that ends with ".png" or ".jpg" characters from input folder
    images = [source + "/" + image for image in listdir(source) if
              (isfile(join(source, image)) and ((".png" in image) or (".jpg" in image)))]

    # for each image finded in source folder
    # open and convert
    progress(50, 100, status='\nConverting images:')
    try:
        converted = list(map(lambda x: Image.open(x).convert('RGB'), images))
    except Exception as e:
        logging.error("Errore!! ", e)
        sleep(5)
        sys.exit(e)

    # saving the pdf
    progress(50, 100, status='\nSaving pdfs')
    try:
        converted[0].save(dest + "/file.pdf", save_all=True, append_images=converted[1:])
    except Exception as e:
        logging.error("Errore!! ", e)
        sleep(5)
        sys.exit(e)

    # deleting images from source folder
    if delete:
        for image in images:
            remove(image)


def pdf_to_png(source, dest, delete):
    progress(0, 100, status="\nExtracting pdf from: " + source)

    names = [pdf for pdf in listdir(source) if (isfile(join(source, pdf)) and ".pdf" in pdf)]
    pdfs = [source + "\\" + pdf for pdf in names]

    if len(pdfs) == 0:
        logging.warning("NO PDFS FOUND")
        return 0

    # Store Pdf with convert_from_path function
    groups_of_images = []
    try:
        for pdf in pdfs:
            groups_of_images.append(convert_from_path(pdf))
    except Exception as e:
        logging.error("Errore: ", e)
        sleep(5)

    progress(50, 100, status="\nSaving images...")
    if len(groups_of_images) != 0:
        jump = 50 / len(groups_of_images)

    i = 50
    # for each group of images
    for index, images in enumerate(groups_of_images):

        folder_path = dest+"\\"+names[index]
        # Destination folder. Create if does not exist
        if not exists(folder_path):
            makedirs(folder_path)

        # Progress bar
        i += jump
        progress(i, 100, status="\nSaving images...")

        # Save all the images in the group
        for n, image in enumerate(images):
            try:
                image.save(folder_path + "\\" + str(n) + '.png', 'PNG')
            except Exception as e:
                logging.error("Errore!! ", e)
                sleep(5)
                sys.exit(e)

    # deleting images from source folder
    if delete:
        for elem in listdir(source):
            remove(source+"\\"+elem)


if __name__ == "__main__":
    main()

