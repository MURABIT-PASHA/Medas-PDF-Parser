from PyPDF2 import PdfWriter, PdfReader

inputpdf = PdfReader(open("2022.pdf", "rb"))  # pdf dosya ismi yazılacak

for i in range(len(inputpdf.pages)):
    output = PdfWriter()
    output.add_page(inputpdf.pages[i])
    # dosyanın çıkarılacağı klasör ismi yazılacak
    with open("C:/Users/mrakd/Desktop/tk/2022/%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)


from PyPDF2 import PdfReader

counter = 0
for k in range(4737):
    # range verirken kaç tane dosya varsa sayı olarak yazılacak.
    # altta dosya dizinleri kısmı da düzenlenecek.
    pdfname = "C:/Users/mrakd/Desktop/tk/2022/" + str(k) + ".pdf"
    reader = PdfReader(pdfname)
    gg = reader.pages[0]
    parpage = gg.extract_text()
    splitt = parpage.split("no'lu tesisata")
    tesisat_no = splitt[0].split(",")[-1]
    pparpage = gg.extract_text()
    ssparpge = pparpage.split("no'lu sayac")
    sayac_no = ssparpge[0].split("Tarihinde")[-1]
    print(str(k) + str(tesisat_no) + " sayac: " + str(sayac_no))
    newpdfname = str(k) + "-" + str(tesisat_no) + "-" + str(sayac_no)
    newpdfnamey = newpdfname.replace("\n", "").replace(" ", "")
    output = PdfWriter()
    output.add_page(gg)
    with open("C:/Users/mrakd/Desktop/tk/2022x/%s.pdf" % newpdfnamey, "wb") as outputStream:
        output.write(outputStream)
