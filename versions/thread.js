// The thread: fill the frame's left guide up to 60% of the viewport,
// and light each section's knot once the thread has reached it.
(function () {
  var frame = document.querySelector('.frame');
  if (!frame) return;
  var blocks = [].slice.call(frame.querySelectorAll('.block'));
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    frame.style.setProperty('--p', 1);
    blocks.forEach(function (b) { b.classList.add('lit'); });
    return;
  }
  var ticking = false;
  function update() {
    ticking = false;
    var r = frame.getBoundingClientRect(), mid = window.innerHeight * 0.6;
    var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
    frame.style.setProperty('--p', p.toFixed(4));
    blocks.forEach(function (b) { b.classList.toggle('lit', b.getBoundingClientRect().top < mid); });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
