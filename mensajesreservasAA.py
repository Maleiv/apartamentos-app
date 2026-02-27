import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess

def switch_to_PB():
    app.destroy()  # Close the current application
    subprocess.Popen(["python", "mensajesreservasPB.py"])  # Open Hotel B application

# Create the main application window
app = tk.Tk()

def generate_message():
    name = name_entry.get()
    ap = ap_var.get()
    password = keys.get(ap, "")
    special = sp_var.get()
    specific= ""
    if ap == "1A":
        specific = """ También tenéis colchonetas para el mobiliario exterior dentro del apartamento en el cuarto de la lavandería. 
        \nEl toldo de la pérgola se acciona con un mando a distancia que está en el salón. Tanto el toldo como los cojines rogamos se mantengan recogidos después de su uso, especialmente el toldo por la noche por seguridad."""
    elif ap == "1B":
        specific = """ También tenéis colchonetas para el mobiliario exterior en un contenedor en la terraza. 
        \nEl toldo de la pérgola se acciona con un mando a distancia que está en el salón. Tanto el toldo como los cojines rogamos se mantengan recogidos después de su uso, especialmente el toldo por la noche por seguridad."""

    message = f"""Hola {name} tu apartamento es el {ap}. Entras con este código: {password}✅, que también abre el portal utilizando el teclado negro. La wifi es cualquiera de las "puertobasella" y la contraseña es "lobeira14".
    \nEn el salón hay una carpeta de color marrón que contiene información, sugerencias y recomendaciones de restaurantes y servicios en la zona.
    \nHay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, por si los necesitáis.{specific}
    \nCualquier cosa que necesitéis, decídmelo. Mañana por la mañana andará por ahí mi empleada Mary Carmen. Espero que paséis una buena estancia.
    """
    if special == "SI":
        message += "\nOs hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino blanco, sin escanciar. Espero que os guste."
    if ap != "Selecciona apartamento":
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, message)
    else:
         messagebox.showwarning("Error", "Selecciona apartamento", parent=app)

def copy_to_clipboard():
    app.clipboard_clear()
    app.clipboard_append(result_text.get("1.0", tk.END))
    app.update()  # Ensures the clipboard contents are updated
    messagebox.showinfo("Info", "Mensaje copiado al portapapeles!", parent=app)

def open_booking_messages():
    booking_messages_url = "https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/search_reservations.html?upcoming_reservations=1&source=nav&hotel_id=260913&lang=es"  # Update with the correct URL if needed
    webbrowser.open(booking_messages_url)

tk.Label(app, text="Nombre:").pack(pady=5)
name_entry = tk.Entry(app)
name_entry.pack(pady=5)

# Create input fields for floor and door number
tk.Label(app, text="Apartamento:").pack(pady=6)
ap_var = tk.StringVar(value="Selecciona apartamento")  # Default value
ap_options = ["1A", "1B", "2A", "2B", "3A", "3B"]
floor_menu = tk.OptionMenu(app, ap_var, *ap_options)
floor_menu.pack(pady=6)

# Create input fields for special option
tk.Label(app, text="Sidra:").pack(pady=6)
sp_var = tk.StringVar(value="NO")  # Default value
sp_options = ["SI", "NO"]
floor_menu = tk.OptionMenu(app, sp_var, *sp_options)
floor_menu.pack(pady=5)

# Generate message button
tk.Button(app, text="Generar mensaje", command=generate_message).pack(pady=10)

# Set the window title
app.title("Auto mensajes apartamentos")

# Set the window size (optional)
app.geometry("800x600")  # Width x Height

# Create a label and entry field to display the generated message
tk.Label(app, text="Mensaje generado:").pack(pady=5)
result_text = tk.Text(app, height=14, width=90)
result_text.pack(pady=5)

# Create a frame for the two buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=10)

# Copy to clipboard button
tk.Button(button_frame, text="Copiar mensaje", command=copy_to_clipboard).pack(side="left", padx=5)

# Open Booking.com messages button
tk.Button(button_frame, text="Abrir mensajes en Booking", command=open_booking_messages).pack(side="right", padx=5)

keys = {
    "1A": "9856",
    "1B": "6248",
    "2A": "6574",
    "2B": "2584",
    "3A": "2784",
    "3B": "7447",
}

# Start the Tkinter event loop
app.mainloop()