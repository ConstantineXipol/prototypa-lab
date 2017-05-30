from __future__ import print_function
import sys
from PIL import Image #python image library
import numpy as np #numpy: επιστημονικά εργαλεία
from numpy import pi, r_
from scipy import optimize
import matplotlib.pyplot as plt #για να δείχνουμε εικόνες/γραφήματα
import csv
import glob, os

# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017 (3 βαθμοί bonus)

counter = 0 # μετράει πλήθος απο εικόνες
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
    counter = counter +1
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
    shadowcount = (shadowcount//10000) * 10000 #πχ. 34501 πίξελ // 10000 = 3, 3 επί 10000 = 30,000
    pixeldata.append(shadowcount)
    print(shadowcount)
    if shadowcount > t_Threshold: firstresults.append(1) #αν έχει πολλά σκούρα σημεία, παίρνει μονάδα "1", δηλαδή είναι χαλασμένη
    else: firstresults.append(0) #αν δεν έχει πολλά σκούρα σημεία, παίρνει "0", δηλαδή δεν έχει πρόβλημα

os.chdir("..") #πήγαινε πίσω στον αρχικό φάκελο για να γράψεις τα αποτελέσματα

try:
    with open('result_data.csv', 'w') as file:
        for i in range(1, counter):
            s = "{},{}\n".format(pixeldata[i], firstresults[i])
            file.write(s)
except OSError:
    print("Πρόβλημα στο γράψιμο του αρχείου αναφοράς csv.. ίσως δεν έχεις δικαιώματα να γράψεις στον φάκελο?")
    sys.exit
'''
Tx = pixeldata

#Fitting
fitfunc = lambda p, x: p[0]*np.cos(2*np.pi/p[1]*x+p[2]) + p[3]*x # Target function
errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
p0 = [-15., 0.8, 0., -1.] # Initial guess for the parameters
p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, tX))

time = np.linspace(Tx.min(), Tx.max(), 100)
plt.plot(Tx, tX, "ro", time, fitfunc(p1, time), "r-") # Plot of the data and the fit



# Legend the plot
plt.title("Oscillations in the compressed trap")
plt.xlabel("time [ms]")
plt.ylabel("displacement [um]")
plt.legend(('x position', 'x fit'))

ax = plt.axes()

plt.text(0.8, 0.07,
         'x freq :  %.3f kHz \n y freq :  %.3f kHz' % (1/p1[1],1/p2[1]),
         fontsize=16,
         horizontalalignment='center',
         verticalalignment='center',
         transform=ax.transAxes)

plt.show() #εμφάνισε το γράφημα στην οθόνη
'''
print(firstresults)
