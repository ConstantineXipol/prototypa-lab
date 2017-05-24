from __future__ import print_function
from PIL import Image #python image library
import numpy as np #numpy: scientific tools for python
import matplotlib.pyplot as plt #plotting library for showing images

# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017

firstresults = []
Threshold = 70 #δυαδικό κατόφλι, οτιδήποτε κάτω απο αυτό γίνεται 0 (μάυρο)
folders = input("Δώσε το όνομα του φακέλου που περιέχει τις εικόνες, πρέπει να είναι στο working dir, και να περιέχει εικόνες με το φορμάτ <***>.jpg, όπου * αριθμός..")
for i in range(1, 21):
    shadowcount = 0
    im = Image.open("./{}/{}.jpg".format(folders, i)) #φορτώνει φωτογραφίες σε object "Image"
    im = im.convert("L") #αλλάζουμε την εικόνα σε greyscale
    #im = im.transform((1000,1000), "PIL.im.Extent", None, 0, 1) #ΓΑΜΩ ΤΙΣ ΜΑΛΑΚΙΕΣ ΣΑΣ ΣΚΑΤΟ PILLOW -- αλλαγή μεγέθους εικόνας, πρώτα είναι ένα tuple μεγέθους, μετά το cropping.

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


print(firstresults)
