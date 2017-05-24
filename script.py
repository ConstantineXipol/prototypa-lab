from __future__ import print_function
from PIL import Image #python image library
import numpy as np #numpy: scientific tools for python
import matplotlib.pyplot as plt #plotting library for showing images

# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017

firstresults = []
shadowcount = 0
Threshold = 50 #δυαδικό κατόφλι, οτιδήποτε κάτω απο αυτό γίνεται 0 (μάυρο)

im = Image.open("./kales/1.jpg") #φορτώνει φωτογραφίες σε object "Image"
im = im.convert("L") #αλλάζουμε την εικόνα σε greyscale

imgData = np.asarray(im) #η 'as_array' της numpy επιστρέφει την εικόνα που διάβασε η PIL σαν πίνακα (μονοδιάστατος γιατί είναι greyscale)
binaryimage = (imgData > Threshold) * 1 #λογική πράξη Χ 1 δίνει την αναπαράστασή της σαν νούμερο.

plt.imshow(binaryimage)
plt.show()#δείξε την εικόνα που φορτώθηκε σε παράθηρο

for row in binaryimage:
    for item in row:
        if item == 0:
            shadowcount = shadowcount +1

print(shadowcount)
if shadowcount > 50000: firstresults.append(1) #αν έχει πολλά σκούρα σημεία, παίρνει μονάδα "1", δηλαδή είναι χαλασμένη
else: firstresults.append(0) #αν δεν έχει πολλά σκούρα σημεία, παίρνει "0", δηλαδή δεν έχει πρόβλημα

print(firstresults[0])
