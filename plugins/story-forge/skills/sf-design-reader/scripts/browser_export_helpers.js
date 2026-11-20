// Browser export helpers: export design screens from Figma's web app, inside the
// app browser, with the user's own session. Inject the WHOLE file with the
// page-script tool in the Figma tab, once per page load. Nothing is downloaded
// to the computer: export blobs are captured in the page.
//
// Typical use (one page-script call per line):
//   await __list()                          -> [[id, name], ...] of the selected section (press Enter first)
//   __batch([["01-step1", "123:456"], ...])  -> starts in the background; do not await
//   __progress()                            -> {done, total, finished, errors, formatChanged}
//   __fetch("01-step1")                     -> '@@01-step1@@<base64>'  (ONE key per call)
// Spanish names (__listar, __lote, __avance, __traer) remain as aliases.
//
// Fragility: relies on Figma's web UI (layer-panel test ids, export combobox,
// "Export"/"Exportar" button). Update the selectors when the UI changes.
(() => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  window.__out = window.__out || {};
  window.__err = window.__err || {};

  if (!window.__via3) {
    window.__caps = [];
    window.__dl = [];
    const crear = URL.createObjectURL.bind(URL);
    URL.createObjectURL = function (o) {
      const u = crear(o);
      if (o instanceof Blob) window.__caps.push({ url: u, blob: o, t: Date.now() });
      return u;
    };
    const clickOriginal = HTMLAnchorElement.prototype.click;
    HTMLAnchorElement.prototype.click = function () {
      if (this.hasAttribute('download')) {
        window.__dl.push(this.getAttribute('download'));
        return; // do not download to the computer
      }
      return clickOriginal.call(this);
    };
    window.__via3 = true;
  }

  const FILA = '[data-testid$="-layers-panel-row"]';
  const idDeFila = (r) => r.getAttribute('data-testid').replace(/-layers-panel-row$/, '');
  const norm = (id) => String(id).replace(/[-:]/g, ':');

  const panel = () => {
    const r = document.querySelector(FILA);
    let e = r && r.parentElement;
    while (e && !(e.scrollHeight > e.clientHeight + 10 && getComputedStyle(e).overflowY !== 'visible')) e = e.parentElement;
    return e;
  };

  // Walk the (virtualized) layer panel and return [id, name] without notes or connectors.
  window.__listar = async () => {
    const p = panel();
    const vistos = new Map();
    if (!p) return [];
    p.scrollTop = 0;
    await sleep(300);
    for (let i = 0; i < 500; i++) {
      document.querySelectorAll(FILA).forEach((r) => {
        const id = idDeFila(r);
        if (!vistos.has(id)) vistos.set(id, (r.innerText || '').trim().split('\n')[0]);
      });
      const antes = p.scrollTop;
      p.scrollTop += p.clientHeight * 0.8;
      await sleep(200);
      if (p.scrollTop === antes) break;
    }
    window.__layers = [...vistos].filter(([, n]) => !/^(note|flow connector|\.)$/i.test(n));
    return window.__layers;
  };

  // Select a layer by id (scrolls the panel when the row is not rendered).
  window.__sel = async (id) => {
    const buscar = () => [...document.querySelectorAll(FILA)].find((r) => norm(idDeFila(r)) === norm(id));
    let r = buscar();
    const p = panel();
    if (!r && p) {
      p.scrollTop = 0;
      for (let i = 0; i < 500 && !r; i++) {
        await sleep(150);
        r = buscar();
        if (r) break;
        const antes = p.scrollTop;
        p.scrollTop += p.clientHeight * 0.8;
        if (p.scrollTop === antes) break;
      }
    }
    if (!r) throw new Error('layer row not found: ' + id);
    r.scrollIntoView({ block: 'center' });
    await sleep(150);
    for (const t of ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click']) {
      r.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window, button: 0 }));
    }
    await sleep(600);
    const actual = new URL(location.href).searchParams.get('node-id');
    if (!actual || norm(actual) !== norm(id)) throw new Error('selection did not change to ' + id + ' (current ' + actual + ')');
    return true;
  };

  // Set the export format to PNG (changes the frame's export setting if it was another one).
  window.__png = async () => {
    const combo = [...document.querySelectorAll('[role="combobox"]')].find((c) => /^(PDF|PNG|JPG|SVG)$/i.test((c.innerText || '').trim()));
    if (!combo) throw new Error('no export setting: add one in the Export panel');
    if (/^PNG$/i.test(combo.innerText.trim())) return 'PNG';
    window.__formatoCambiado = (window.__formatoCambiado || []).concat(new URL(location.href).searchParams.get('node-id'));
    combo.click();
    await sleep(400);
    const opcion = [...document.querySelectorAll('[role="option"]')].find((o) => /^PNG$/i.test((o.innerText || '').trim()));
    if (!opcion) throw new Error('PNG option did not appear');
    opcion.click();
    await sleep(400);
    return 'changed to PNG';
  };

  const aBase64 = (blob) => new Promise((ok, mal) => {
    const fr = new FileReader();
    fr.onload = () => ok(String(fr.result).split(',')[1]);
    fr.onerror = mal;
    fr.readAsDataURL(blob);
  });

  // Click "Export …"/"Exportar …" and store the new blob in __out[key].
  window.__exp = async (clave) => {
    const boton = [...document.querySelectorAll('button')].find((b) => /^(Exportar|Export) /.test((b.innerText || '').trim()));
    if (!boton) throw new Error('Export button not found');
    const n = window.__caps.length;
    boton.click();
    for (let i = 0; i < 100 && window.__caps.length === n; i++) await sleep(200);
    if (window.__caps.length === n) throw new Error('export produced no image');
    window.__out[clave] = await aBase64(window.__caps[window.__caps.length - 1].blob);
    return window.__out[clave].length;
  };

  // Export a list [[key, id], ...] in the background. Poll with __progress().
  window.__lote = (lista) => {
    window.__total = lista.length;
    (async () => {
      for (const [clave, id] of lista) {
        if (window.__out[clave]) continue;
        try {
          await window.__sel(id);
          await window.__png();
          await window.__exp(clave);
        } catch (e) {
          window.__err[clave] = String(e.message || e);
        }
      }
      window.__terminado = true;
    })();
    return 'started: ' + lista.length;
  };

  window.__avance = () => ({
    hechas: Object.keys(window.__out).length,
    total: window.__total || 0,
    terminado: !!window.__terminado,
    errores: window.__err,
    formatoCambiado: window.__formatoCambiado || [],
  });

  window.__traer = (clave) => '@@' + clave + '@@' + (window.__out[clave] || '');

  // English names (preferred)
  window.__list = window.__listar;
  window.__batch = window.__lote;
  window.__fetch = window.__traer;
  window.__progress = () => {
    const a = window.__avance();
    return { done: a.hechas, total: a.total, finished: a.terminado, errors: a.errores, formatChanged: a.formatoCambiado };
  };

  return 'browser export helpers ready';
})();
