# Tema de Blogger

El tema se genera a partir de la propuesta (`index.html`, `contacto.html`, `donar.html`, `styles.css`, `script.js`). Después de cambiar algo, regenerarlo:

```
python3 blogger/build.py
```

Genera:
- `tema-redherramientas.xml`: el tema.
- `paginas/contacto.html` y `paginas/donar.html`: el contenido de esas dos páginas.

Los estilos que solo se usan en Blogger (posteos, listados y ajustes) están en `blogger.css`.

## Instalación
1. **Copia de seguridad del tema actual:** Blogger → Tema → flecha junto a "Personalizar" → Copia de seguridad → Descargar.
2. **Subir el tema:** Tema → flecha → Restaurar → `tema-redherramientas.xml`. Si pregunta qué hacer con los gadgets del tema anterior, se pueden borrar.
3. **Página Contacto:** Páginas → "Contactanos" → vista HTML (ícono `<>`) → reemplazar todo por el contenido de `paginas/contacto.html`.
4. **Página Donar:** Páginas → Nueva página → título "Donar" (tiene que quedar en `/p/donar.html`) → vista HTML → pegar `paginas/donar.html`.
5. **Carrusel:** a los posteos que tienen que aparecer en el carrusel se les agrega la etiqueta `Carrusel`. Si ninguno la tiene, se muestran los últimos.

## Cómo se ve cada parte
- **Home:** el carrusel, Quiénes somos, los ejes, Novedades, Donar y la franja de contacto.
- **Posteos:** una tarjeta blanca con las etiquetas, el título, la fecha, el contenido y botones para compartir.
- **Etiquetas, búsquedas y archivo** (por ejemplo, los links de los ejes): una grilla de tarjetas con imagen, título y resumen, más "Más antiguas / Más nuevas".
- **Páginas** como Quiénes somos: el mismo formato que los posteos. Las que empiezan con `<div class="rh-full">`, como Contacto y Donar, se muestran a página completa.

## Editar la home sin tocar código
En Blogger → **Diseño**, cada sección de la home es un gadget HTML: Quiénes somos, Nuestros ejes, Novedades y Apoyá nuestro espacio. Se editan con el lápiz, y en el último bloque se pueden reordenar o agregar gadgets.

Ojo: si después se vuelve a subir el tema, puede que Blogger conserve el contenido editado o que lo reemplace por el de `index.html`. Conviene pasar los cambios también a `index.html`.

## Pendiente
- No probado todavía en Blogger: probarlo primero en un blog de prueba.
- Comentarios en los posteos: el tema no los muestra.
- Las imágenes de `donar.html` son las ilustraciones provisorias que están en GitHub Pages.
