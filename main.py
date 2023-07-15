import os
import threading
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from PyPDF2 import PdfWriter, PdfReader
from kivymd.toast import toast


class DragDropPdfApp(MDApp):
    progress_value = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_file_name = "Null"
        self.desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'MedasPDF')
        self.temporary_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'MedasPDF', 'temporary')
        self.screen = Builder.load_file('./main.kv')

    def build(self):
        self.title = 'MEDAŞ PDF Parser'
        self.icon = './icon.ico'
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        Window.size = (640, 480)
        Window.bind(on_dropfile=self.on_file_drop)
        return self.screen

    def on_file_drop(self, window, file_path):
        self.source_file_name = file_path.decode("utf-8")

    def start_long_running_task(self):
        if self.source_file_name != "Null":
            toast("İşleminiz başlatılıyor", duration=1.0)
            thread = threading.Thread(target=self.start_parse)
            thread.start()
            toast("İşleminiz tamamlandı")
        else:
            toast("Bir dosya seçmediniz")

    def create_desktop_path(self) -> bool:
        try:
            os.makedirs(self.desktop_path)
            return True
        except FileExistsError:
            return True

    def create_temporary_path(self) -> bool:
        try:
            os.makedirs(self.temporary_path)
            return True
        except FileExistsError:
            return True

    def start_parse(self):
        input_pdf = PdfReader(open(self.source_file_name, "rb"))
        for i in range(len(input_pdf.pages)):
            output = PdfWriter()
            output.add_page(input_pdf.pages[i])
            if self.create_temporary_path():
                with open(f"{self.temporary_path}/{i}.pdf", "wb") as outputStream:
                    output.write(outputStream)
            else:
                toast("Dosya yazma sistemi hatası var")

        for k in range(len(input_pdf.pages)):
            pdf_name = f"{self.temporary_path}/" + str(k) + ".pdf"
            reader = PdfReader(pdf_name)
            read_page = reader.pages[0]
            first_extracted_part = read_page.extract_text()
            first_split = first_extracted_part.split("no'lu tesisata")
            installation_number = first_split[0].split(",")[-1]
            second_split = first_extracted_part.split("no'lu sayac")
            counter_number = second_split[0].split("Tarihinde")[-1]
            new_pdf_name = (str(k) + "-" + str(installation_number) + "-" + str(counter_number)) \
                .replace("\n", "").replace(" ", "")
            output = PdfWriter()
            output.add_page(read_page)
            if self.create_desktop_path():
                with open(f"{self.desktop_path}/{new_pdf_name}.pdf", "wb") as outputStream:
                    output.write(outputStream)
                    self.root.ids.progress_bar.value = 100 * (k + 1) / len(input_pdf.pages)
            else:
                toast('Dosya yazma sistemi hatası var')
        for file_name in os.listdir(self.temporary_path):
            file_path = os.path.join(self.temporary_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        if os.path.isdir(self.temporary_path):
            os.rmdir(self.temporary_path)


if __name__ == '__main__':
    DragDropPdfApp().run()
