# png_to_pdf
Simply converter from png to pdf and vice versa.   
With this script you can choose if create a pdf using a set of images or to split a pdf in pages and save them as images.   
   
* The default way to run this script is merging images in one pdf, using _-i <source>_ and _-o <destination>_ arguments.    
* If you want to do che opposite process you must use _-p <source>_, _-o <destination>_, _-r y_  arguments.
   
_Source_ and _destination_ args are mandatory. You can also choose if delete the elements from source after the conversion.   

## Requirements 
To use this script you must install the following modules
```bash
pdf2image==1.14.0
Pillow==8.0.1
```
Also, to use pdf2image, you need to download poppler, and add _bin_ folder to PATH.
* poppler for windows: [https://github.com/oschwartz10612/poppler-windows/releases/](https://github.com/oschwartz10612/poppler-windows/releases/)
* poppler for linux:
```bash
pip install python-poppler
```

## Usage 
The script was built to being used from terminal/cmd.
If you want to build a pdf from images, a simple usage is the following:
```bash
main.py -i <source> -o <destination>
```
If you want to split a pdf in images, you have to use this syntax:
```bash
main.py -p <source> -o <destination> -r y
```

The options are:
```bash
-i, --image_source_folder  'Source from which to take image'
-p, --pdf_source           'Source from which to take .pdf files'
-o, --destination_folder   'Destination where to save .pdf or images files'
-d, --delete_after_run,    'Choose if delete files after conversion [y/n], DEFAULT: n'
-r, --reverse              'If yes, splits pdf in images, else vice versa [y/n], DEFAULT: "n"'
```

## License 
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)