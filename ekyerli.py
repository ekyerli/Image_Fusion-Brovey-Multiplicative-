from tkinter import Tk, Button
import tkinter.filedialog as filedialog
import skimage.io as io
import cv2
import numpy as np
from numpy import newaxis


class Project:
    openimage1 = ""
    openimage2 = ""

    def selectFile1(self):
        self.openimage1 = filedialog.askopenfilename(initialdir="/", title="Resim Dosyası Seçiniz", filetypes=(
            ("image files", "*.jpg | *.jpeg | *.tif | *.png"), ("all files", "*.*")))

    def selectFile2(self):
        self.openimage2 = filedialog.askopenfilename(initialdir="/", title="Resim Dosyası Seçiniz", filetypes=(
            ("image files", "*.jpg | *.jpeg | *.tif | *.png"), ("all files", "*.*")))

    def start(self):
        np.seterr(divide='ignore', invalid='ignore')
        P = io.imread(fname=self.openimage1)
        MS = io.imread(fname=self.openimage2)
        h1, w1 = P.shape  # gri resmi yüklüyoruz eğer renkliyse aşağıda ki c2 değeri gibi c1 değeri ekliyoruz.
        print(P.shape)
        h2, w2, c2 = MS.shape
        w2 = int(
            (MS.shape[1] * w1) / w2)  # en sondaki 5 yerine istediğimizdeğeri koyarak resmin boyutunu değiştirebiliriz.
        h2 = int(
            (MS.shape[0] * h1) / h2)  # en sondaki 5 yerine istediğimizdeğeri koyarak resmin boyutunu değiştirebiliriz.
        dim = (w2, h2)
        # resize image
        resized = cv2.resize(MS, dim, interpolation=2)  # 2 GÜZEL
        print('New_size : ', resized.shape)  # buraya kadar iki fotoğrafın boyutlarını eşitledik.
        R = resized[:, :, 0]  # ikinci resimde ki renkleri ayırıyoruz,daha sonra birinci resme algoritmadan çıkan filtreyi uygulayacağız.
        G = resized[:, :, 1]
        B = resized[:, :, 2]
        Total = ((R / 3 + G / 3 + B / 3) / P)  # alogritmamızı kuruyoruz.
        fR = (R / Total)
        fG = (G / Total)
        fB = (B / Total)
        fR = fR[:, :, newaxis]
        fG = fG[:, :, newaxis]
        fB = fB[:, :, newaxis]
        Son = np.insert(fB, [1], fR, axis=2)
        Son = np.insert(Son, [1], fG, axis=2)
        cv2.imwrite("BROVEY.jpg", Son)
        fR2 = (R * (P/256))
        print(fR2)
        fG2 = (G * (P/256))
        fB2 = (B * (P/256))
        fR2 = fR2[:, :, newaxis]
        fG2 = fG2[:, :, newaxis]
        fB2 = fB2[:, :, newaxis]
        Son2 = np.insert(fB2, [1], fR2, axis=2)
        Son2 = np.insert(Son2, [1], fG2, axis=2)
        cv2.imwrite("MULTICLICATIVE.jpg",Son2.astype(np.uint16))
        cv2.destroyAllWindows()


def main():
    root = Tk()
    root.title("Proje X")
    root.minsize(width=500, height=360)

    obj = Project()

    button1 = Button(root, text="1.RESMİ YÜKLE !", command=obj.selectFile1)
    button1.place(x=150, y=100)

    button2 = Button(root, text="2.RESMİ YÜKLE !", command=obj.selectFile2)
    button2.place(x=150, y=150)

    button3 = Button(root, text="BİRLEŞTİR !", command=obj.start)
    button3.place(x=150, y=200)
    root.mainloop()


if __name__ == "__main__":
    main()
