(async () => {
  await new Promise(r => window.addEventListener('load', r));
  document.querySelector('code').textContent =
    `${window.origin}/cowsay/{message}`;
})();
