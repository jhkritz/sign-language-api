# Note: these curl commands are output from Postman, I did not write them myself.

echo curl --location --request GET 'http://127.0.0.1:5000/library/image?library_name=asl_alphabet_train&image_name=A1234.jpg'
echo

curl --location --request GET 'http://127.0.0.1:5000/library/image?library_name=asl_alphabet_train&image_name=A1234.jpg'

printf "\n---------------------------------------------------------------------------------------\n"

echo curl --location --request GET 'http://127.0.0.1:5000/library/signs?library_name=asl_alphabet_train'
echo

curl --location --request GET 'http://127.0.0.1:5000/library/signs?library_name=asl_alphabet_train'

printf "\n---------------------------------------------------------------------------------------\n"

echo curl --location --request GET 'http://127.0.0.1:5000/libraries/names'
echo

curl --location --request GET 'http://127.0.0.1:5000/libraries/names'

printf "\n---------------------------------------------------------------------------------------\n"

echo curl --location --request PUT 'http://127.0.0.1:5000/library/classify/image' \
--form 'library_name="asl_alphabet_train"' \
--form 'image=@"/home/river/Pictures/wallhaven-dpqjwj.jpg"'
echo

# You'll probably need to change the image path below to one that matches an image you have on your computer.

curl --location --request PUT 'http://127.0.0.1:5000/library/classify/image' \
--form 'library_name="asl_alphabet_train"' \
--form 'image=@"/home/river/Pictures/wallhaven-dpqjwj.jpg"'

printf "\n---------------------------------------------------------------------------------------\n"
