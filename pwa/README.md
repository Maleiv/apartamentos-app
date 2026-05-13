# Mensajes reservas PWA

Esta carpeta contiene una versión web instalable en iPhone sin usar App Store.

## Probar en local

Desde esta carpeta:

```powershell
python -m http.server 8080
```

Abre `http://localhost:8080` en el navegador del ordenador.

## Usar en iPhone

Para que iPhone permita instalarla bien, súbela a un hosting con HTTPS. Opciones gratuitas:

- GitHub Pages
- Netlify
- Cloudflare Pages

Después, en el iPhone:

1. Abre la URL en Safari.
2. Pulsa Compartir.
3. Pulsa Añadir a pantalla de inicio.

La app quedará como un icono normal y se abrirá a pantalla completa.
