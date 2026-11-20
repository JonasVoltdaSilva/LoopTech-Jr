"""Real browser checks for the built site; no server is started by this file."""

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (360, 390, 520, 768, 1024, 1280, 1440)


def main():
    parser = argparse.ArgumentParser(description="Check Loop Tech Jr. with Chromium.")
    parser.add_argument("--url", default="http://127.0.0.1:5173")
    parser.add_argument("--output", default="artifacts/review")
    parser.add_argument("--channel", default=os.environ.get("BROWSER_CHANNEL", "chrome"))
    args = parser.parse_args()
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    report = {"url": args.url, "checks": [], "layouts": [], "accessibility": []}
    errors, failed_requests, external_requests = [], [], []

    def check(name, condition, detail=None):
        passed = bool(condition)
        report["checks"].append({"name": name, "passed": passed, "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {name}")

    def accessibility(page, state):
        page.add_script_tag(path=str(ROOT / "node_modules/axe-core/axe.min.js"))
        findings = page.evaluate("""async () => {
          const result = await axe.run(document, {
            runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] }
          });
          return result.violations.map(v => ({
            id: v.id, impact: v.impact, description: v.description,
            nodes: v.nodes.map(n => ({target: n.target, summary: n.failureSummary}))
          }));
        }""")
        report["accessibility"].append({"state": state, "violations": findings})
        check(f"axe accessibility: {state}", not findings, findings)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel=None if args.channel == 'chromium' else args.channel)
        context = browser.new_context(
            viewport={"width": 1440, "height": 960},
            reduced_motion="reduce",
            accept_downloads=True,
        )
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("response", lambda response: failed_requests.append(f"{response.status} {response.url}") if response.status >= 400 else None)
        page.on("request", lambda request: external_requests.append(request.url) if urlparse(request.url).hostname not in {"localhost", "127.0.0.1", None} else None)

        for width in WIDTHS:
            page.set_viewport_size({"width": width, "height": 960 if width >= 768 else 844})
            page.goto(args.url)
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            layout = page.evaluate("""() => ({
              viewport: innerWidth,
              document: document.documentElement.scrollWidth,
              fontLoaded: document.fonts.check('700 32px Sora'),
              brokenImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).length,
              emptyLinks: [...document.querySelectorAll('a')].filter(a => !a.getAttribute('href') || a.getAttribute('href') === '#').length,
              brokenAnchors: [...document.querySelectorAll('a[href^="#"]')].filter(a => !document.getElementById(a.hash.slice(1))).map(a => a.hash),
              headings: document.querySelectorAll('h1').length,
              outside: [...document.querySelectorAll('main h1, main h2, main h3, main p, main input, main textarea, main select, main button, .values-strip > div')]
                .filter(e => !e.closest('[hidden], [aria-hidden="true"]') && e.getClientRects().length)
                .filter(e => {const r=e.getBoundingClientRect(); return r.left < -1 || r.right > innerWidth + 1;})
                .map(e => ({tag:e.tagName, class:e.className, text:e.textContent.slice(0,80)}))
            })""")
            report["layouts"].append(layout)
            check(f"no horizontal overflow at {width}px", layout["document"] <= width and not layout["outside"], layout)
            check(f"font and assets at {width}px", layout["fontLoaded"] and not layout["brokenImages"])
            check(f"semantic links and title at {width}px", not layout["emptyLinks"] and not layout["brokenAnchors"] and layout["headings"] == 1)
            page.screenshot(path=str(output / f"layout-{width}.png"), full_page=True)
            if width in (390, 1440):
                page.screenshot(path=str(output / f"hero-{width}.png"))
            accessibility(page, f"initial-{width}")

        page.set_viewport_size({"width": 1440, "height": 960})
        page.goto(args.url)
        page.wait_for_load_state("networkidle")
        page.keyboard.press("Tab")
        check("keyboard skip link is first", page.evaluate("document.activeElement.classList.contains('skip-link')"))
        page.keyboard.press("Enter")
        check("skip link moves focus to main", page.evaluate("document.activeElement.id === 'conteudo'"))

        page.locator('.nav-link[href="#servicos"]').click()
        check("desktop navigation and active state", page.evaluate("location.hash === '#servicos'") and page.locator('.nav-link[href="#servicos"]').get_attribute("aria-current") == "location")
        page.locator('.nav-link[href="#projetos"]').click()
        page.go_back()
        check("browser back restores anchor", page.evaluate("location.hash === '#servicos'"))

        page.locator('[data-filter="sites"]').click()
        check("sites filter", page.locator('.project-card:visible').count() == 1 and page.locator('.project-card[data-category="sites"]').is_visible())
        check("filter announces results", page.locator('#project-status').inner_text() == '1 conceito demonstrativo exibido.')
        page.locator('.project-card[data-category="sites"] summary').click()
        check("concept details expand", page.locator('.project-card[data-category="sites"] details').get_attribute('open') is not None)
        page.locator('[data-filter="sistemas"]').click()
        check("systems filter and hidden details reset", page.locator('.project-card:visible').count() == 1 and page.locator('.project-card[data-category="sites"] details').get_attribute('open') is None)
        page.locator('[data-filter="todos"]').click()
        check("all projects restored", page.locator('.project-card:visible').count() == 2)
        page.locator('.project-card[data-category="sistemas"] summary').focus()
        page.keyboard.press('Enter')
        check("details works with keyboard", page.locator('.project-card[data-category="sistemas"] details').get_attribute('open') is not None)

        page.locator('.service-link[data-service="design"]').click()
        check("service CTA preselects contact subject", page.locator('#service').input_value() == 'design' and page.evaluate("location.hash === '#contato'"))
        page.locator('#service').select_option('')
        page.locator('.form-submit').click()
        check("empty form has four associated errors", page.locator('[aria-invalid="true"]').count() == 4 and page.evaluate("document.activeElement.id === 'name'"))
        check("form error status is explicit", 'Revise os campos' in page.locator('#form-status').inner_text())
        page.screenshot(path=str(output / 'form-errors.png'), full_page=True)
        accessibility(page, 'form-errors')

        page.locator('#name').fill('Pessoa de teste')
        page.locator('#email').fill('email-invalido')
        page.locator('#service').select_option('sites')
        page.locator('#message').fill('Ideia curta')
        page.locator('.form-submit').click()
        check("invalid email and short message rejected", page.locator('[aria-invalid="true"]').count() == 2 and 'e-mail válido' in page.locator('#email-error').inner_text())

        page.locator('#email').fill('teste@example.com')
        safe_message = 'Quero um site acessível para apresentar meu trabalho. <script>alert("teste")</script>'
        page.locator('#message').fill(safe_message)
        check("message character counter", page.locator('#message-count').inner_text() == f'{len(safe_message)} / 2000')
        page.locator('.form-submit').click()
        check("valid form generates local summary", page.locator('#brief-result').is_visible() and not page.locator('#contact-form').is_visible())
        check("summary uses safe text, not HTML", safe_message in page.locator('#brief-summary').inner_text() and page.locator('#brief-summary script').count() == 0)
        check("summary receives accessible focus", page.evaluate("document.activeElement.id === 'result-title'"))
        check("no fake submission confirmation", 'Nada foi enviado' in page.locator('#brief-result').inner_text())
        accessibility(page, 'brief-result')

        with page.expect_download() as downloaded:
            page.locator('#download-brief').click()
        download = downloaded.value
        download.save_as(str(output / download.suggested_filename))
        downloaded_text = (output / download.suggested_filename).read_text(encoding='utf-8-sig')
        check("download contains the local briefing", 'Pessoa de teste' in downloaded_text and safe_message in downloaded_text and 'não foi enviado' in downloaded_text)
        page.locator('#edit-brief').click()
        check("editing retains values and restores focus", page.locator('#contact-form').is_visible() and page.locator('#name').input_value() == 'Pessoa de teste' and page.evaluate("document.activeElement.id === 'name'"))
        check("no persistent browser storage", page.evaluate("localStorage.length === 0 && sessionStorage.length === 0"))

        page.locator('#name').fill('N' * 100)
        page.locator('#message').fill('A' * 2000)
        page.locator('.form-submit').click()
        page.set_viewport_size({"width": 360, "height": 844})
        check("long briefing wraps on small screens", page.evaluate("document.documentElement.scrollWidth === innerWidth") and page.locator('#brief-summary').evaluate('(el) => el.scrollWidth <= el.clientWidth'))

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(args.url)
        page.wait_for_load_state("networkidle")
        toggle = page.locator('.menu-toggle')
        check("mobile navigation is hidden and inert", page.locator('#main-navigation').evaluate('(el) => el.inert') and toggle.get_attribute('aria-expanded') == 'false')
        toggle.click()
        check("mobile menu opens", toggle.get_attribute('aria-expanded') == 'true' and page.locator('.nav-link[href="#servicos"]').is_visible())
        page.screenshot(path=str(output / 'menu-mobile.png'))
        accessibility(page, 'mobile-menu-open')
        page.keyboard.press('Escape')
        check("escape closes menu and returns focus", toggle.get_attribute('aria-expanded') == 'false' and toggle.evaluate('(el) => document.activeElement === el'))
        toggle.click()
        page.locator('.nav-link[href="#sobre"]').click()
        check("mobile link closes menu and focuses section", toggle.get_attribute('aria-expanded') == 'false' and page.evaluate("document.activeElement.id === 'sobre' && location.hash === '#sobre'"))
        toggle.click()
        page.locator('#about-title').click()
        check("outside click closes mobile menu", toggle.get_attribute('aria-expanded') == 'false')
        toggle.click()
        page.locator('.sidebar-cta').focus()
        page.keyboard.press('Tab')
        check("tab leaves disclosure without a focus trap", toggle.get_attribute('aria-expanded') == 'false')
        toggle.click()
        page.set_viewport_size({"width": 1024, "height": 900})
        check("resize restores desktop navigation", not page.locator('#main-navigation').evaluate('(el) => el.inert'))

        check("reduced motion respected", page.evaluate("getComputedStyle(document.documentElement).scrollBehavior === 'auto'"))
        check("no runtime or browser console errors", not errors, errors)
        check("no failed HTTP resources", not failed_requests, failed_requests)
        check("no external requests from the site", not external_requests, external_requests)

        no_js = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
        no_js_page = no_js.new_page()
        no_js_page.goto(args.url)
        check("no-JS form cannot accidentally submit personal data", no_js_page.locator('.form-submit').is_disabled() and no_js_page.locator('.noscript-notice').is_visible())
        check("core content exists without JavaScript", no_js_page.locator('h1').is_visible() and no_js_page.locator('.service-item').count() == 4)
        no_js.close()

        context.close()
        browser.close()

    report['passed'] = sum(c['passed'] for c in report['checks'])
    report['total'] = len(report['checks'])
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n{report['passed']}/{report['total']} checks passed. Report: {output / 'report.json'}")
    if report['passed'] != report['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
