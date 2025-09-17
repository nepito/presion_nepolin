// sw.js
self.addEventListener('install', (event) => {
  console.log('Service Worker instalado');
});

self.addEventListener('fetch', (event) => {
  // Puedes dejar esto vacío o agregar lógica para cachear recursos
});