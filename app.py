import customtkinter as ctk
from tkinter import messagebox
import os
from datetime import datetime
from fpdf import FPDF


class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generator Faktur i Ofert Budowlanych")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.materialy = []
        self.robocizna = []

        self.create_widgets()

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(top_frame, text="Typ dokumentu:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_doc_type = ctk.CTkComboBox(top_frame, values=["Faktura", "Oferta"])
        self.combo_doc_type.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(top_frame, text="Numer:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_nr = ctk.CTkEntry(top_frame, placeholder_text="np. 1/2026")
        self.entry_nr.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(top_frame, text="Tytuł (opcjonalnie):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_title = ctk.CTkEntry(top_frame, placeholder_text="np. za remont dachu", width=200)
        self.entry_title.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(top_frame, text="Miejscowość:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_city = ctk.CTkEntry(top_frame, placeholder_text="np. Warszawa")
        self.entry_city.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        mid_frame = ctk.CTkFrame(self)
        mid_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(mid_frame, text="Kategoria:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_category = ctk.CTkComboBox(mid_frame, values=["Materiał", "Robocizna"])
        self.combo_category.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(mid_frame, text="Nazwa pozycji:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_name = ctk.CTkEntry(mid_frame, width=300)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(mid_frame, text="Ilość:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_qty = ctk.CTkEntry(mid_frame)
        self.entry_qty.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(mid_frame, text="Cena Netto:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_price = ctk.CTkEntry(mid_frame)
        self.entry_price.grid(row=1, column=3, padx=5, pady=5)

        btn_add = ctk.CTkButton(mid_frame, text="Dodaj Pozycję", command=self.add_item, fg_color="#28a745",
                                hover_color="#218838")
        btn_add.grid(row=1, column=4, padx=15, pady=5)

        self.textbox = ctk.CTkTextbox(self, height=200)
        self.textbox.pack(pady=10, padx=10, fill="both", expand=True)
        self.textbox.insert("0.0", "Dodane pozycje pojawią się tutaj...\n\n")
        self.textbox.configure(state="disabled")

        btn_generate = ctk.CTkButton(self, text="GENERUJ PLIK PDF", command=self.generate_pdf,
                                     font=("Helvetica", 16, "bold"), height=50)
        btn_generate.pack(pady=15, padx=10, fill="x")

    def add_item(self):
        try:
            kategoria = self.combo_category.get()
            nazwa = self.entry_name.get()

            if not nazwa:
                raise ValueError("Brak nazwy")

            ilosc = float(self.entry_qty.get().replace(',', '.'))
            cena_netto = float(self.entry_price.get().replace(',', '.'))

            w_netto = ilosc * cena_netto
            kwota_vat = w_netto * 0.23
            w_brutto = w_netto * 1.23

            pozycja = {
                "nazwa": nazwa,
                "ilosc": ilosc,
                "cena_netto": cena_netto,
                "w_netto": w_netto,
                "kwota_vat": kwota_vat,
                "w_brutto": w_brutto
            }

            if kategoria == "Materiał":
                self.materialy.append(pozycja)
            else:
                self.robocizna.append(pozycja)

            self.textbox.configure(state="normal")
            self.textbox.insert("end",
                                f"[{kategoria}] {nazwa} | Ilość: {ilosc} | Netto: {w_netto:.2f} zł | Brutto: {w_brutto:.2f} zł\n")
            self.textbox.configure(state="disabled")

            self.entry_name.delete(0, 'end')
            self.entry_qty.delete(0, 'end')
            self.entry_price.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Błąd",
                                 "Wprowadź poprawne dane w polach 'Ilość' oraz 'Cena Netto' (tylko liczby) i upewnij się, że wpisałeś nazwę!")

    def generate_pdf(self):
        typ_dok = self.combo_doc_type.get()
        nr_faktury = self.entry_nr.get() or "Brak"
        tytul_dok = self.entry_title.get()
        miejscowosc = self.entry_city.get() or "Nie podano"
        data_wystawienia = datetime.now().strftime("%d.%m.%Y")

        pdf = FPDF()
        pdf.add_page()

        font_path = r"C:\Windows\Fonts\arial.ttf"
        font_bold_path = r"C:\Windows\Fonts\arialbd.ttf"

        if os.path.exists(font_path) and os.path.exists(font_bold_path):
            pdf.add_font("ArialPL", "", font_path)
            pdf.add_font("ArialPL", "B", font_bold_path)
            font_family = "ArialPL"
        else:
            font_family = "helvetica"

        pdf.set_font(font_family, "B", 18)
        naglowek_glowny = f"{typ_dok.upper()} nr {nr_faktury}"
        pdf.cell(0, 10, naglowek_glowny, align="L", new_x="LMARGIN", new_y="NEXT")

        if tytul_dok:
            pdf.set_font(font_family, "", 12)
            pdf.cell(0, 6, f"Tytuł: {tytul_dok}", align="L", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(5)

        pdf.set_font(font_family, "", 10)
        pdf.cell(0, 5, f"Miejsce wystawienia: {miejscowosc}", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, f"Data wystawienia: {data_wystawienia}", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        pdf.set_font(font_family, "B", 12)
        pdf.cell(0, 8, "Wystawiający (Sprzedawca):", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_family, "", 10)
        pdf.cell(0, 6, "Bamar Bartosz Borowski", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, "ul. Teresy 4, 42-200 Częstochowa", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, "NIP: 949-164-32-60 ", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        def rysuj_tabele(tytul, lista_pozycji):
            if not lista_pozycji:
                return 0, 0, 0

            pdf.set_font(font_family, "B", 12)
            pdf.cell(0, 10, tytul, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font(font_family, "", 9)

            col_widths = (45, 10, 15, 15, 10, 15)

            with pdf.table(col_widths=col_widths, text_align="CENTER") as table:
                row = table.row()
                for header in ["Nazwa", "Ilość", "Cena Netto", "W. Netto", "VAT", "W. Brutto"]:
                    row.cell(header)

                suma_netto = suma_vat = suma_brutto = 0

                for item in lista_pozycji:
                    row = table.row()
                    row.cell(item['nazwa'], align="LEFT")
                    row.cell(str(item['ilosc']))
                    row.cell(f"{item['cena_netto']:.2f} zł", align="RIGHT")
                    row.cell(f"{item['w_netto']:.2f} zł", align="RIGHT")
                    row.cell(f"{item['kwota_vat']:.2f} zł", align="RIGHT")
                    row.cell(f"{item['w_brutto']:.2f} zł", align="RIGHT")

                    suma_netto += item['w_netto']
                    suma_vat += item['kwota_vat']
                    suma_brutto += item['w_brutto']

                pdf.set_font(font_family, "B", 9)
                row = table.row()
                row.cell("PODSUMOWANIE SEKCJI:", colspan=3, align="RIGHT")
                row.cell(f"{suma_netto:.2f} zł", align="RIGHT")
                row.cell(f"{suma_vat:.2f} zł", align="RIGHT")
                row.cell(f"{suma_brutto:.2f} zł", align="RIGHT")

            pdf.ln(5)
            return suma_netto, suma_vat, suma_brutto

        mat_n, mat_v, mat_b = rysuj_tabele("Część I: Koszt Materiałów", self.materialy)
        rob_n, rob_v, rob_b = rysuj_tabele("Część II: Koszt Robocizny", self.robocizna)

        pdf.ln(10)
        pdf.set_font(font_family, "B", 12)
        pdf.cell(0, 10, "PODSUMOWANIE GŁÓWNE:", new_x="LMARGIN", new_y="NEXT")

        szerokosc_etykiety = 65
        szerokosc_wartosci = 40

        pdf.set_font(font_family, "B", 12)
        pdf.cell(szerokosc_etykiety, 10, "DO ZAPŁATY (BRUTTO):", border=1)
        pdf.cell(szerokosc_wartosci, 10, f"{mat_b + rob_b:.2f} zł", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font(font_family, "", 11)
        pdf.cell(szerokosc_etykiety, 8, "Suma Netto:", border=1)
        pdf.cell(szerokosc_wartosci, 8, f"{mat_n + rob_n:.2f} zł", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.cell(szerokosc_etykiety, 8, "Kwota VAT:", border=1)
        pdf.cell(szerokosc_wartosci, 8, f"{mat_v + rob_v:.2f} zł", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

        nazwa_pliku = f"{typ_dok}_{nr_faktury.replace('/', '_')}.pdf"
        try:
            pdf.output(nazwa_pliku)
            messagebox.showinfo("Sukces!",
                                f"Wygenerowano pomyślnie plik:\n{nazwa_pliku}\nZnajdziesz go w tym samym folderze.")
        except Exception as e:
            messagebox.showerror("Błąd",
                                 f"Nie udało się zapisać PDF. Upewnij się, że plik nie jest otwarty w innym programie.\nSzczegóły: {e}")


if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()