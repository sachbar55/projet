const API = '/api/products';
const AUTOPLAY_INTERVAL = 3000; // 3 secondes

// ===== Load & render products =====
async function loadProducts() {
  const res = await fetch(API);
  const products = await res.json();
  renderProducts(products);
}

function renderProducts(products) {
  const grid = document.getElementById('products-grid');
  grid.innerHTML = '';

  if (products.length === 0) {
    grid.innerHTML = '<p style="color:#888">Aucun produit pour le moment.</p>';
    return;
  }

  products.forEach(product => {
    grid.appendChild(createCard(product));
  });
}

// ===== Product Card with Carousel =====
function createCard(product) {
  const card = document.createElement('div');
  card.className = 'product-card';

  const photos = product.photos || [];
  const hasMultiple = photos.length > 1;

  // Carousel
  const carousel = document.createElement('div');
  carousel.className = 'carousel';

  const track = document.createElement('div');
  track.className = 'carousel-track';
  photos.forEach(src => {
    const img = document.createElement('img');
    img.src = src;
    img.alt = product.name;
    img.loading = 'lazy';
    track.appendChild(img);
  });
  carousel.appendChild(track);

  let currentIndex = 0;
  let autoplayTimer = null;

  function goTo(index) {
    if (photos.length === 0) return;
    currentIndex = ((index % photos.length) + photos.length) % photos.length;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;
    updateDots();
  }

  function next() { goTo(currentIndex + 1); }
  function prev() { goTo(currentIndex - 1); }

  // Auto-play
  function startAutoplay() {
    stopAutoplay();
    if (hasMultiple) {
      autoplayTimer = setInterval(next, AUTOPLAY_INTERVAL);
    }
  }
  function stopAutoplay() {
    if (autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; }
  }

  // Arrows (manual navigation)
  if (hasMultiple) {
    const prevBtn = document.createElement('button');
    prevBtn.className = 'carousel-btn prev';
    prevBtn.textContent = '‹';
    prevBtn.addEventListener('click', () => { prev(); startAutoplay(); });

    const nextBtn = document.createElement('button');
    nextBtn.className = 'carousel-btn next';
    nextBtn.textContent = '›';
    nextBtn.addEventListener('click', () => { next(); startAutoplay(); });

    carousel.appendChild(prevBtn);
    carousel.appendChild(nextBtn);
  }

  // Dots
  const dotsContainer = document.createElement('div');
  dotsContainer.className = 'carousel-dots';

  function updateDots() {
    dotsContainer.querySelectorAll('.carousel-dot').forEach((dot, i) => {
      dot.classList.toggle('active', i === currentIndex);
    });
  }

  if (hasMultiple) {
    photos.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
      dot.addEventListener('click', () => { goTo(i); startAutoplay(); });
      dotsContainer.appendChild(dot);
    });
    carousel.appendChild(dotsContainer);
  }

  // Pause on hover, resume on leave
  carousel.addEventListener('mouseenter', stopAutoplay);
  carousel.addEventListener('mouseleave', startAutoplay);

  card.appendChild(carousel);

  // Card body
  const body = document.createElement('div');
  body.className = 'card-body';
  body.innerHTML = `
    <h3>${escapeHtml(product.name)}</h3>
    <p class="description">${escapeHtml(product.description)}</p>
    <p class="price">${Number(product.price).toFixed(2)} €</p>
  `;
  card.appendChild(body);

  // Actions
  const actions = document.createElement('div');
  actions.className = 'card-actions';

  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'btn-delete';
  deleteBtn.textContent = 'Supprimer';
  deleteBtn.addEventListener('click', async () => {
    if (!confirm('Supprimer ce produit ?')) return;
    await fetch(`${API}/${product.id}`, { method: 'DELETE' });
    loadProducts();
  });
  actions.appendChild(deleteBtn);
  card.appendChild(actions);

  // Start auto-slide
  startAutoplay();

  return card;
}

// ===== Form: add product =====
const form = document.getElementById('product-form');
const photosInput = document.getElementById('form-photos');
const preview = document.getElementById('photo-preview');

photosInput.addEventListener('change', () => {
  preview.innerHTML = '';
  Array.from(photosInput.files).forEach(file => {
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    preview.appendChild(img);
  });
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append('name', document.getElementById('form-name').value);
  formData.append('description', document.getElementById('form-desc').value);
  formData.append('price', document.getElementById('form-price').value);

  Array.from(photosInput.files).forEach(file => {
    formData.append('photos', file);
  });

  const res = await fetch(API, { method: 'POST', body: formData });

  if (res.ok) {
    form.reset();
    preview.innerHTML = '';
    loadProducts();
  } else {
    alert('Erreur lors de l\'ajout du produit');
  }
});

// ===== Helpers =====
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

// ===== Init =====
loadProducts();
