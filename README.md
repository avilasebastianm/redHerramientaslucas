# Red de Herramientas Entre Mujeres — propuesta de home

Sitio simple en HTML, CSS y JavaScript (sin frameworks), con el diseño de la propuesta de Lucas y los cambios pedidos por la comisión (devolución del 28/9 y del 1/10).

- `index.html` — home
- `contacto.html` — página de contacto con formulario
- `donar.html` — página de donación: fotos de actividades y formas de donar (transferencia y depósito abren un modal)
- `img/` — ilustraciones provisorias de actividades (reemplazar por fotos reales)
- `styles.css` — estilos
- `script.js` — menú, tamaño de letra, carrusel, volver arriba y formulario

Para verlo: abrir `index.html` en el navegador.

## Configuración
- **Carrusel**: toma los posteos de redherramientas.com con la etiqueta `Carrusel` (si no hay, los últimos). Se cambia en `script.js` (`CAROUSEL_LABEL`).
- **Formulario**: envía a info@redherramientas.com con el asunto "WEB - SOLICITUD INFORMACIÓN" usando FormSubmit. El primer envío manda un mail de activación a esa casilla que hay que confirmar.

- **Datos para donar** (`donar.html`): reemplazar cada `<span class="pending" data-value="...">A completar</span>` por el dato, sin la clase `pending` (ej. `<span data-value="alias">red.herramientas</span>`). Al quitar `pending` aparece el botón "Copiar". Los links de Mercado Pago y PayPal están en `#pendiente-mercadopago` y `#pendiente-paypal`.

## Pendientes
- Datos de Mercado Pago, transferencia, PayPal y depósito, y texto de "Apoyá nuestro espacio" (los envía la comisión).
- Imágenes de los ejes (800 x 880 px, casi cuadradas) y link del eje Salud y Bienestar.
- Links de Lic Tips, Grabaciones, Drive y de las tarjetas de recursos.
