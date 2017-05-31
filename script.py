from __future__ import print_function
import sys
from PIL import Image #python image library
import numpy as np #numpy: επιστημονικά εργαλεία
from numpy import pi, r_
from scipy import optimize
from scipy import asarray as ar,exp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt #για να δείχνουμε εικόνες/γραφήματα
from matplotlib import style #διάφορα στύλ για τα plot του matplotlib
import csv
import glob, os #parsing φακέλων
from statistics import mean


# Π2014116 Ξυπολιτόπουλος Κωνσταντίνος - Για την εργαστηριακή bonus εργασία 'Αναγνώρισης Προτύπων' 2016-2017 (15 βαθμοί bonus)


style.use('fivethirtyeight')
counter = 0 # μετράει πλήθος απο εικόνες
counter2 = 0
pixeldata = []
pixeldata2 = []
freq = []
freq2 = []
Threshold = int(sys.argv[1]) #δυαδικό κατόφλι, οτιδήποτε κάτω απο αυτό γίνεται 0 (μάυρο), είναι το πρώτο argument στην κάλεση του προγράμματος
#t_Threshold = int(sys.argv[2])
if Threshold < 0 or Threshold > 255: # or t_Threshold < 0 or t_Threshold > 250000:
    print("Λάθος κατόφλι/α, reminder: 0-255 για το πρώτο argument")
    sys.exit

folders = sys.argv[2] #το όνομα του φακέλου που περιέχει τις εικόνες, πρέπει να είναι στο working dir, και να περιέχει εικόνες .jpg
folders2 = sys.argv[3]
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

os.chdir("..") #πήγαινε πίσω στον αρχικό φάκελο
#για τον δεύτερο φάκελο
while True:
    try:
        os.chdir(folders2) #μπές μέσα στον δεύερο φάκελο
        break
    except OSError:
        print("Λάθος όνομα φακέλου, let's try that again..")
        folders2 = input()
for file in glob.glob("*.jpg"):
    counter2 = counter2 +1
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
    pixeldata2.append(shadowcount)
    print(shadowcount)

#βρίσκει την συχνότητα εμφάνισης για κάθε αριθμό μαύρων πίξελ.
for j in range(0, 26): # μέχρι 26 γιατί έχουμε αριθμό πίξελ 500χ500 = 250,000
    freq.append(0)
    for i in range(0, counter): #counter: πόσες εικόνες έχουμε
        if pixeldata[i] == int("{:2d}0000".format(j)): # αν αριθμός πίξελ == **,000 αύξησε την συχνότητα κατα +1
            freq[j] = freq[j] + 1

#βρίσκει την συχνότητα εμφάνισης για κάθε αριθμό μαύρων πίξελ. (2η εικονα)
for j in range(0, 26): # μέχρι 26 γιατί έχουμε αριθμό πίξελ 500χ500 = 250,000
    freq2.append(0)
    for i in range(0, counter2): #counter: πόσες εικόνες έχουμε
        if pixeldata2[i] == int("{:2d}0000".format(j)): # αν αριθμός πίξελ == **,000 αύξησε την συχνότητα κατα +1
            freq2[j] = freq2[j] + 1

os.chdir("..") #πήγαινε πίσω στον αρχικό φάκελο για να γράψεις τα αποτελέσματα
data = []
data2 = []
try:
    with open('result_data.csv', 'w') as file: #άνοιγμα αρχείου σε write mode
        for i in range(0, 26):
            s = "{:2d}0000,{}\n".format(i, freq[i]) #τελικό output
            file.write(s)
            data.append(int("{:2d}0000".format(i))) #χτίζουμε μια λίστα με τους αριθμούς πίξελ.
except OSError:
    print("Πρόβλημα στο γράψιμο του αρχείου αναφοράς csv.. ίσως δεν έχεις δικαιώματα να γράψεις στον φάκελο?")
    sys.exit

#2o
try:
    with open('result_data2.csv', 'w') as file: #άνοιγμα αρχείου σε write mode
        for i in range(0, 26):
            s = "{:2d}0000,{}\n".format(i, freq2[i]) #τελικό output
            file.write(s)
            data2.append(int("{:2d}0000".format(i))) #χτίζουμε μια λίστα με τους αριθμούς πίξελ.
except OSError:
    print("Πρόβλημα στο γράψιμο του αρχείου αναφοράς csv.. ίσως δεν έχεις δικαιώματα να γράψεις στον φάκελο?")
    sys.exit

#print(len(data)) #DEBUGGING
#print(len(freq))
x = np.array(data) #περνάμε τους αριθμούς και συχνότητες εμφάνισης σε numpy arrays
y = np.array(freq)

x2 = np.array(data2)
y2 = np.array(freq2)
#regresion γραμμές

def best_fit(x, y):
    m = ( (mean(x) * mean(y)) - mean(x*y) )  /  (( mean(x) **2) - ( mean(x**2) )) #η εξίσωση regression γραμμής
    b = mean(y) - m*mean(x) #σημείο τομής γραμμής
    return m, b

m, b = best_fit(x, y)
regression_line = [ (m*xs)+b for xs in x ] #υπολογισμός της τελικής γραμμής
print(m, b)
plt.scatter(x, y) #γράφημα scatterplot
plt.plot(x, regression_line)
plt.show() #εμφάνισε το γράφημα στην οθόνη


#αριθμητικό μέσο με βάρη
mean = sum(x * y) / sum(y)
mean2 = sum(x2 * y2) / sum(y2)
sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))
sigma2 = np.sqrt(sum(y2 * (x2 - mean)**2) / sum(y2))

#Γκαουσιανή μέθοδος
def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

popt,pcov = curve_fit(Gauss, x, y, p0=[max(y), mean, sigma])
popt2,pcov2 = curve_fit(Gauss, x2, y2, p0=[max(y2), mean2, sigma2])
#κάνουμε plot τα πρώτα στοιχεία και fitting τις καμπύλες
plt.plot(x, y,'b+',label='data')
plt.plot(x, Gauss(x, *popt),'r-',label='fit')
#κάνουμε plot τα δεύτερα στοιχεία και fitting τις καμπύλες
plt.plot(x2, y2,'b+',label='second data')
plt.plot(x2, Gauss(x2, *popt2),'r-',label='second fit')

plt.legend()
plt.title('Fitting 2 Γκαουσιανών καμπύλών')
plt.xlabel('Αριθμός Μαύρων Pixel')
plt.ylabel('Συχνότητα εμφάνισης')
plt.show()
