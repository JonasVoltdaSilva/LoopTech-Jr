# Cópia de avaliação — refinamento editorial

As regras de memória no `AGENTS.md` do workspace continuam válidas.

- Trabalhar apenas nesta cópia. A pasta irmã `looptech-site` é a versão preservada.
- Backup integral verificado: `../backups/looptech-site_2026-11-19_10-07-56/project`.
- Não modificar ou regenerar as logos transparentes aprovadas, o favicon, a fonte
  Sora ou `src/brand.css` sem aprovação específica. O refinamento verifica hashes.
- Contexto atual de composição e referências: `EDITORIAL.md` e `src/editorial.css`.
  `src/styles.css` permanece como base do site original; a folha editorial contém
  somente a variante de apresentação, sem substituir os módulos funcionais.
- Desenvolvimento: `npm.cmd run dev` em http://127.0.0.1:5180/.
- Build: `npm.cmd run check` e `npm.cmd run build`; `npm.cmd run preview`
  abre o build em http://127.0.0.1:5181/.
- Validação completa desta variante: `.\.venv\Scripts\python.exe tests\run_editorial.py --url http://127.0.0.1:5181`.
- Manter o briefing exclusivamente local, os conceitos explicitamente fictícios
  e todos os conteúdos originais. Não publicar ou promover esta cópia sobre a
  versão original sem autorização.
