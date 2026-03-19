from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.clipboard import Clipboard

from openpyxl import load_workbook
from collections import defaultdict
from datetime import datetime


class RekapApp(App):

    def build(self):

        self.data_excel = []
        self.data_manual = []

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        with root.canvas.before:
            Color(rgba=get_color_from_hex("#1e272e"))
            self.bg = Rectangle(size=root.size, pos=root.pos)

        root.bind(size=self.update_bg, pos=self.update_bg)

        title = Label(
            text="[b]REKAP VOUCHER GABUNGAN[/b]",
            markup=True,
            size_hint=(1, 0.08),
            color=(1,1,1,1)
        )
        root.add_widget(title)

        # =======================
        # BUTTON FILE EXCEL
        # =======================
        btn_file = Button(
            text="PILIH FILE EXCEL",
            background_normal="",
            background_color=get_color_from_hex("#e67e22"),
            size_hint=(1, 0.08)
        )
        btn_file.bind(on_press=self.buka_file)
        root.add_widget(btn_file)

        # =======================
        # INPUT MANUAL
        # =======================
        self.tanggal = TextInput(hint_text="Tanggal (YYYY/MM/DD)", size_hint=(1,0.07))
        self.grup = TextInput(hint_text="Grup", size_hint=(1,0.07))
        self.harga = TextInput(hint_text="Harga", input_filter="int", size_hint=(1,0.07))

        root.add_widget(self.tanggal)
        root.add_widget(self.grup)
        root.add_widget(self.harga)

        btn_tambah = Button(
            text="TAMBAH DATA MANUAL",
            background_normal="",
            background_color=get_color_from_hex("#27ae60"),
            size_hint=(1,0.08)
        )
        btn_tambah.bind(on_press=self.tambah_manual)
        root.add_widget(btn_tambah)

        # =======================
        # BUTTON REKAP GABUNGAN
        # =======================
        btn_rekap = Button(
            text="REKAP SEMUA DATA",
            background_normal="",
            background_color=get_color_from_hex("#2980b9"),
            size_hint=(1,0.08)
        )
        btn_rekap.bind(on_press=self.rekap_semua)
        root.add_widget(btn_rekap)

        # =======================
        # HASIL
        # =======================
        self.result = Label(
            text="Belum ada data...",
            markup=True,
            size_hint_y=None,
            color=(1,1,1,1),
            halign="left",
            valign="top"
        )

        self.result.bind(texture_size=self.result.setter('size'))
        self.result.bind(
            width=lambda s, w: s.setter('text_size')(s, (w - 20, None))
        )

        scroll = ScrollView(size_hint=(1,0.4))
        scroll.add_widget(self.result)
        root.add_widget(scroll)

        # =======================
        # COPY
        # =======================
        btn_copy = Button(
            text="COPY HASIL",
            background_normal="",
            background_color=get_color_from_hex("#8e44ad"),
            size_hint=(1,0.07)
        )
        btn_copy.bind(on_press=self.copy_hasil)
        root.add_widget(btn_copy)

        self.notif = Label(text="", size_hint=(1,0.05))
        root.add_widget(self.notif)

        return root

    def update_bg(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

    def rupiah(self, x):
        return "Rp {:,}".format(int(x)).replace(",", ".")

    # =======================
    # FILE EXCEL
    # =======================
    def buka_file(self, instance):

        chooser = FileChooserListView(
            path="/storage/emulated/0",
            filters=["*.xlsx"]
        )

        popup = Popup(
            title="Pilih File Excel",
            content=chooser,
            size_hint=(0.9,0.9)
        )

        chooser.bind(
            on_submit=lambda x, selection, touch:
            self.load_excel(selection, popup)
        )

        popup.open()

    def load_excel(self, selection, popup):

        if not selection:
            return

        path = selection[0]
        popup.dismiss()

        try:
            wb = load_workbook(path)
            sheet = wb.active
        except:
            self.notif.text = "Gagal buka file"
            return

        self.data_excel.clear()

        header = [cell.value for cell in sheet[1]]

        try:
            i_grup = header.index("Grup pengguna")
            i_harga = header.index("Harga")
            i_tgl = header.index("Diaktifkan di")
        except:
            self.notif.text = "Header salah"
            return

        for row in sheet.iter_rows(min_row=2, values_only=True):

            grup = row[i_grup]
            harga = row[i_harga]
            tanggal = row[i_tgl]

            if grup and harga and tanggal:

                if isinstance(tanggal, datetime):
                    tgl = tanggal.strftime("%Y/%m/%d")
                else:
                    tgl = str(tanggal).split(" ")[0]

                try:
                    harga = int(harga)
                except:
                    continue

                self.data_excel.append((tgl, grup, harga))

        self.notif.text = "✔ Data Excel masuk"

    # =======================
    # INPUT MANUAL
    # =======================
    def tambah_manual(self, instance):

        tgl = self.tanggal.text.strip()
        grp = self.grup.text.strip()
        hrg = self.harga.text.strip()

        if not tgl or not grp or not hrg:
            self.notif.text = "Isi semua!"
            return

        try:
            datetime.strptime(tgl, "%Y/%m/%d")
            hrg = int(hrg)
        except:
            self.notif.text = "Format salah"
            return

        self.data_manual.append((tgl, grp, hrg))

        self.tanggal.text = ""
        self.grup.text = ""
        self.harga.text = ""

        self.notif.text = "✔ Data manual masuk"

    # =======================
    # REKAP GABUNGAN
    # =======================
    def rekap_semua(self, instance):

        semua = self.data_excel + self.data_manual

        if not semua:
            self.result.text = "Tidak ada data"
            return

        rekap = defaultdict(lambda: {"jumlah":0, "total":0})
        total_harian = defaultdict(int)

        for tgl, grp, hrg in semua:
            key = (tgl, grp)
            rekap[key]["jumlah"] += 1
            rekap[key]["total"] += hrg
            total_harian[tgl] += hrg

        hasil = "[b]===== HASIL REKAP GABUNGAN =====[/b]\n\n"

        last = None

        for (tgl, grp), val in sorted(rekap.items()):

            if last and tgl != last:
                hasil += f"[color=00ffcc][b]TOTAL : {self.rupiah(total_harian[last])}[/b][/color]\n\n"

            if tgl != last:
                hasil += f"[color=FFA726][b]Tanggal : {tgl}[/b][/color]\n"

            hasil += f"Grup : {grp}\n"
            hasil += f"Jumlah : {val['jumlah']}\n"
            hasil += f"Total : {self.rupiah(val['total'])}\n\n"

            last = tgl

        grand = sum(total_harian.values())

        hasil += f"\n[color=FFD700][b]GRAND TOTAL : {self.rupiah(grand)}[/b][/color]"

        self.result.text = hasil
        self.notif.text = "✔ Rekap gabungan selesai"

    def copy_hasil(self, instance):
        Clipboard.copy(self.result.text)
        self.notif.text = "✔ Disalin"
