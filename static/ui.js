(() => {
  const form = document.querySelector('[data-analysis-form]');
  if (!form) return;
  const submit = form.querySelector('[data-submit]');
  const loading = form.querySelector('[data-loading]');
  for (const panel of form.querySelectorAll('[data-input-panel]')) {
    const file = panel.querySelector('input[type=file]');
    const text = panel.querySelector('textarea');
    file.addEventListener('change', () => {
      if (file.files.length) { text.value = ''; panel.querySelector('details').open = false; }
    });
    text.addEventListener('input', () => { if (text.value.trim()) file.value = ''; });
  }
  let pending = false;
  const reset = () => { pending = false; submit.disabled = false; submit.innerHTML = 'Review invoice <span aria-hidden="true">→</span>'; loading.hidden = true; form.removeAttribute('aria-busy'); };
  window.addEventListener('pageshow', reset);
  form.addEventListener('submit', (event) => {
    if (pending) { event.preventDefault(); return; }
    if (!form.checkValidity()) return;
    pending = true; submit.disabled = true; submit.textContent = 'Reviewing…'; loading.hidden = false; form.setAttribute('aria-busy', 'true');
  });
})();
