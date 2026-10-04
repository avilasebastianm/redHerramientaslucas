// Red de Herramientas Entre Mujeres — comportamiento del sitio

// ---------- Configuración ----------
var BLOG_URL = 'https://www.redherramientas.com';
var CAROUSEL_LABEL = 'Carrusel'; // etiqueta de Blogger para elegir los posteos del carrusel
var CAROUSEL_MAX = 6;
var CAROUSEL_DELAY = 5000;      // ms entre diapositivas

// Si el blog no responde, se muestran estas diapositivas
var FALLBACK_SLIDES = [
  {
    title: '¿Qué es #ClicSeguroEnRED?',
    text: ['Un nuevo espacio para adultas mayores enfocado en la prevención de estafas digitales.',
           'Los facilitadores somos también mujeres mayores, lo que conlleva la empatía necesaria para generar un clima de seguridad. Hablamos de autonomía tecnológica que les permita dejar de pedir ayuda para las tareas cotidianas relacionadas con la tecnología, como pedir un turno médico o escanear una receta.'],
    image: 'https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&q=80&w=1200',
    url: BLOG_URL
  },
  {
    title: 'Talleres de Sensibilización',
    text: ['Iniciamos nuestro ciclo de talleres presenciales para el buen uso del celular.',
           'Abordamos los temores comunes, cómo configurar contraseñas seguras y reconocer mensajes engañosos por WhatsApp o SMS.'],
    image: 'https://images.unsplash.com/photo-1581056771107-24ca5f033842?auto=format&fit=crop&q=80&w=1200',
    url: BLOG_URL
  }
];

// ---------- Header ----------
function setupHeader() {
  var header = document.querySelector('.header');
  var nav = document.getElementById('nav');
  var menuBtn = document.querySelector('.menu-btn');

  function updateHeaderHeight() {
    document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }
  updateHeaderHeight();
  window.addEventListener('resize', updateHeaderHeight);

  function closeMenu() {
    nav.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }

  menuBtn.addEventListener('click', function () {
    var isOpen = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(isOpen));
  });

  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') closeMenu();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });
}

// ---------- Tamaño de letra (como el menú de Lucas: Pequeña / Normal / Grande / Muy grande) ----------
function setupFontSize() {
  var toggle = document.querySelector('.font-size .icon-btn');
  var menu = document.querySelector('.font-size-menu');
  var options = menu.querySelectorAll('button');

  function apply(scale) {
    document.documentElement.style.fontSize = (scale * 100) + '%';
    options.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.scale === scale));
    });
    var header = document.querySelector('.header');
    document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }

  var saved = '1';
  try { saved = localStorage.getItem('font-scale') || '1'; } catch (e) {}
  apply(saved);

  toggle.addEventListener('click', function () {
    menu.hidden = !menu.hidden;
    toggle.setAttribute('aria-expanded', String(!menu.hidden));
  });

  options.forEach(function (b) {
    b.addEventListener('click', function () {
      apply(b.dataset.scale);
      try { localStorage.setItem('font-scale', b.dataset.scale); } catch (e) {}
      menu.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.font-size')) {
      menu.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// ---------- Volver arriba ----------
function setupToTop() {
  var btn = document.querySelector('.to-top');
  window.addEventListener('scroll', function () {
    btn.classList.toggle('show', window.scrollY > 500);
  });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ---------- Carrusel ----------
function setupCarousel() {
  var carousel = document.querySelector('.carousel');
  if (!carousel) return;

  var slidesEl = carousel.querySelector('.slides');
  var dotsEl = carousel.querySelector('.dots');
  var current = 0;
  var total = 0;
  var timer = null;
  var paused = false;

  function play() {
    stop();
    if (paused || total < 2) return;
    timer = setInterval(function () { goTo(current + 1); }, CAROUSEL_DELAY);
  }

  function stop() {
    clearInterval(timer);
  }

  function closeSlide(slide) {
    if (!slide || !slide.classList.contains('open')) return;
    slide.classList.remove('open');
    slide.querySelector('.slide-more').textContent = 'Ver más';
  }

  function goTo(index) {
    closeSlide(slidesEl.children[current]);
    current = (index + total) % total;
    slidesEl.style.transform = 'translateX(-' + (current * 100) + '%)';
    for (var i = 0; i < total; i++) {
      dotsEl.children[i].classList.toggle('active', i === current);
      slidesEl.children[i].setAttribute('aria-hidden', String(i !== current));
    }
    paused = false;
    play();
  }

  function makeSlide(item) {
    var slide = document.createElement('article');
    slide.className = 'slide';

    var media = document.createElement('a');
    media.className = 'slide-media';
    media.href = item.url;
    media.setAttribute('aria-label', 'Ver el posteo: ' + item.title);
    var blur = document.createElement('div');
    blur.className = 'blur';
    blur.style.backgroundImage = 'url("' + item.image + '")';
    var img = document.createElement('img');
    img.src = item.image;
    img.alt = '';
    media.appendChild(blur);
    media.appendChild(img);

    var box = document.createElement('div');
    box.className = 'slide-box';

    var title = document.createElement('h2');
    title.textContent = item.title;

    var desc = document.createElement('p');
    desc.className = 'slide-desc';
    desc.textContent = item.text[0];

    var full = document.createElement('div');
    full.className = 'slide-full';
    item.text.forEach(function (t) {
      var p = document.createElement('p');
      p.textContent = t;
      full.appendChild(p);
    });

    var actions = document.createElement('div');
    actions.className = 'slide-actions';

    var more = document.createElement('button');
    more.type = 'button';
    more.className = 'btn slide-more';
    more.textContent = 'Ver más';
    more.addEventListener('click', function () {
      var isOpen = slide.classList.toggle('open');
      more.textContent = isOpen ? 'Ver menos' : 'Ver más';
      paused = isOpen;
      if (isOpen) stop(); else play();
    });

    var link = document.createElement('a');
    link.className = 'btn btn-outline slide-link';
    link.href = item.url;
    link.textContent = 'Leer el posteo completo';

    actions.appendChild(more);
    actions.appendChild(link);
    box.appendChild(title);
    box.appendChild(desc);
    box.appendChild(full);
    box.appendChild(actions);
    slide.appendChild(media);
    slide.appendChild(box);
    return slide;
  }

  function render(items) {
    stop();
    slidesEl.innerHTML = '';
    dotsEl.innerHTML = '';
    total = items.length;
    current = 0;

    items.forEach(function (item, i) {
      slidesEl.appendChild(makeSlide(item));
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('aria-label', 'Ir a la actividad ' + (i + 1));
      dot.addEventListener('click', function () { goTo(i); });
      dotsEl.appendChild(dot);
    });

    carousel.querySelectorAll('.carousel-arrow, .dots').forEach(function (el) {
      el.style.display = total < 2 ? 'none' : '';
    });
    goTo(0);
  }

  carousel.querySelector('.prev').addEventListener('click', function () { goTo(current - 1); });
  carousel.querySelector('.next').addEventListener('click', function () { goTo(current + 1); });
  carousel.addEventListener('mouseenter', stop);
  carousel.addEventListener('mouseleave', play);

  render(FALLBACK_SLIDES);

  // Posteos del blog: primero los de la etiqueta del carrusel; si no hay, los últimos
  loadPosts(CAROUSEL_LABEL, function (posts) {
    if (posts.length) return render(posts);
    loadPosts('', function (latest) {
      if (latest.length) render(latest);
    });
  });
}

// Lee el feed de Blogger (JSONP: funciona dentro de Blogger y desde cualquier dominio)
function loadPosts(label, callback) {
  var name = 'blogFeed' + Date.now() + Math.floor(Math.random() * 1000);
  var script = document.createElement('script');
  var timeout = setTimeout(function () { finish([]); }, 8000);

  function finish(posts) {
    clearTimeout(timeout);
    window[name] = function () {};
    script.remove();
    callback(posts);
  }

  window[name] = function (data) { finish(parseFeed(data)); };
  script.onerror = function () { finish([]); };
  script.src = BLOG_URL + '/feeds/posts/default' +
    (label ? '/-/' + encodeURIComponent(label) : '') +
    '?alt=json-in-script&max-results=' + CAROUSEL_MAX + '&callback=' + name;
  document.head.appendChild(script);
}

function parseFeed(data) {
  var entries = (data && data.feed && data.feed.entry) || [];
  return entries.map(function (entry) {
    var html = (entry.content || entry.summary || {}).$t || '';
    var link = (entry.link || []).filter(function (l) { return l.rel === 'alternate'; })[0];
    var image = entry.media$thumbnail ? entry.media$thumbnail.url : '';
    if (!image) {
      var match = html.match(/<img[^>]+src="([^"]+)"/i);
      image = match ? match[1] : '';
    }
    // Las miniaturas vienen chicas (s72-c): se pide la versión de 1200px
    image = image.replace(/\/s\d+(-[a-z0-9-]+)?\//, '/w1200/').replace(/=s\d+(-[a-z0-9-]+)?$/, '=w1200');

    var text = htmlToText(html);
    return {
      title: entry.title.$t,
      text: text.length ? text : [entry.title.$t],
      image: image || 'https://i.imgur.com/CFM0Pcr.png',
      url: link ? link.href : BLOG_URL
    };
  });
}

function htmlToText(html) {
  html = html.replace(/<br\s*\/?>/gi, '\n').replace(/<\/(p|div|h\d|li)>/gi, '\n');
  var doc = new DOMParser().parseFromString(html, 'text/html');
  return (doc.body.textContent || '')
    .split('\n')
    .map(function (line) { return line.trim(); })
    .filter(function (line) { return line; });
}

// ---------- Formulario de contacto (FormSubmit → info@redherramientas.com) ----------
function setupContactForm() {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var msg = document.getElementById('form-msg');
  var button = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    button.disabled = true;
    msg.className = 'form-msg';
    msg.textContent = 'Enviando...';

    fetch('https://formsubmit.co/ajax/info@redherramientas.com', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (String(data.success) !== 'true') throw new Error(data.message);
        form.reset();
        msg.className = 'form-msg ok';
        msg.textContent = '¡Gracias! Recibimos tu mensaje y te vamos a responder a la brevedad.';
      })
      .catch(function () {
        msg.className = 'form-msg error';
        msg.textContent = 'No pudimos enviar el mensaje. Probá de nuevo o escribinos por WhatsApp.';
      })
      .finally(function () {
        button.disabled = false;
      });
  });
}

// ---------- Inicio ----------
setupHeader();
setupFontSize();
setupToTop();
setupCarousel();
setupContactForm();
