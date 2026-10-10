#!/usr/bin/env python3
"""Arma el tema de Blogger y las páginas a partir de la propuesta (index.html, contacto.html, donar.html, styles.css, script.js).

Uso:  python3 blogger/build.py
Genera:
  blogger/tema-redherramientas.xml   -> Tema > Restaurar
  blogger/paginas/contacto.html      -> contenido (vista HTML) de la página Contacto
  blogger/paginas/donar.html         -> contenido (vista HTML) de la página Donar
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

# Direcciones de las páginas estáticas en Blogger
CONTACT_URL = '/p/contactanos.html'   # la página que ya existe
DONATE_URL = '/p/donar.html'          # página nueva "Donar"
# Ilustraciones provisorias de la página de donar (reemplazar por fotos subidas a Blogger)
IMG_BASE = 'https://avilasebastianm.github.io/redHerramientaslucas/img/'


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


def links(s):
    """Adapta los links de la propuesta a las direcciones de Blogger."""
    s = s.replace('href="index.html"', 'href="/"').replace('href="index.html#', 'href="/#')
    for anchor in ('quienes-somos', 'actividades'):
        s = s.replace('href="#%s"' % anchor, 'href="/#%s"' % anchor)
    s = s.replace('href="contacto.html"', 'href="%s"' % CONTACT_URL)
    s = s.replace('href="donar.html"', 'href="%s"' % DONATE_URL)
    s = s.replace('src="img/', 'src="' + IMG_BASE)
    return s


def xhtml(s):
    """HTML -> XHTML para las partes fijas del tema (Blogger exige XML bien formado)."""
    s = s.replace('&times;', '&#215;')
    s = re.sub(r'&(?!(amp|lt|gt|quot|apos|#\d+);)', '&amp;', s)

    def fix_tag(m):
        tag = m.group(0)
        if tag.startswith('<!--') or tag.startswith('</'):
            return tag
        tag = re.sub(r'\s(hidden|required|novalidate|disabled)(?=[\s>/])', r' \1="\1"', tag)
        if re.match(r'<(img|input|br|meta|link|hr|source)\b', tag) and not tag.endswith('/>'):
            tag = tag[:-1].rstrip() + '/>'
        return tag

    return re.sub(r'<!--.*?-->|<[^>]+>', fix_tag, s, flags=re.S)


def cdata(s):
    assert ']]>' not in s
    return '<![CDATA[' + s + ']]>'


index = read('index.html')
contacto = read('contacto.html')
donar = read('donar.html')

# ---------- Partes de la home ----------
header = xhtml(links(between(index, '<header class="header">', '</header>') + '</header>'))
carousel = xhtml(between(index, '    <!-- Carrusel de actividades', '    <!-- Mini sección Quiénes somos'))
about = links(between(index, '    <!-- Mini sección Quiénes somos', '    <!-- Nuestros ejes'))
ejes = links(between(index, '    <!-- Nuestros ejes', '    <div class="container">\n      <div class="separator">'))
middle = between(index, '    <div class="container">\n      <div class="separator">', '    <!-- Llamado a la página de contacto')
# novedades y donar: cada uno con su barra separadora
chunks = middle.split('<div class="separator"></div>')[1:]
chunks[-1] = chunks[-1].rsplit('</div>', 1)[0]  # cierre del .container
blocks = [links('      <div class="separator"></div>' + c.rstrip() + '\n') for c in chunks]
contact_cta = xhtml(links(between(index, '    <!-- Llamado a la página de contacto', '  </main>')))
footer = xhtml(between(index, '  <footer class="footer">', '  <script'))

# Gadgets editables desde Diseño (ids altos para no pisar los gadgets del tema anterior)
home_widgets = [
    ('home-quienes', 'HTML101', 'Quiénes somos', about),
    ('home-ejes', 'HTML102', 'Nuestros ejes', ejes),
]
home_container_widgets = [
    ('HTML105', 'Novedades', blocks[0]),
    ('HTML106', 'Apoyá nuestro espacio (Donar)', blocks[1]),
]


def html_widget(wid, title, content):
    return f"""<b:widget id='{wid}' locked='false' title='{title}' type='HTML' version='2' visible='true'>
  <b:widget-settings>
    <b:widget-setting name='content'>{cdata(content)}</b:widget-setting>
  </b:widget-settings>
  <b:includable id='main'><data:content/></b:includable>
</b:widget>"""


home_html = ''
for sid, wid, title, content in home_widgets:
    home_html += f"<b:section class='home-section' id='{sid}' maxwidgets='1' showaddelement='no'>\n{html_widget(wid, title, content)}\n</b:section>\n"
home_html += "<div class='container'>\n<b:section class='home-section' id='home-bloques' showaddelement='yes'>\n"
home_html += '\n'.join(html_widget(w, t, c) for w, t, c in home_container_widgets)
home_html += "\n</b:section>\n</div>\n"

# ---------- Posteos, etiquetas y búsquedas ----------
blog_widget = """<b:section class='main' id='main' maxwidgets='1' showaddelement='no'>
<b:widget id='Blog1' locked='true' title='Entradas del blog' type='Blog' version='2' visible='true'>
<b:includable id='main' var='this'>
  <b:if cond='data:view.isSingleItem'>
    <b:loop values='data:posts' var='post'>
      <b:if cond='data:view.isPage and (data:post.body contains &quot;rh-full&quot;)'>
        <!-- Páginas armadas con el diseño del sitio (Contacto, Donar): van completas -->
        <data:post.body/>
      <b:else/>
        <article class='post-page'>
          <div class='container narrow'>
            <a class='post-back' expr:href='data:blog.homepageUrl'>&#8592; Volver al inicio</a>
            <b:if cond='data:post.labels'>
              <div class='post-labels'>
                <b:loop values='data:post.labels' var='label'><a class='chip-label' expr:href='data:label.url'><data:label.name/></a></b:loop>
              </div>
            </b:if>
            <h1 class='post-title'><b:eval expr='data:post.title ? data:post.title : &quot;Sin título&quot;'/></h1>
            <b:if cond='data:view.isPost'><p class='post-date'><data:post.date/></p></b:if>
            <div class='post-body'><data:post.body/></div>
            <b:if cond='data:view.isPost'>
              <div class='post-share'>
                <span>Compartir:</span>
                <a class='share-btn share-wa' expr:href='&quot;https://wa.me/?text=&quot; + data:post.url.canonical' rel='noopener' target='_blank'>WhatsApp</a>
                <a class='share-btn share-fb' expr:href='&quot;https://www.facebook.com/sharer.php?u=&quot; + data:post.url.canonical' rel='noopener' target='_blank'>Facebook</a>
              </div>
            </b:if>
          </div>
        </article>
      </b:if>
    </b:loop>
  <b:elseif cond='!data:view.isHomepage'/>
    <section class='list-page'>
      <div class='container'>
        <h1 class='section-title list-title'>
          <b:if cond='data:view.search.label'><data:view.search.label/>
          <b:elseif cond='data:view.search.query'/>Resultados para &#8220;<data:view.search.query/>&#8221;
          <b:elseif cond='data:view.isArchive'/><data:view.archive.rangeMessage/>
          <b:else/>Publicaciones</b:if>
        </h1>
        <b:if cond='data:posts.empty'><p class='list-empty'>No encontramos publicaciones.</p></b:if>
        <div class='post-grid'>
          <b:loop values='data:posts' var='post'>
            <a class='post-card' expr:href='data:post.url'>
              <div class='post-card-img'>
                <b:if cond='data:post.featuredImage'>
                  <img expr:alt='data:post.title' expr:src='resizeImage(data:post.featuredImage, 640, &quot;4:3&quot;)' loading='lazy'/>
                <b:else/>
                  <img alt='' class='no-img' src='https://i.imgur.com/CFM0Pcr.png'/>
                </b:if>
              </div>
              <div class='post-card-body'>
                <b:if cond='data:post.labels'><span class='chip-label'><data:post.labels.first.name/></span></b:if>
                <h2><b:eval expr='data:post.title ? data:post.title : &quot;Sin título&quot;'/></h2>
                <p class='post-card-date'><data:post.date/></p>
                <p class='post-card-snippet'><data:post.snippets.short/></p>
                <span class='post-card-more'>Leer más &#8594;</span>
              </div>
            </a>
          </b:loop>
        </div>
        <nav class='pager' aria-label='Más publicaciones'>
          <b:if cond='data:newerPageUrl'><a class='btn btn-light' expr:href='data:newerPageUrl'>&#8592; Más nuevas</a></b:if>
          <b:if cond='data:olderPageUrl'><a class='btn' expr:href='data:olderPageUrl'>Más antiguas &#8594;</a></b:if>
        </nav>
      </div>
    </section>
  </b:if>
</b:includable>
</b:widget>
</b:section>"""

css = read('styles.css') + '\n' + (OUT / 'blogger.css').read_text(encoding='utf-8')
js = read('script.js')
assert '</script' not in js and ']]>' not in js and ']]>' not in css

theme = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<!-- Tema de Red de Herramientas Entre Mujeres. Generado con blogger/build.py: no editar a mano. -->
<html b:css='false' b:defaultwidgetversion='2' b:layoutsVersion='3' b:responsive='true' b:templateVersion='1.0.0' expr:dir='data:blog.languageDirection' lang='es-AR' xmlns='http://www.w3.org/1999/xhtml' xmlns:b='http://www.google.com/2005/gml/b' xmlns:data='http://www.google.com/2005/gml/data' xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
<meta content='width=device-width, initial-scale=1' name='viewport'/>
<b:include data='blog' name='all-head-content'/>
<title><b:if cond='data:view.isHomepage'><data:blog.title.escaped/><b:else/><data:view.title.escaped/> | <data:blog.title.escaped/></b:if></title>
<link href='https://fonts.googleapis.com' rel='preconnect'/>
<link href='https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700;900&amp;display=swap' rel='stylesheet'/>
<b:skin version='1.0.0'><![CDATA[/* Los estilos están en el <style> de abajo */]]></b:skin>
<b:template-skin><![CDATA[
body#layout .carousel, body#layout .to-top {{ display: none; }}
body#layout .header {{ position: static; }}
]]></b:template-skin>
<style>/*<![CDATA[*/
{css}
/*]]>*/</style>
</head>
<body>
<a class='skip' href='#contenido'>Saltar al contenido</a>

{header}

<main id='contenido'>
<b:if cond='data:view.isHomepage'>
{carousel}
{home_html}
</b:if>

{blog_widget}

<b:if cond='data:view.isHomepage'>
{contact_cta}
</b:if>
</main>

{footer}
<script>//<![CDATA[
{js}
//]]></script>
</body>
</html>
"""

# El tema tiene que ser XML válido o Blogger lo rechaza
ET.fromstring(theme.split('\n', 1)[1].replace('<!DOCTYPE html>', '', 1).encode('utf-8'))
(OUT / 'tema-redherramientas.xml').write_text(theme, encoding='utf-8')

# ---------- Páginas estáticas ----------
pages = OUT / 'paginas'
pages.mkdir(exist_ok=True)
contact_body = between(contacto, '  <main id="contenido">', '  </main>').replace('  <main id="contenido">', '', 1)
(pages / 'contacto.html').write_text('<div class="rh-full">\n' + links(contact_body) + '</div>\n', encoding='utf-8')
donate_body = between(donar, '  <main id="contenido">', '  <footer').replace('  <main id="contenido">', '', 1).replace('  </main>\n', '', 1)
(pages / 'donar.html').write_text('<div class="rh-full">\n' + links(donate_body) + '</div>\n', encoding='utf-8')

print('Listo:', (OUT / 'tema-redherramientas.xml').relative_to(ROOT), '+', ', '.join(str(p.relative_to(ROOT)) for p in sorted(pages.iterdir())))
