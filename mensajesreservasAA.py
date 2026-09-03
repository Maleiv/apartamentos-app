import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from html.parser import HTMLParser
import webbrowser
from urllib.parse import quote

ESTABLISHMENTS = {
    "Apartamentos Puerto Basella": {
        "wifi_name": "puertobasella",
        "wifi_password": "lobeira14",
        "booking_url": "https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/search_reservations.html?upcoming_reservations=1&source=nav&hotel_id=260913&lang=es",
        "message_sections": {
            "es": {
                "welcome": (
                    "En el salón hay una carpeta de color marrón que contiene información, sugerencias y "
                    "recomendaciones de restaurantes y servicios en la zona."
                ),
                "cleaning": (
                    "Hay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, "
                    "por si los necesitáis."
                ),
                "closing": (
                    "Cualquier cosa que necesitéis, decídmelo. Mañana por la mañana andará por ahí mi "
                    "empleada Mary Carmen. Espero que paséis una buena estancia."
                ),
                "cider": (
                    "Os hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la "
                    "provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino "
                    "blanco, sin escanciar. Espero que os guste."
                ),
            },
            "en": {
                "welcome": (
                    "In the living room, there is a brown folder with useful information, suggestions, "
                    "and recommendations for restaurants and services in the area."
                ),
                "cleaning": (
                    "There are cleaning supplies in a cupboard outside the apartment, next to the lift, "
                    "in case you need them."
                ),
                "closing": (
                    "If you need anything, just let me know. My employee Mary Carmen will be around "
                    "tomorrow morning. I hope you have a lovely stay."
                ),
                "cider": (
                    "We have left you a bottle of natural artisan cider, made in our village in the "
                    "province of Lugo with apples from our own trees. Please drink it chilled, like a "
                    "white wine, without pouring it from a height. I hope you enjoy it."
                ),
            },
        },
        "apartments": {
            "1A": {"code": "9856"},
            "1B": {"code": "6248"},
            "2A": {"code": "6574"},
            "2B": {"code": "8784"},
            "3A": {"code": "5321"},
            "3B": {"code": "9476"},
        },
        "apartment_notes": {
            "es": {
                "1A": (
                    " También tenéis colchonetas para el mobiliario exterior dentro del apartamento en el "
                    "cuarto de la lavandería.\nEl toldo de la pérgola se acciona con un mando a distancia "
                    "que está en el salón. Tanto el toldo como los cojines rogamos se mantengan recogidos "
                    "después de su uso, especialmente el toldo por la noche por seguridad."
                ),
                "1B": (
                    " También tenéis colchonetas para el mobiliario exterior en un contenedor en la "
                    "terraza.\nEl toldo de la pérgola se acciona con un mando a distancia que está en el "
                    "salón. Tanto el toldo como los cojines rogamos se mantengan recogidos después de su uso, "
                    "especialmente el toldo por la noche por seguridad."
                ),
            },
            "en": {
                "1A": (
                    " You will also find cushions for the outdoor furniture inside the apartment, in the "
                    "laundry room.\nThe pergola awning is operated with a remote control, which is in the "
                    "living room. Please make sure both the awning and the cushions are put away after use, "
                    "especially the awning at night, for safety."
                ),
                "1B": (
                    " You will also find cushions for the outdoor furniture in a storage box on the "
                    "terrace.\nThe pergola awning is operated with a remote control, which is in the "
                    "living room. Please make sure both the awning and the cushions are put away after use, "
                    "especially the awning at night, for safety."
                ),
            },
        },
    },
    "Apartamentos Autor": {
        "wifi_name": "puertobasella",
        "wifi_password": "a123b456",
        "booking_url": "https://admin.booking.com/",
        "message_sections": {
            "es": {
                "welcome": "",
                "cleaning": (
                    "Hay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, "
                    "por si los necesitáis."
                ),
                "closing": (
                    "Si necesitáis cualquier cosa durante la estancia, escribidme y os ayudo enseguida. "
                    "¡Disfrutad mucho de vuestro apartamento!"
                ),
                "cider": (
                    "Os hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la "
                    "provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino "
                    "blanco, sin escanciar. Espero que os guste."
                ),
            },
            "en": {
                "welcome": "",
                "cleaning": (
                    "There are cleaning supplies in a cupboard outside the apartment, next to the lift, "
                    "in case you need them."
                ),
                "closing": (
                    "If you need anything during your stay, just send me a message and I will help you "
                    "right away. Enjoy your apartment!"
                ),
                "cider": (
                    "We have left you a bottle of natural artisan cider, made in our village in the "
                    "province of Lugo with apples from our own trees. Please drink it chilled, like a "
                    "white wine, without pouring it from a height. I hope you enjoy it."
                ),
            },
        },
        "apartments": {
            "1": {"code": "3279", "wifi_name": "Puerto Basella P1", "wifi_password": "a123b456"},
            "2": {"code": "5972", "wifi_name": "PUERTO BASELLA", "wifi_password": "Lobeira14"},
            "3": {"code": "7021"},
            "4": {"code": "5676", "wifi_name": "TP-LINK_8D44", "wifi_password": "32288285"},
        },
        "apartment_notes": {"es": {}, "en": {}},
    },
}


class MisterPlanExportParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self._tr_depth = 0
        self._td_depth = 0
        self._target_depth = None
        self._cells = []
        self._current_cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "tr":
            self._tr_depth += 1
            row_classes = attrs.get("class", "")
            if "TCloudDisponibilidad_ListadoReservas" in row_classes:
                self._target_depth = self._tr_depth
                self._cells = []

        if tag == "td":
            self._td_depth += 1
            if self._target_depth and self._tr_depth == self._target_depth and self._td_depth == 1:
                self._current_cell = []

    def handle_endtag(self, tag):
        if tag == "td":
            if self._current_cell is not None and self._td_depth == 1:
                text = " ".join("".join(self._current_cell).split())
                self._cells.append(text)
                self._current_cell = None
            self._td_depth -= 1

        if tag == "tr":
            if self._target_depth == self._tr_depth and len(self._cells) >= 6:
                self.rows.append({
                    "reservation_date": self._cells[0],
                    "establishment": self._cells[1],
                    "apartments_text": self._cells[2],
                    "reservation_id": self._cells[3],
                    "checkin": self._cells[4],
                    "guest": self._cells[5].strip(),
                })
                self._target_depth = None
                self._cells = []
            self._tr_depth -= 1

    def handle_data(self, data):
        if self._current_cell is not None:
            self._current_cell.append(data)


app = tk.Tk()
app.title("Auto mensajes apartamentos")
app.geometry("920x740")


def update_apartment_options(*_):
    selected_establishment = establishment_var.get()
    apartments = ESTABLISHMENTS[selected_establishment]["apartments"].keys()

    for widget in apartment_frame.winfo_children():
        widget.destroy()

    apartment_vars.clear()
    for apartment in apartments:
        apartment_vars[apartment] = tk.BooleanVar(value=False)
        tk.Checkbutton(
            apartment_frame,
            text=apartment,
            variable=apartment_vars[apartment],
            width=8,
            anchor="w",
        ).pack(side="left", padx=6)


def format_list(items, language_code):
    if len(items) <= 1:
        return items[0] if items else ""

    conjunction = "and" if language_code == "en" else "y"
    return f"{', '.join(items[:-1])} {conjunction} {items[-1]}"


def format_code_lines(selected_apartments, apartments, language_code):
    lines = []

    for ap in selected_apartments:
        password = apartments.get(ap, {}).get("code", "")

        if language_code == "en":
            lines.append(f"You can enter apartment {ap} with this code: {password}✅.")
        else:
            lines.append(f"Puedes entrar al apartamento {ap} con este código: {password}✅.")

    return "\n".join(lines)


def format_apartment_notes(selected_apartments, notes):
    return "\n".join(notes.get(ap, "") for ap in selected_apartments if notes.get(ap, ""))


def wifi_for_apartment(establishment_data, ap):
    apartment_data = establishment_data["apartments"].get(ap, {})

    return {
        "apartment_name": ap,
        "name": apartment_data.get("wifi_name", establishment_data["wifi_name"]),
        "password": apartment_data.get("wifi_password", establishment_data["wifi_password"]),
    }


def format_wifi_text(selected_apartments, establishment_data, language_code):
    wifi_entries = [wifi_for_apartment(establishment_data, ap) for ap in selected_apartments]
    unique_entries = []

    for entry in wifi_entries:
        if not any(
            existing["name"] == entry["name"] and existing["password"] == entry["password"]
            for existing in unique_entries
        ):
            unique_entries.append(entry)

    if len(unique_entries) == 1:
        name = unique_entries[0]["name"]
        password = unique_entries[0]["password"]

        if language_code == "en":
            return f'The Wi-Fi network is "{name}" and the password is "{password}".'

        return f'La wifi es "{name}" y la contraseña es "{password}".'

    if language_code == "en":
        lines = ["The Wi-Fi details are:"]
        lines.extend(
            f'Apartment {entry["apartment_name"]}: network "{entry["name"]}" '
            f'and password "{entry["password"]}".'
            for entry in wifi_entries
        )
        return "\n".join(lines)

    lines = ["Los datos de la wifi son:"]
    lines.extend(
        f'Apartamento {entry["apartment_name"]}: red "{entry["name"]}" '
        f'y contraseña "{entry["password"]}".'
        for entry in wifi_entries
    )
    return "\n".join(lines)


def join_message_parts(parts):
    return "\n".join(part for part in parts if part.strip())


def generate_message():
    name = name_entry.get().strip()
    establishment_name = establishment_var.get()
    selected_apartments = [ap for ap, var in apartment_vars.items() if var.get()]
    special = sp_var.get()
    language = language_var.get()

    if not name:
        # messagebox.showwarning("Error", "Introduce el nombre del huésped", parent=app)
        return

    if not selected_apartments:
        messagebox.showwarning("Error", "Selecciona al menos un apartamento", parent=app)
        return

    establishment_data = ESTABLISHMENTS[establishment_name]
    apartments = establishment_data["apartments"]

    language_code = "en" if language == "Inglés" else "es"
    selected_list = format_list(selected_apartments, language_code)
    code_lines = format_code_lines(selected_apartments, apartments, language_code)
    specific = format_apartment_notes(
        selected_apartments,
        establishment_data["apartment_notes"][language_code],
    )
    wifi_text = format_wifi_text(selected_apartments, establishment_data, language_code)
    sections = establishment_data["message_sections"][language_code]

    if language_code == "en":
        apartment_label = "apartment" if len(selected_apartments) == 1 else "apartments"
        verb = "is" if len(selected_apartments) == 1 else "are"
        entrance_text = (
            "This code also opens the main entrance using the black keypad."
            if len(selected_apartments) == 1
            else "These codes also open the main entrance using the black keypad."
        )

        message = join_message_parts([
            f"Hello {name}, your {apartment_label} at {establishment_name} {verb} {selected_list}.\n\n"
            f"{code_lines}\n\n"
            f"{entrance_text} "
            f"{wifi_text}",
            sections["welcome"],
            f"{sections['cleaning']}{specific}",
            sections["closing"],
        ])
    else:
        apartment_label = "apartamento" if len(selected_apartments) == 1 else "apartamentos"
        possessive = "tu" if len(selected_apartments) == 1 else "tus"
        verb = "es" if len(selected_apartments) == 1 else "son"
        entrance_text = (
            "Este código también abre el portal utilizando el teclado negro."
            if len(selected_apartments) == 1
            else "Estos códigos también abren el portal utilizando el teclado negro."
        )

        message = join_message_parts([
            f"Hola {name}, {possessive} {apartment_label} en {establishment_name} {verb} {selected_list}.\n\n"
            f"{code_lines}\n\n"
            f"{entrance_text} "
            f"{wifi_text}",
            sections["welcome"],
            f"{sections['cleaning']}{specific}",
            sections["closing"],
        ])

    if special == "SI":
        message += f"\n{sections['cider']}"

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, message)


def copy_to_clipboard():
    app.clipboard_clear()
    app.clipboard_append(result_text.get("1.0", tk.END))
    app.update()
    messagebox.showinfo("Info", "Mensaje copiado al portapapeles!", parent=app)


def open_whatsapp():
    message = result_text.get("1.0", tk.END).strip()

    if not message:
        generate_message()
        message = result_text.get("1.0", tk.END).strip()

    if not message:
        return

    webbrowser.open(f"https://wa.me/?text={quote(message)}")


def open_booking_messages():
    establishment_name = establishment_var.get()
    booking_messages_url = ESTABLISHMENTS[establishment_name]["booking_url"]
    webbrowser.open(booking_messages_url)


def parse_misterplan_file(path):
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=encoding) as file:
                content = file.read()
            break
        except UnicodeDecodeError:
            continue
    else:
        with open(path, "r", encoding="utf-8", errors="replace") as file:
            content = file.read()

    parser = MisterPlanExportParser()
    parser.feed(content)
    return parser.rows


def match_establishment(name):
    normalized = " ".join(name.split()).lower()

    for establishment_name in ESTABLISHMENTS:
        if establishment_name.lower() == normalized:
            return establishment_name

    return None


def match_apartments(establishment_name, apartments_text):
    if not establishment_name:
        return []

    available_apartments = ESTABLISHMENTS[establishment_name]["apartments"].keys()
    imported_tokens = set(apartments_text.replace(",", " ").replace(";", " ").split())
    return [ap for ap in available_apartments if ap in imported_tokens]


def import_misterplan_file():
    path = filedialog.askopenfilename(
        parent=app,
        title="Importar archivo MisterPlan",
        filetypes=[
            ("Archivos MisterPlan", "*.xls *.html *.htm"),
            ("Todos los archivos", "*.*"),
        ],
    )

    if not path:
        return

    try:
        rows = parse_misterplan_file(path)
    except OSError as error:
        messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{error}", parent=app)
        return

    imported_reservations.clear()
    import_tree.delete(*import_tree.get_children())

    for row in rows:
        establishment_name = match_establishment(row["establishment"])
        apartments = match_apartments(establishment_name, row["apartments_text"])
        row["matched_establishment"] = establishment_name
        row["matched_apartments"] = apartments
        imported_reservations.append(row)

        import_tree.insert(
            "",
            "end",
            iid=str(len(imported_reservations) - 1),
            values=(
                row["guest"],
                establishment_name or row["establishment"],
                ", ".join(apartments) or row["apartments_text"],
                row["checkin"],
                row["reservation_id"],
            ),
        )

    import_status_var.set(f"{len(rows)} reserva(s) importada(s).")

    if rows:
        first_item = import_tree.get_children()[0]
        import_tree.selection_set(first_item)
        import_tree.focus(first_item)


def load_selected_import():
    selected = import_tree.selection()

    if not selected:
        messagebox.showwarning("Error", "Selecciona una reserva importada", parent=app)
        return

    row = imported_reservations[int(selected[0])]
    establishment_name = row["matched_establishment"]
    apartments = row["matched_apartments"]

    if not establishment_name:
        messagebox.showwarning(
            "Error",
            f"No reconozco el alojamiento importado:\n{row['establishment']}",
            parent=app,
        )
        return

    if not apartments:
        messagebox.showwarning(
            "Error",
            f"No reconozco los apartamentos importados:\n{row['apartments_text']}",
            parent=app,
        )
        return

    name_entry.delete(0, tk.END)
    name_entry.insert(0, row["guest"])
    establishment_var.set(establishment_name)
    update_apartment_options()

    for ap, var in apartment_vars.items():
        var.set(ap in apartments)

    notebook.select(manual_tab)
    generate_message()


# Inputs
notebook = ttk.Notebook(app)
manual_tab = ttk.Frame(notebook)
import_tab = ttk.Frame(notebook)
notebook.add(manual_tab, text="Manual")
notebook.add(import_tab, text="Importar check-ins")
notebook.pack(fill="both", expand=True, padx=12, pady=12)

tk.Label(manual_tab, text="Nombre:").pack(pady=5)
name_entry = tk.Entry(manual_tab)
name_entry.pack(pady=5)

tk.Label(manual_tab, text="Establecimiento:").pack(pady=6)
establishment_var = tk.StringVar(value=list(ESTABLISHMENTS.keys())[0])
establishment_menu = tk.OptionMenu(manual_tab, establishment_var, *ESTABLISHMENTS.keys())
establishment_menu.pack(pady=6)

tk.Label(manual_tab, text="Apartamento:").pack(pady=6)
apartment_vars = {}
apartment_frame = tk.Frame(manual_tab)
apartment_frame.pack(pady=6)

tk.Label(manual_tab, text="Idioma del mensaje:").pack(pady=6)
language_var = tk.StringVar(value="Español")
language_options = ["Español", "Inglés"]
language_menu = tk.OptionMenu(manual_tab, language_var, *language_options)
language_menu.pack(pady=5)

tk.Label(manual_tab, text="Sidra:").pack(pady=6)
sp_var = tk.StringVar(value="SI")
sp_options = ["SI", "NO"]
sp_menu = tk.OptionMenu(manual_tab, sp_var, *sp_options)
sp_menu.pack(pady=5)

tk.Button(manual_tab, text="Generar mensaje", command=generate_message).pack(pady=10)

tk.Label(manual_tab, text="Mensaje generado:").pack(pady=5)
result_text = tk.Text(manual_tab, height=14, width=105)
result_text.pack(pady=5, padx=10, fill="both", expand=True)

button_frame = tk.Frame(manual_tab)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Copiar mensaje", command=copy_to_clipboard).pack(side="left", padx=5)
tk.Button(button_frame, text="Abrir WhatsApp", command=open_whatsapp).pack(side="left", padx=5)
tk.Button(button_frame, text="Abrir mensajes en Booking", command=open_booking_messages).pack(side="right", padx=5)

imported_reservations = []
import_toolbar = tk.Frame(import_tab)
import_toolbar.pack(fill="x", padx=12, pady=12)

tk.Button(import_toolbar, text="Importar archivo MisterPlan", command=import_misterplan_file).pack(side="left")
tk.Button(import_toolbar, text="Cargar seleccionado en formulario", command=load_selected_import).pack(
    side="left",
    padx=8,
)

import_status_var = tk.StringVar(value="Importa el archivo .xls de entradas de MisterPlan.")
tk.Label(import_tab, textvariable=import_status_var, anchor="w").pack(fill="x", padx=12)

columns = ("guest", "establishment", "apartments", "checkin", "reservation_id")
import_tree = ttk.Treeview(import_tab, columns=columns, show="headings", height=16)
import_tree.heading("guest", text="Cliente")
import_tree.heading("establishment", text="Alojamiento")
import_tree.heading("apartments", text="Apartamentos")
import_tree.heading("checkin", text="Entrada - noches")
import_tree.heading("reservation_id", text="Id reserva")
import_tree.column("guest", width=190)
import_tree.column("establishment", width=220)
import_tree.column("apartments", width=120)
import_tree.column("checkin", width=140)
import_tree.column("reservation_id", width=120)
import_tree.pack(fill="both", expand=True, padx=12, pady=10)
import_tree.bind("<Double-1>", lambda _event: load_selected_import())

establishment_var.trace_add("write", update_apartment_options)
update_apartment_options()

app.mainloop()
