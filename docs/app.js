const ESTABLISHMENTS = {
  "Apartamentos Puerto Basella": {
    wifiName: "puertobasella",
    wifiPassword: "lobeira14",
    bookingUrl:
      "https://admin.booking.com/hotel/hoteladmin/extranet_ng/manage/search_reservations.html?upcoming_reservations=1&source=nav&hotel_id=260913&lang=es",
    messageSections: {
      es: {
        welcome:
          "En el salón hay una carpeta de color marrón que contiene información, sugerencias y recomendaciones de restaurantes y servicios en la zona.",
        cleaning:
          "Hay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, por si los necesitáis.",
        closing:
          "Cualquier cosa que necesitéis, decídmelo. Mañana por la mañana andará por ahí mi empleada Mary Carmen. Espero que paséis una buena estancia.",
        cider:
          "Os hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino blanco, sin escanciar. Espero que os guste.",
      },
      en: {
        welcome:
          "In the living room, there is a brown folder with useful information, suggestions, and recommendations for restaurants and services in the area.",
        cleaning:
          "There are cleaning supplies in a cupboard outside the apartment, next to the lift, in case you need them.",
        closing:
          "If you need anything, just let me know. My employee Mary Carmen will be around tomorrow morning. I hope you have a lovely stay.",
        cider:
          "We have left you a bottle of natural artisan cider, made in our village in the province of Lugo with apples from our own trees. Please drink it chilled, like a white wine, without pouring it from a height. I hope you enjoy it.",
      },
    },
    apartments: {
      "1A": { code: "9856" },
      "1B": { code: "6248" },
      "2A": { code: "6574" },
      "2B": { code: "2584" },
      "3A": { code: "2784" },
      "3B": { code: "7447" },
    },
    apartmentNotes: {
      es: {
        "1A":
          " También tenéis colchonetas para el mobiliario exterior dentro del apartamento en el cuarto de la lavandería.\nEl toldo de la pérgola se acciona con un mando a distancia que está en el salón. Tanto el toldo como los cojines rogamos se mantengan recogidos después de su uso, especialmente el toldo por la noche por seguridad.",
        "1B":
          " También tenéis colchonetas para el mobiliario exterior en un contenedor en la terraza.\nEl toldo de la pérgola se acciona con un mando a distancia que está en el salón. Tanto el toldo como los cojines rogamos se mantengan recogidos después de su uso, especialmente el toldo por la noche por seguridad.",
      },
      en: {
        "1A":
          " You will also find cushions for the outdoor furniture inside the apartment, in the laundry room.\nThe pergola awning is operated with a remote control, which is in the living room. Please make sure both the awning and the cushions are put away after use, especially the awning at night, for safety.",
        "1B":
          " You will also find cushions for the outdoor furniture in a storage box on the terrace.\nThe pergola awning is operated with a remote control, which is in the living room. Please make sure both the awning and the cushions are put away after use, especially the awning at night, for safety.",
      },
    },
  },
  "Apartamentos Autor": {
    wifiName: "puertobasella",
    wifiPassword: "a123b456",
    bookingUrl: "https://admin.booking.com/",
    messageSections: {
      es: {
        welcome:
          "En la mesa del salón tenéis una guía rápida con recomendaciones de playas, rutas y servicios de la zona.",
        cleaning:
          "Hay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, por si los necesitáis.",
        closing:
          "Si necesitáis cualquier ayuda durante la estancia, escribidme y os ayudo enseguida. ¡Disfrutad mucho de vuestras vacaciones!",
        cider:
          "Os hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino blanco, sin escanciar. Espero que os guste.",
      },
      en: {
        welcome:
          "On the living room table, you will find a quick guide with recommendations for beaches, walking routes, and local services.",
        cleaning:
          "There are cleaning supplies in a cupboard outside the apartment, next to the lift, in case you need them.",
        closing:
          "If you need any help during your stay, just send me a message and I will help you right away. Enjoy your holiday!",
        cider:
          "We have left you a bottle of natural artisan cider, made in our village in the province of Lugo with apples from our own trees. Please drink it chilled, like a white wine, without pouring it from a height. I hope you enjoy it.",
      },
    },
    apartments: {
      "1": { code: "3279" },
      "2": { code: "3480" },
      "3": { code: "7021" },
      "4": { code: "5676" },
    },
    apartmentNotes: { es: {}, en: {} },
  },
};

const form = document.querySelector("#messageForm");
const guestName = document.querySelector("#guestName");
const establishment = document.querySelector("#establishment");
const apartment = document.querySelector("#apartment");
const result = document.querySelector("#result");
const statusMessage = document.querySelector("#status");
const copyButton = document.querySelector("#copyButton");
const bookingButton = document.querySelector("#bookingButton");

function setStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.classList.toggle("error", isError);
}

function fillEstablishments() {
  establishment.replaceChildren(
    ...Object.keys(ESTABLISHMENTS).map((name) => new Option(name, name)),
  );
}

function fillApartments() {
  const selected = ESTABLISHMENTS[establishment.value];
  apartment.replaceChildren(
    new Option("Selecciona apartamento", ""),
    ...Object.keys(selected.apartments).map((name) => new Option(name, name)),
  );
}

function selectedCider() {
  return new FormData(form).get("cider");
}

function selectedLanguage() {
  return new FormData(form).get("language");
}

function generateMessage() {
  const name = guestName.value.trim();
  const establishmentName = establishment.value;
  const apartmentName = apartment.value;
  const language = selectedLanguage();

  if (!name) {
    setStatus("Introduce el nombre del huésped.", true);
    guestName.focus();
    return "";
  }

  if (!apartmentName) {
    setStatus("Selecciona apartamento.", true);
    apartment.focus();
    return "";
  }

  const establishmentData = ESTABLISHMENTS[establishmentName];
  const password = establishmentData.apartments[apartmentName]?.code ?? "";
  const specific = establishmentData.apartmentNotes[language][apartmentName] ?? "";
  const sections = establishmentData.messageSections[language];

  let message = "";

  if (language === "en") {
    message =
      `Hello ${name}, your apartment at ${establishmentName} is ${apartmentName}. ` +
      `You can enter with this code: ${password}✅. The same code also opens the main entrance using the black keypad. ` +
      `The Wi-Fi network is "${establishmentData.wifiName}" and the password is "${establishmentData.wifiPassword}".\n` +
      `${sections.welcome}\n` +
      `${sections.cleaning}${specific}\n` +
      sections.closing;
  } else {
    message =
      `Hola ${name} tu apartamento en ${establishmentName} es el ${apartmentName}. ` +
      `Entras con este código: ${password}✅, que también abre el portal utilizando el teclado negro. ` +
      `La wifi es "${establishmentData.wifiName}" y la contraseña es "${establishmentData.wifiPassword}".\n` +
      `${sections.welcome}\n` +
      `${sections.cleaning}${specific}\n` +
      sections.closing;
  }

  if (selectedCider() === "SI") {
    message += `\n${sections.cider}`;
  }

  setStatus("Mensaje generado.");
  return message;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = generateMessage();

  if (message) {
    result.value = message;
    result.focus();
    result.setSelectionRange(0, 0);
  }
});

establishment.addEventListener("change", () => {
  fillApartments();
  setStatus("");
});

copyButton.addEventListener("click", async () => {
  if (!result.value.trim()) {
    setStatus("Genera un mensaje antes de copiar.", true);
    return;
  }

  try {
    await navigator.clipboard.writeText(result.value);
    setStatus("Mensaje copiado al portapapeles.");
  } catch {
    result.focus();
    result.select();
    setStatus("Selecciona el texto y usa Copiar.", true);
  }
});

bookingButton.addEventListener("click", () => {
  const url = ESTABLISHMENTS[establishment.value].bookingUrl;
  window.open(url, "_blank", "noopener,noreferrer");
});

fillEstablishments();
fillApartments();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js");
  });
}
