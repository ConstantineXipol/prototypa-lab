from __future__ import print_function
import sys
from PIL import Image #python image library
import numpy as np #numpy: επιστημονικά εργαλεία
import matplotlib.pyplot as plt #για να δείχνουμε εικόνες/γραφήματα
import csv
import glob, os

# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017 (3 βαθμοί bonus)


pixeldata = []
firstresults = []
Threshold = int(sys.argv[1]) #δυαδικό κατόφλι, οτιδήποτε κάτω απο αυτό γίνεται 0 (μάυρο), είναι το πρώτο argument στην κάλεση του προγράμματος
t_Threshold = int(sys.argv[2]) #το συνολικό κατόφλι εικόνας για την κατάταξή της σε φωτεινή η σκοτεινή, είναι το δεύτερο argument
if Threshold < 0 or Threshold > 255 or t_Threshold < 0 or t_Threshold > 250000:
    print("Λάθος κατόφλι/α, reminder: 0-255 για το πρώτο argument, 0-250.000 για το δεύτερο..")
    sys.exit

folders = input("Δώσε το όνομα του φακέλου που περιέχει τις εικόνες, πρέπει να είναι στο working dir, και να περιέχει εικόνες .jpg\n")
while True:
    try:
        os.chdir(folders) #μπές μέσα στον φάκελο που δώθηκε
        break
    except OSError:
        print("Λάθος όνομα φακέλου, let's try that again..")
        folders = input()
for file in glob.glob("*.jpg"):
    shadowcount = 0
    try:
        im = Image.open(file) #φορτώνει φωτογραφίες σε object "Image"
    except IOError:
        print("Σφάλμα στο άνοιγμα εικόνας.. τσέκαρε τα extensions των εικόνων")
    im = im.convert("L") #αλλάζουμε την εικόνα σε greyscale
    #im = im.transform((1000,1000), "PIL.im.Extent", None, 0, 1) #ΓΑΜΩ ΤΙΣ ΜΑΛΑΚΙΕΣ ΣΑΣ ΣΚΑΤΟ PILLOW -- αλλαγή μεγέθους εικόνας, πρώτα είναι ένα tuple μεγέθους, μετά το cropping.

    imgData = np.asarray(im) #η 'as_array' της numpy επιστρέφει την εικόνα που διάβασε η PIL σαν πίνακα (μονοδιάστατος γιατί είναι greyscale)
    binaryimage = (imgData > Threshold) * 1 #λογική πράξη Χ 1 δίνει την αναπαράστασή της σαν νούμερο.

    #plt.imshow(binaryimage)
    #plt.show() #δείξε την εικόνα που φορτώθηκε σε παράθηρο

    for row in binaryimage:
        for item in row:
            if item == 0:
                shadowcount = shadowcount +1
    pixeldata.append(shadowcount)
    print(shadowcount)
    if shadowcount > t_Threshold: firstresults.append(1) #αν έχει πολλά σκούρα σημεία, παίρνει μονάδα "1", δηλαδή είναι χαλασμένη
    else: firstresults.append(0) #αν δεν έχει πολλά σκούρα σημεία, παίρνει "0", δηλαδή δεν έχει πρόβλημα

os.chdir("..") #πήγαινε πίσω στον αρχικό φάκελο για να γράψεις τα αποτελέσματα

try:
    with open('result_data.csv', 'w') as file:
        for es in range(1, 21):
            s = "{},{},{}\n".format(es, pixeldata[es-1], firstresults[es-1])
            file.write(s)
except OSError:
    print("Πρόβλημα στο γράψιμο του αρχείου αναφοράς csv.. ίσως δεν έχεις δικαιώματα να γράψεις στον φάκελο?")
    sys.exit
    
print(firstresults)
