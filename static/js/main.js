/* MarketPro – Main JavaScript */

// ── Navbar Scroll Effect ─────────────────────────────────────────
(function () {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
})();

// ── Mobile Nav Toggle ────────────────────────────────────────────
(function () {
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('navMenu');
  if (!toggle || !menu) return;
  toggle.addEventListener('click', () => {
    menu.classList.toggle('open');
    const spans = toggle.querySelectorAll('span');
    const open = menu.classList.contains('open');
    if (open) {
      spans[0].style.cssText = 'transform:rotate(45deg) translate(5px,5px)';
      spans[1].style.opacity = '0';
      spans[2].style.cssText = 'transform:rotate(-45deg) translate(5px,-5px)';
    } else {
      spans.forEach(s => { s.style.cssText = ''; });
    }
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!toggle.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('open');
      toggle.querySelectorAll('span').forEach(s => { s.style.cssText = ''; });
    }
  });
})();

// ── Search Bar Toggle ────────────────────────────────────────────
(function () {
  const toggle = document.getElementById('searchToggle');
  const bar = document.getElementById('searchBar');
  if (!toggle || !bar) return;
  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    bar.classList.toggle('open');
    if (bar.classList.contains('open')) {
      const input = bar.querySelector('input');
      if (input) setTimeout(() => input.focus(), 100);
    }
  });
})();

// ── Intersection Observer – Animate Cards ────────────────────────
(function () {
  const cards = document.querySelectorAll('.product-card, .category-card, .feature-card');
  if (!cards.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = parseInt(entry.target.dataset.delay || 0);
        setTimeout(() => {
          entry.target.classList.add('animated');
        }, delay);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  cards.forEach(card => observer.observe(card));
})();

// ── Auto-dismiss Flash Messages ───────────────────────────────────
(function () {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity .5s ease, transform .5s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(40px)';
      setTimeout(() => flash.remove(), 500);
    }, 4000);
  });
})();

// ── Hero Counter Animation ────────────────────────────────────────
(function () {
  const numbers = document.querySelectorAll('.hero-stat-number');
  if (!numbers.length) return;

  const animateCount = (el) => {
    const target = parseInt(el.textContent.replace(/\D/g, ''));
    if (!target) return;
    const suffix = el.textContent.replace(/[\d]/g, '');
    let current = 0;
    const step = Math.ceil(target / 40);
    const interval = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current + suffix;
      if (current >= target) clearInterval(interval);
    }, 30);
  };

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  numbers.forEach(n => observer.observe(n));
})();

// ── Smooth scroll for anchor links ───────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const navH = document.getElementById('navbar')?.offsetHeight || 70;
      const y = target.getBoundingClientRect().top + window.scrollY - navH - 16;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  });
});
