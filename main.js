// International format, digits only (no + or leading zero).
var WHATSAPP = '966555048914';
var CURRENCY = 'ر.س';

function waLink(text) {
  return 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(text);
}

function priceLabel(price) {
  return price ? 'السعر: ' + price + ' ' + CURRENCY : 'السعر عند الطلب';
}

document.querySelectorAll('[data-wa]').forEach(function (a) {
  a.href = waLink('مرحبًا M PACK، أرغب في الاستفسار عن منتجاتكم.');
  a.target = '_blank';
  a.rel = 'noopener';
});

var items = Array.prototype.slice.call(document.querySelectorAll('.item'));
var select = document.getElementById('s');

items.forEach(function (item) {
  var name = item.querySelector('h3').textContent;
  var price = item.dataset.price;

  var priceEl = document.createElement('div');
  priceEl.className = 'price' + (price ? '' : ' ask');
  priceEl.textContent = priceLabel(price);

  var btn = document.createElement('a');
  btn.className = 'btn wa';
  btn.href = waLink('مرحبًا M PACK، أرغب في طلب: ' + name + '\nالرجاء إرسال السعر والمقاسات المتوفرة.');
  btn.target = '_blank';
  btn.rel = 'noopener';
  btn.textContent = 'اطلب عبر واتساب';

  item.append(priceEl, btn);
  item.querySelector('.pic').addEventListener('click', function () { openLightbox(item); });

  select.add(new Option(name));
});
select.add(new Option('أخرى'));

document.querySelectorAll('.filters button').forEach(function (b) {
  b.addEventListener('click', function () {
    document.querySelector('.filters .on').classList.remove('on');
    b.classList.add('on');
    var f = b.dataset.filter;
    items.forEach(function (item) { item.hidden = f !== 'all' && item.dataset.cat !== f; });
  });
});

var lb = document.getElementById('lb');
var lastFocus = null;

function openLightbox(item) {
  var img = item.querySelector('img');
  document.getElementById('lb-img').src = img.src;
  document.getElementById('lb-img').alt = img.alt;
  document.getElementById('lb-title').innerHTML = item.querySelector('h3').innerHTML;
  document.getElementById('lb-desc').textContent = item.querySelector('p').textContent;
  var p = document.getElementById('lb-price');
  p.textContent = priceLabel(item.dataset.price);
  p.className = 'price' + (item.dataset.price ? '' : ' ask');
  document.getElementById('lb-wa').href = item.querySelector('.btn.wa').href;
  lastFocus = document.activeElement;
  lb.hidden = false;
  lb.querySelector('.lb-close').focus();
}

function closeLightbox() {
  lb.hidden = true;
  if (lastFocus) lastFocus.focus();
}

lb.addEventListener('click', function (e) { if (e.target === lb) closeLightbox(); });
lb.querySelector('.lb-close').addEventListener('click', closeLightbox);
document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) closeLightbox(); });

document.getElementById('order').addEventListener('submit', function (e) {
  e.preventDefault();
  var name = document.getElementById('n');
  if (!name.value.trim()) {
    name.classList.add('err');
    name.focus();
    return;
  }
  name.classList.remove('err');
  var lines = [
    'مرحبًا M PACK، أرغب في عرض سعر:',
    'الاسم: ' + name.value.trim(),
    'المنتج: ' + select.value
  ];
  var q = document.getElementById('q').value.trim();
  var m = document.getElementById('m').value.trim();
  if (q) lines.push('الكمية: ' + q);
  if (m) lines.push('التفاصيل: ' + m);
  window.open(waLink(lines.join('\n')), '_blank', 'noopener');
});

var menuBtn = document.querySelector('.menu-btn');
var menu = document.getElementById('menu');
menuBtn.addEventListener('click', function () {
  var open = menu.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded', open);
});
menu.addEventListener('click', function (e) {
  if (e.target.tagName === 'A') {
    menu.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }
});

var navLinks = Array.prototype.slice.call(menu.querySelectorAll('a'));
var spyTargets = navLinks.map(function (a) {
  var id = a.getAttribute('href').slice(1);
  return { link: a, el: id === 'top' ? null : document.getElementById(id) };
});

function updateActive() {
  var line = window.scrollY + window.innerHeight / 3;
  var current = spyTargets[0];
  spyTargets.forEach(function (t) {
    if (t.el && t.el.offsetTop <= line) current = t;
  });
  if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
    current = spyTargets[spyTargets.length - 1];
  }
  navLinks.forEach(function (a) { a.classList.toggle('active', a === current.link); });
}

var spyQueued = false;
window.addEventListener('scroll', function () {
  if (spyQueued) return;
  spyQueued = true;
  requestAnimationFrame(function () { spyQueued = false; updateActive(); });
}, { passive: true });
updateActive();

document.getElementById('yr').textContent = new Date().getFullYear();
