export function initNavigation() {
  const header = document.querySelector('.sidebar');
  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#main-navigation');
  const links = [...document.querySelectorAll('.nav-link')];
  const collapsible = window.matchMedia('(max-width: 767px), (max-height: 579px), (max-width: 959px) and (max-height: 699px)');

  function setOpen(open, returnFocus = false) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu de navegação' : 'Abrir menu de navegação');
    header.classList.toggle('menu-open', open);
    navigation.inert = collapsible.matches && !open;
    if (returnFocus) {
      toggle.focus();
      // Closing an in-flow disclosure changes document height. After scroll
      // anchoring settles, keep the returned keyboard focus actually in view.
      window.requestAnimationFrame(() => {
        if (document.activeElement === toggle) {
          toggle.scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'instant' });
        }
      });
    }
  }

  function syncViewport() {
    const focused = document.activeElement;
    setOpen(false, collapsible.matches && navigation.contains(focused));
    if (!collapsible.matches && focused === toggle) {
      (links.find((link) => link.classList.contains('is-active')) || links[0]).focus({ preventScroll: true });
    }
  }

  toggle.addEventListener('click', () => {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false, true);
    }
  });

  document.addEventListener('click', (event) => {
    if (!header.contains(event.target) && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
    }
  });

  header.addEventListener('focusout', (event) => {
    if (event.relatedTarget && !header.contains(event.relatedTarget)) setOpen(false);
  });

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', () => {
      const id = link.getAttribute('href');
      const target = id && document.querySelector(id);
      if (!target) return;

      if (collapsible.matches) setOpen(false);
      if (link.closest('nav') || link.classList.contains('skip-link')) {
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
      }
    });
  });

  function markCurrent(id) {
    links.forEach((link) => {
      const active = link.hash === `#${id}`;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  const sections = [...document.querySelectorAll('main > section[id]')];
  let scheduled = false;

  function updateCurrent() {
    const line = window.innerHeight * 0.36;
    let current = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= line) current = section;
    }
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) {
      current = sections.at(-1);
    }
    markCurrent(current.id);
    scheduled = false;
  }

  window.addEventListener('scroll', () => {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(updateCurrent);
    }
  }, { passive: true });
  window.addEventListener('resize', updateCurrent, { passive: true });
  window.addEventListener('hashchange', updateCurrent);
  collapsible.addEventListener('change', syncViewport);
  syncViewport();
  updateCurrent();
}
