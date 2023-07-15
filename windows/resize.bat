:: resize all photos drag-dropped onto this file under thumbnails folder
:: requires ImageMagick installed
for %%x in (%*) do magick convert -resize 600x800 %%x "%%~dx%%~pxthumbnails\%%~nx.jpg"
