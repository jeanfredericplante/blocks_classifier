echo "creating directories"
mkdir processed
mkdir processed/one
mkdir processed/ten

# cp images and remove metadata
echo "copying tens"
cp ten/*.JPG processed/ten/.
echo "copying ones"
cp one/*.JPG processed/one/.


#
cd processed
echo "removing metadata"

for i in one/*.JPG; do echo "Processing $i"; exiftool -all= "$i"; done
for i in ten/*.JPG; do echo "Processing $i"; exiftool -all= "$i"; done

# resize images
echo "resizing images"
sips -Z 640 ten/*.JPG
sips -Z 640 one/*.JPG
