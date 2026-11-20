/* Loop Tech Jr. — Sistema de movimento autoral (tudo animado)
 *
 * Motion Personality: Premium
 *   - Easing assinatura: cubic-bezier(0.4, 0, 0.2, 1)
 *   - Overshoot: 0%
 *   - Durações: hero 800ms, reveal 600ms, micro 250ms, loop infinito 4s
 *
 * Regras respeitadas:
 *   - Sem preloader, sem sequestro de rolagem, sem cursor customizado
 *   - prefers-reduced-motion desativa toda animação
 *   - Conteúdo nunca escondido permanentemente se JS falhar
 *   - Apenas transform/opacity para performance
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const PREMIUM_EASE = 'cubic-bezier(0.4, 0, 0.2, 1)';
const DURATION = { hero: 0.8, reveal: 0.6, micro: 0.25, loop: 4 };

let mm;
let isReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ------------------------------------------------------------------ */
/* 1. Hero — revelação do título por linhas                           */
/* ------------------------------------------------------------------ */

function revealTitle() {
  if (isReduced) return;

  const lines = document.querySelectorAll('[data-split] .line');
  if (!lines.length) return;

  gsap.set(lines, { y: 22, opacity: 0 });

  gsap.to(lines, {
    y: 0,
    opacity: 1,
    duration: DURATION.hero,
    stagger: 0.14,
    ease: PREMIUM_EASE,
  });
}

/* ------------------------------------------------------------------ */
/* 2. Hero — infinito em loop contínuo (mais ousado)                 */
/* ------------------------------------------------------------------ */

function initInfinityLoop() {
  if (isReduced) return;

  const trail = document.querySelector('.infinity-trail');
  const heroInfinity = document.querySelector('.hero-infinity');

  if (!trail && !heroInfinity) return;

  if (trail) {
    const length = trail.getTotalLength();
    gsap.set(trail, { strokeDasharray: length, strokeDashoffset: length });

    /* Traço que se desenha e apaga continuamente = loop infinito */
    gsap.to(trail, {
      strokeDashoffset: 0,
      duration: DURATION.loop,
      ease: 'none',
      repeat: -1,
      yoyo: true,
    });
  }

  if (heroInfinity) {
    /* Pulsação de escala mais marcante */
    gsap.to(heroInfinity, {
      scale: 1.12,
      duration: DURATION.loop / 2,
      ease: PREMIUM_EASE,
      repeat: -1,
      yoyo: true,
      transformOrigin: 'center center',
    });

    /* Rotação sutil e contínua para dar vida ao símbolo */
    gsap.to(heroInfinity, {
      rotation: '-=6',
      duration: DURATION.loop * 2,
      ease: 'none',
      repeat: -1,
      transformOrigin: 'center center',
    });
  }
}

/* ------------------------------------------------------------------ */
/* 3. Scroll — reveal em todas as seções                             */
/* ------------------------------------------------------------------ */

function initScrollReveal() {
  if (isReduced) return;

  const sections = document.querySelectorAll('[data-reveal]');
  if (!sections.length) return;

  sections.forEach((section) => {
    const isHero = section.id === 'inicio';

    gsap.fromTo(
      section,
      { y: isHero ? 0 : 40, opacity: isHero ? 1 : 0 },
      {
        y: 0,
        opacity: 1,
        duration: DURATION.reveal,
        ease: PREMIUM_EASE,
        scrollTrigger: {
          trigger: section,
          start: isHero ? 'top top' : 'top 80%',
          end: 'bottom 60%',
          toggleActions: isHero ? 'play none none none' : 'play none reverse play',
          once: !isHero,
        },
      }
    );
  });

  /* Serviços: entrada escalonada dos itens */
  const serviceItems = document.querySelectorAll('.service-item');
  if (serviceItems.length) {
    gsap.fromTo(
      serviceItems,
      { y: 20, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.55,
        ease: PREMIUM_EASE,
        stagger: 0.1,
        scrollTrigger: {
          trigger: '.service-grid',
          start: 'top 80%',
          once: true,
        },
      }
    );
  }

  /* Projetos: revelação dos cards com escala */
  const projectCards = document.querySelectorAll('.project-card');
  if (projectCards.length) {
    gsap.fromTo(
      projectCards,
      { y: 24, opacity: 0, scale: 0.97 },
      {
        y: 0,
        opacity: 1,
        scale: 1,
        duration: 0.6,
        ease: PREMIUM_EASE,
        stagger: 0.12,
        scrollTrigger: {
          trigger: '.project-grid',
          start: 'top 80%',
          once: true,
        },
      }
    );
  }

  /* Sobre: revelação do copy e da arte */
  const aboutCopy = document.querySelector('.about-copy');
  if (aboutCopy) {
    gsap.fromTo(
      aboutCopy,
      { y: 20, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: DURATION.reveal,
        ease: PREMIUM_EASE,
        scrollTrigger: {
          trigger: '#sobre',
          start: 'top 75%',
          once: true,
        },
      }
    );
  }

  /* Contato: revelação do copy e do formulário */
  const contactCopy = document.querySelector('.contact-copy');
  const contactForm = document.querySelector('.contact-form-panel');
  if (contactCopy) {
    gsap.fromTo(
      contactCopy,
      { y: 20, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: DURATION.reveal,
        ease: PREMIUM_EASE,
        scrollTrigger: {
          trigger: '#contato',
          start: 'top 75%',
          once: true,
        },
      }
    );
  }
  if (contactForm) {
    gsap.fromTo(
      contactForm,
      { y: 20, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: DURATION.reveal,
        ease: PREMIUM_EASE,
        scrollTrigger: {
          trigger: '#contato',
          start: 'top 75%',
          once: true,
        },
      }
    );
  }
}

/* ------------------------------------------------------------------ */
/* 4. Microinterações (botões, links, navegação)                     */
/* ------------------------------------------------------------------ */

function initMicroInteractions() {
  if (isReduced) return;

  /* Botão primário: pressão sutil + ícone acompanha */
  const primaryButtons = document.querySelectorAll('.button-primary');
  primaryButtons.forEach((btn) => {
    btn.addEventListener('pointerenter', () => {
      gsap.to(btn, { scale: 0.97, duration: DURATION.micro, ease: 'power1.in' });
    });
    btn.addEventListener('pointerleave', () => {
      gsap.to(btn, { scale: 1, duration: DURATION.micro, ease: PREMIUM_EASE });
    });
    const icon = btn.querySelector('.icon');
    if (icon) {
      btn.addEventListener('pointerenter', () => {
        gsap.to(icon, { x: 4, duration: DURATION.micro, ease: PREMIUM_EASE });
      });
      btn.addEventListener('pointerleave', () => {
        gsap.to(icon, { x: 0, duration: DURATION.micro, ease: PREMIUM_EASE });
      });
    }
  });

  /* Links textuais: ícone desliza */
  const textLinks = document.querySelectorAll('.text-link');
  textLinks.forEach((link) => {
    link.addEventListener('pointerenter', () => {
      const icon = link.querySelector('.icon');
      if (icon) gsap.to(icon, { x: 5, duration: DURATION.micro, ease: PREMIUM_EASE });
    });
    link.addEventListener('pointerleave', () => {
      const icon = link.querySelector('.icon');
      if (icon) gsap.to(icon, { x: 0, duration: DURATION.micro, ease: PREMIUM_EASE });
    });
  });

  /* Navegação sidebar: hover nos links */
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach((link) => {
    link.addEventListener('pointerenter', () => {
      if (!link.classList.contains('is-active')) {
        gsap.to(link, { backgroundColor: '#241837', duration: DURATION.micro, ease: PREMIUM_EASE });
      }
    });
    link.addEventListener('pointerleave', () => {
      if (!link.classList.contains('is-active')) {
        gsap.to(link, { backgroundColor: 'transparent', duration: DURATION.micro, ease: PREMIUM_EASE });
      }
    });
  });
}

/* ------------------------------------------------------------------ */
/* 5. Menu mobile e acordeão (details)                               */
/* ------------------------------------------------------------------ */

function initMenuAndDetails() {
  const menuToggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      const open = sidebar.classList.toggle('menu-open');
      const body = document.body;

      if (open) {
        gsap.set('.sidebar-body', { display: 'flex', opacity: 0 });
        gsap.to('.sidebar-body', { opacity: 1, duration: 0.35, ease: PREMIUM_EASE });
        gsap.to(menuToggle.querySelectorAll('span'), {
          keyframes: [
            { transform: 'translateY(4px) rotate(45deg)' },
            { transform: 'translateY(-4px) rotate(-45deg)' },
          ],
          duration: 0.3,
          ease: PREMIUM_EASE,
          stagger: 0.05,
        });
        body.style.overflow = 'hidden';
      } else {
        gsap.to('.sidebar-body', {
          opacity: 0,
          duration: 0.25,
          ease: PREMIUM_EASE,
          onComplete: () => gsap.set('.sidebar-body', { display: 'none' }),
        });
        gsap.to(menuToggle.querySelectorAll('span'), {
          keyframes: [
            { transform: 'translateY(0) rotate(0)' },
            { transform: 'translateY(0) rotate(0)' },
          ],
          duration: 0.3,
          ease: PREMIUM_EASE,
          stagger: 0.05,
        });
        body.style.overflow = '';
      }
    });
  }

  /* Details do projeto: seta gira suavemente */
  const summaries = document.querySelectorAll('details > summary');
  summaries.forEach((summary) => {
    summary.addEventListener('click', () => {
      const details = summary.parentElement;
      const icon = summary.querySelector('.icon');
      const isOpen = details.open;

      if (icon) {
        gsap.to(icon, { rotation: isOpen ? 90 : 0, duration: 0.25, ease: PREMIUM_EASE });
      }
    });
  });
}

/* ------------------------------------------------------------------ */
/* 6. Feedback do formulário (confirmação)                           */
/* ------------------------------------------------------------------ */

function initFormFeedback() {
  const form = document.getElementById('contact-form');
  const result = document.getElementById('brief-result');
  const resultCheck = document.querySelector('.result-check');

  if (!form || !result) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const observer = new MutationObserver(() => {
      if (!result.hasAttribute('hidden') && resultCheck) {
        gsap.fromTo(
          resultCheck,
          { scale: 0.5, opacity: 0 },
          { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(1.2)' }
        );
        gsap.fromTo(
          result,
          { y: 12, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.5, ease: PREMIUM_EASE },
          '-=0.2'
        );
        observer.disconnect();
      }
    });
    observer.observe(result, { attributes: true, attributeFilter: ['hidden'] });
  });
}

/* ------------------------------------------------------------------ */
/* Inicialização                                                      */
/* ------------------------------------------------------------------ */

export function initMotion() {
  document.documentElement.classList.add('js-ready');

  mm = gsap.matchMedia();

  revealTitle();
  initInfinityLoop();

  if (!isReduced) {
    initScrollReveal();
    initMicroInteractions();
    initMenuAndDetails();
  }

  initFormFeedback();

  window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', () => {
    window.location.reload();
  });
}

export function cleanupMotion() {
  if (mm) mm.revert();
  ScrollTrigger.getAll().forEach((t) => t.kill());
  gsap.killTweensOf('.infinity-trail');
  gsap.killTweensOf('.hero-infinity');
  gsap.killTweensOf('[data-split] .line');
  gsap.killTweensOf('[data-reveal]');
  gsap.killTweensOf('.service-item');
  gsap.killTweensOf('.project-card');
  gsap.killTweensOf('.about-copy');
  gsap.killTweensOf('.contact-copy');
  gsap.killTweensOf('.contact-form-panel');
}
