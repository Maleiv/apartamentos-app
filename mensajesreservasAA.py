import tkinter as tk
from tkinter import messagebox
import webbrowser

ESTABLISHMENTS = {
    "Apartamentos Basella": {
        "wifi_name": "puertobasella",
        "wifi_password": "lobeira14",
        "booking_url": "https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/search_reservations.html?upcoming_reservations=1&source=nav&hotel_id=260913&lang=es",
        "message_sections": {
            "welcome": (
                "En el salón hay una carpeta de color marrón que contiene información, sugerencias y "
                "recomendaciones de restaurantes y servicios en la zona."
            ),
            "closing": (
                "Cualquier cosa que necesitéis, decídmelo. Mañana por la mañana andará por ahí mi "
                "empleada Mary Carmen. Espero que paséis una buena estancia."
            ),
        },
        "apartments": {
            "1A": {"code": "9856"},
            "1B": {"code": "6248"},
            "2A": {"code": "6574"},
            "2B": {"code": "2584"},
            "3A": {"code": "2784"},
            "3B": {"code": "7447"},
        },
        "apartment_notes": {
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
    },
    "Apartamentos Mirador": {
        "wifi_name": "miradorapartamentos",
        "wifi_password": "mirador2026",
        "booking_url": "https://admin.booking.com/",
        "message_sections": {
            "welcome": (
                "En la mesa del salón tenéis una guía rápida con recomendaciones de playas, rutas y "
                "servicios de la zona."
            ),
            "closing": (
                "Si necesitáis cualquier ayuda durante la estancia, escribidme y os ayudo enseguida. "
                "¡Disfrutad mucho de vuestras vacaciones!"
            ),
        },
        "apartments": {
            "A1": {"code": "1122"},
            "A2": {"code": "3344"},
            "B1": {"code": "5566"},
            "B2": {"code": "7788"},
        },
        "apartment_notes": {
            "A1": " El apartamento A1 incluye acceso directo al jardín común.",
            "B2": " El apartamento B2 tiene plaza de garaje reservada nº8.",
        },
    },
}


app = tk.Tk()
app.title("Auto mensajes apartamentos")
app.geometry("860x640")


def update_apartment_options(*_):
    selected_establishment = establishment_var.get()
    apartments = ESTABLISHMENTS[selected_establishment]["apartments"].keys()

    apartment_menu["menu"].delete(0, "end")
    for apartment in apartments:
        apartment_menu["menu"].add_command(
            label=apartment,
            command=tk._setit(ap_var, apartment),
        )

    ap_var.set("Selecciona apartamento")


def generate_message():
    name = name_entry.get().strip()
    establishment_name = establishment_var.get()
    ap = ap_var.get()
    special = sp_var.get()

    if not name:
        messagebox.showwarning("Error", "Introduce el nombre del huésped", parent=app)
        return

    if ap == "Selecciona apartamento":
        messagebox.showwarning("Error", "Selecciona apartamento", parent=app)
        return

    establishment_data = ESTABLISHMENTS[establishment_name]
    apartments = establishment_data["apartments"]

    password = apartments.get(ap, {}).get("code", "")
    wifi_name = establishment_data["wifi_name"]
    wifi_password = establishment_data["wifi_password"]
    specific = establishment_data["apartment_notes"].get(ap, "")
    welcome = establishment_data["message_sections"]["welcome"]
    closing = establishment_data["message_sections"]["closing"]

    message = (
        f"Hola {name} tu apartamento en {establishment_name} es el {ap}. "
        f"Entras con este código: {password}✅, que también abre el portal utilizando el teclado negro. "
        f"La wifi es \"{wifi_name}\" y la contraseña es \"{wifi_password}\".\n"
        f"{welcome}\n"
        "Hay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, "
        f"por si los necesitáis.{specific}\n"
        f"{closing}"
    )

    if special == "SI":
        message += (
            "\nOs hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la "
            "provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino "
            "blanco, sin escanciar. Espero que os guste."
        )

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, message)


def copy_to_clipboard():
    app.clipboard_clear()
    app.clipboard_append(result_text.get("1.0", tk.END))
    app.update()
    messagebox.showinfo("Info", "Mensaje copiado al portapapeles!", parent=app)


def open_booking_messages():
    establishment_name = establishment_var.get()
    booking_messages_url = ESTABLISHMENTS[establishment_name]["booking_url"]
    webbrowser.open(booking_messages_url)


# Inputs
tk.Label(app, text="Nombre:").pack(pady=5)
name_entry = tk.Entry(app)
name_entry.pack(pady=5)

tk.Label(app, text="Establecimiento:").pack(pady=6)
establishment_var = tk.StringVar(value=list(ESTABLISHMENTS.keys())[0])
establishment_menu = tk.OptionMenu(app, establishment_var, *ESTABLISHMENTS.keys())
establishment_menu.pack(pady=6)

tk.Label(app, text="Apartamento:").pack(pady=6)
ap_var = tk.StringVar(value="Selecciona apartamento")
apartment_menu = tk.OptionMenu(app, ap_var, "Selecciona apartamento")
apartment_menu.pack(pady=6)

tk.Label(app, text="Sidra:").pack(pady=6)
sp_var = tk.StringVar(value="NO")
sp_options = ["SI", "NO"]
sp_menu = tk.OptionMenu(app, sp_var, *sp_options)
sp_menu.pack(pady=5)


tk.Button(app, text="Generar mensaje", command=generate_message).pack(pady=10)

tk.Label(app, text="Mensaje generado:").pack(pady=5)
result_text = tk.Text(app, height=14, width=95)
result_text.pack(pady=5)

button_frame = tk.Frame(app)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Copiar mensaje", command=copy_to_clipboard).pack(side="left", padx=5)
tk.Button(button_frame, text="Abrir mensajes en Booking", command=open_booking_messages).pack(side="right", padx=5)

establishment_var.trace_add("write", update_apartment_options)
update_apartment_options()

app.mainloop()
