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
      "2B": { code: "8784" },
      "3A": { code: "5321" },
      "3B": { code: "9476" },
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
        welcome: "",
        cleaning:
          "Hay artículos de limpieza en un armario fuera del apartamento, al lado del ascensor, por si los necesitáis.",
        closing:
          "Si necesitáis cualquier cosa durante la estancia, escribidme y os ayudo enseguida. ¡Disfrutad mucho de vuestro apartamento!",
        cider:
          "Os hemos dejado una sidra natural artesanal que elaboramos en nuestra aldea de la provincia de Lugo con nuestras propias manzanas. Tomadla fría, como si fuera un vino blanco, sin escanciar. Espero que os guste.",
      },
      en: {
        welcome: "",
        cleaning:
          "There are cleaning supplies in a cupboard outside the apartment, next to the lift, in case you need them.",
        closing:
          "If you need anything during your stay, just send me a message and I will help you right away. Enjoy your apartment!",
        cider:
          "We have left you a bottle of natural artisan cider, made in our village in the province of Lugo with apples from our own trees. Please drink it chilled, like a white wine, without pouring it from a height. I hope you enjoy it.",
      },
    },
    apartments: {
      "1": { code: "3279", wifiName: "Puerto Basella P1", wifiPassword: "a123b456" },
      "2": { code: "5972", wifiName: "PUERTO BASELLA", wifiPassword: "Lobeira14" },
      "3": { code: "7021" },
      "4": { code: "5676", wifiName: "TP-LINK_8D44", wifiPassword: "32288285" },
    },
    apartmentNotes: { es: {}, en: {} },
  },
};

const form = document.querySelector("#messageForm");
const guestName = document.querySelector("#guestName");
const establishment = document.querySelector("#establishment");
const apartmentOptions = document.querySelector("#apartmentOptions");
const result = document.querySelector("#result");
const statusMessage = document.querySelector("#status");
const copyButton = document.querySelector("#copyButton");
const whatsappButton = document.querySelector("#whatsappButton");
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
  apartmentOptions.replaceChildren(
    ...Object.keys(selected.apartments).map((name) => {
      const label = document.createElement("label");
      const input = document.createElement("input");
      const text = document.createElement("span");

      input.type = "checkbox";
      input.name = "apartments";
      input.value = name;
      text.textContent = name;
      label.append(input, text);

      return label;
    }),
  );
}

function selectedCider() {
  return new FormData(form).get("cider");
}

function selectedLanguage() {
  return new FormData(form).get("language");
}

function selectedApartments() {
  return new FormData(form).getAll("apartments");
}

function formatList(items, language) {
  if (items.length <= 1) {
    return items[0] ?? "";
  }

  const conjunction = language === "en" ? "and" : "y";
  return `${items.slice(0, -1).join(", ")} ${conjunction} ${items.at(-1)}`;
}

function formatCodeLines(apartments, establishmentData, language) {
  return apartments
    .map((apartmentName) => {
      const code = establishmentData.apartments[apartmentName]?.code ?? "";

      if (language === "en") {
        return `You can enter apartment ${apartmentName} with this code: ${code}✅.`;
      }

      return `Puedes entrar al apartamento ${apartmentName} con este código: ${code}✅.`;
    })
    .join("\n");
}

function formatApartmentNotes(apartments, notes) {
  return apartments
    .map((apartmentName) => notes[apartmentName] ?? "")
    .filter(Boolean)
    .join("\n");
}

function wifiForApartment(establishmentData, apartmentName) {
  const apartmentData = establishmentData.apartments[apartmentName] ?? {};

  return {
    apartmentName,
    name: apartmentData.wifiName ?? establishmentData.wifiName,
    password: apartmentData.wifiPassword ?? establishmentData.wifiPassword,
  };
}

function formatWifiText(apartments, establishmentData, language) {
  const wifiEntries = apartments.map((apartmentName) => wifiForApartment(establishmentData, apartmentName));
  const uniqueEntries = wifiEntries.filter((entry, index, entries) => {
    return entries.findIndex((other) => other.name === entry.name && other.password === entry.password) === index;
  });

  if (uniqueEntries.length === 1) {
    const { name, password } = uniqueEntries[0];

    if (language === "en") {
      return `The Wi-Fi network is "${name}" and the password is "${password}".`;
    }

    return `La wifi es "${name}" y la contraseña es "${password}".`;
  }

  if (language === "en") {
    return [
      "The Wi-Fi details are:",
      ...wifiEntries.map(
        ({ apartmentName, name, password }) =>
          `Apartment ${apartmentName}: network "${name}" and password "${password}".`,
      ),
    ].join("\n");
  }

  return [
    "Los datos de la wifi son:",
    ...wifiEntries.map(
      ({ apartmentName, name, password }) =>
        `Apartamento ${apartmentName}: red "${name}" y contraseña "${password}".`,
    ),
  ].join("\n");
}

function joinMessageParts(parts) {
  return parts.filter((part) => part.trim()).join("\n");
}

function generateMessage() {
  const name = guestName.value.trim();
  const establishmentName = establishment.value;
  const apartmentNames = selectedApartments();
  const language = selectedLanguage();

  if (!name) {
    setStatus("Introduce el nombre del huésped.", true);
    guestName.focus();
    return "";
  }

  if (apartmentNames.length === 0) {
    setStatus("Selecciona al menos un apartamento.", true);
    apartmentOptions.querySelector("input")?.focus();
    return "";
  }

  const establishmentData = ESTABLISHMENTS[establishmentName];
  const selectedList = formatList(apartmentNames, language);
  const codeLines = formatCodeLines(apartmentNames, establishmentData, language);
  const specific = formatApartmentNotes(apartmentNames, establishmentData.apartmentNotes[language]);
  const wifiText = formatWifiText(apartmentNames, establishmentData, language);
  const sections = establishmentData.messageSections[language];

  let message = "";

  if (language === "en") {
    const apartmentLabel = apartmentNames.length === 1 ? "apartment" : "apartments";
    const verb = apartmentNames.length === 1 ? "is" : "are";
    const entranceText =
      apartmentNames.length === 1
        ? "This code also opens the main entrance using the black keypad."
        : "These codes also open the main entrance using the black keypad.";

    message = joinMessageParts([
      `Hello ${name}, your ${apartmentLabel} at ${establishmentName} ${verb} ${selectedList}.\n\n` +
      `${codeLines}\n\n` +
      `${entranceText} ` +
      wifiText,
      sections.welcome,
      `${sections.cleaning}${specific}`,
      sections.closing,
    ]);
  } else {
    const apartmentLabel = apartmentNames.length === 1 ? "apartamento" : "apartamentos";
    const possessive = apartmentNames.length === 1 ? "tu" : "tus";
    const verb = apartmentNames.length === 1 ? "es" : "son";
    const entranceText =
      apartmentNames.length === 1
        ? "Este código también abre el portal utilizando el teclado negro."
        : "Estos códigos también abren el portal utilizando el teclado negro.";

    message = joinMessageParts([
      `Hola ${name}, ${possessive} ${apartmentLabel} en ${establishmentName} ${verb} ${selectedList}.\n\n` +
      `${codeLines}\n\n` +
      `${entranceText} ` +
      wifiText,
      sections.welcome,
      `${sections.cleaning}${specific}`,
      sections.closing,
    ]);
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

whatsappButton.addEventListener("click", () => {
  let message = result.value.trim();

  if (!message) {
    message = generateMessage();

    if (!message) {
      return;
    }

    result.value = message;
  }

  window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, "_blank", "noopener,noreferrer");
  setStatus("Abriendo WhatsApp.");
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
