/* MarketPro – Admin JavaScript */

// ── Sidebar Toggle ────────────────────────────────────────────────
function toggleSidebar() {
  const sidebar = document.getElementById('adminSidebar');
  const main = document.getElementById('adminMain');
  if (!sidebar) return;

  const isMobile = window.innerWidth <= 768;
  if (isMobile) {
    sidebar.classList.toggle('open');
    // Overlay
    let overlay = document.getElementById('sidebarOverlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'sidebarOverlay';
      overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:99;';
      overlay.onclick = toggleSidebar;
      document.body.appendChild(overlay);
    }
    if (sidebar.classList.contains('open')) {
      overlay.style.display = 'block';
    } else {
      overlay.style.display = 'none';
    }
  } else {
    sidebar.classList.toggle('collapsed');
    if (main) main.classList.toggle('expanded');
  }
}

// ── Auto-dismiss Flash Messages ───────────────────────────────────
(function () {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity .4s ease';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 400);
    }, 4500);
  });
})();

// ── Confirm delete buttons ────────────────────────────────────────
document.querySelectorAll('form[onsubmit]').forEach(form => {
  // handled inline
});

// ── Table row highlight ───────────────────────────────────────────
document.querySelectorAll('.admin-table tbody tr').forEach(row => {
  row.style.cursor = 'default';
});
