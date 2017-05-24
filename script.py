from PIL import Image #python image library
import numpy as np #numpy: scientific tools for python
import matplotlib.pyplot as plt #plotting library for showing images

# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017


Threshold = 50 #δυαδικό κατόφλι, οτιδήποτε κάτω απο αυτό γίνεται 0 (μάυρο)

im = Image.open("./kales/1.jpg") #φορτώνει φωτογραφίες σε object "Image"
im = im.convert("L") #αλλάζουμε την εικόνα σε greyscale

imgData = np.asarray(im) #η 'as_array' της numpy επιστρέφει την εικόνα που διάβασε η PIL σαν πίνακα (μονοδιάστατος γιατί είναι greyscale)
binaryimage = (imgData > Threshold) * 1.0

plt.imshow(binaryimage)
plt.show()#δείξε την εικόνα που φορτώθηκε σε παράθηρο
