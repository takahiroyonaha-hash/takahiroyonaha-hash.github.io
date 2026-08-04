/* 電波がなくても遊べるようにするためのサービスワーカー。
   index.html を更新したら CACHE の版を上げる（古いキャッシュは自動で消える）。 */
const CACHE = 'ao-hiragana-v12';
const ASSETS = ['./', './index.html','./strokes.js', './manifest.webmanifest', './icon.svg', './icon-maskable.svg'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  // 版の確認だけは必ずネットワークを見る（キャッシュを返すと更新に気づけない）
  if (new URL(req.url).searchParams.has('fresh')) return;
  // まずキャッシュを返して即表示し、裏側で新しい版を取り込む
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit => {
      const fresh = fetch(req)
        .then(res => {
          if (res && res.ok && new URL(req.url).origin === location.origin) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy));
          }
          return res;
        })
        .catch(() => hit || caches.match('./index.html'));
      return hit || fresh;
    })
  );
});
