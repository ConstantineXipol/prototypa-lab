from __future__ import print_function
import sys
from PIL import Image #python image library
import numpy as np #numpy: επιστημονικά εργαλεία
from numpy import pi, r_
from scipy import optimize
import matplotlib.pyplot as plt #για να δείχνουμε εικόνες/γραφήματα
import csv
import glob, os #parsing φακέλων
from statistics import mean
from matplotlib import style #διάφορα στύλ για τα plot του matplotlib

# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017 (10 βαθμοί bonus)

style.use('fivethirtyeight')
counter = 0 # μετράει πλήθος απο εικόνες
pixeldata = []
firstresults = []
freq = []
Threshold = int(sys.argv[1]) #δυαδικό κατόφλι, οτιδήποτε κάτω απο αυτό γίνεται 0 (μάυρο), είναι το πρώτο argument στην κάλεση του προγράμματος
#t_Threshold = int(sys.argv[2]) #το συνολικό κατόφλι εικόνας για την κατάταξή της σε φωτεινή η σκοτεινή, είναι το δεύτερο argument
if Threshold < 0 or Threshold > 255: # or t_Threshold < 0 or t_Threshold > 250000:
    print("Λάθος κατόφλι/α, reminder: 0-255 για το πρώτο argument")
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
    #if shadowcount > t_Threshold: firstresults.append(1) #αν έχει πολλά σκούρα σημεία, παίρνει μονάδα "1", δηλαδή είναι χαλασμένη
    #else: firstresults.append(0) #αν δεν έχει πολλά σκούρα σημεία, παίρνει "0", δηλαδή δεν έχει πρόβλημα

#βρίσκει την συχνότητα εμφάνισης για κάθε αριθμό μαύρων πίξελ.
for j in range(0, 26): # μέχρι 26 γιατί έχουμε αριθμό πίξελ 500χ500 = 250,000
    freq.append(0)
    for i in range(0, counter): #counter: πόσες εικόνες έχουμε
        if pixeldata[i] == int("{:2d}0000".format(j)): # αν αριθμός πίξελ == **,000 αύξησε την συχνότητα κατα +1
            freq[j] = freq[j] + 1

os.chdir("..") #πήγαινε πίσω στον αρχικό φάκελο για να γράψεις τα αποτελέσματα
data = []
try:
    with open('result_data.csv', 'w') as file: #άνοιγμα αρχείου σε write mode
        for i in range(0, 26):
            s = "{:2d}0000,{}\n".format(i, freq[i]) #τελικό output
            file.write(s)
            data.append(int("{:2d}0000".format(i))) #χτίζουμε μια λίστα με τους αριθμούς πίξελ.
except OSError:
    print("Πρόβλημα στο γράψιμο του αρχείου αναφοράς csv.. ίσως δεν έχεις δικαιώματα να γράψεις στον φάκελο?")
    sys.exit

#print(len(data)) #DEBUGGING
#print(len(freq))
x = np.array(data) #περνάμε τους αριθμούς και συχνότητες εμφάνισης σε numpy arrays
y = np.array(freq)

print(x)
print(y)

#regresion γραμμές
def best_fit(x, y):
    m = ( (mean(x) * mean(y)) - mean(x*y) )  /  (( mean(x) **2) - ( mean(x**2) )) #η εξίσωση regression γραμμής
    b = mean(y) - m*mean(x) #σημείο τομής γραμμής
    return m, b


m, b = best_fit(x, y)
regression_line = [ (m*xs)+b for xs in x ] 
print(m, b)

plt.scatter(x, y) #γράφημα scatterplot
plt.plot(x, regression_line)
plt.show() #εμφάνισε το γράφημα στην οθόνη
