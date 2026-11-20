# Skills baixadas

## Conteudo

- `skills-do-artigo/`: skills disponiveis para download citadas em https://composio.dev/content/top-codex-skills, com seus arquivos auxiliares.
  - Composio, Impeccable, Frontend Design, Webapp Testing, grill-me, handoff, Excalidraw, Frontend Slides e MCP Builder.
  - `remotion/`: as 13 skills atualmente presentes na colecao oficial indicada pelo artigo.
- `awesome-codex-skills/`: copia completa dos arquivos do repositorio https://github.com/composio-community/awesome-codex-skills, incluindo README, scripts, referencias, fontes e skills de integracoes. Contem 880 arquivos `SKILL.md`, dos quais 48 sao skills diretamente na raiz.
- `fontes-download.json`: origens, identificadores dos snapshots e contagens de arquivos.

## Excecoes e limites

- **Record & Replay**: segundo o artigo, e um recurso integrado em ambientes Codex compativeis. Nao ha uma pasta de skill para baixar no link indicado. Consulte https://learn.chatgpt.com/docs/extend/record-and-replay.
- O README do Awesome tambem recomenda projetos externos por links. Esses outros repositorios nao fazem parte da copia deste repositorio; seus links permanecem disponiveis em `awesome-codex-skills/README.md`.
- Frontend Slides inclui uma copia da skill para plugin; por isso a contagem de arquivos `SKILL.md` nao representa necessariamente skills unicas.

## Como usar no Codex

Os arquivos foram apenas baixados nesta pasta. Nao foram instalados globalmente, nenhum script baixado foi executado e nenhuma conta foi conectada.

Para instalar manualmente, copie a pasta da skill desejada, contendo `SKILL.md` e seus arquivos auxiliares, para `%USERPROFILE%\.codex\skills\` e reinicie o Codex. Para Remotion, escolha as subpastas dentro de `skills-do-artigo/remotion/`.

Impeccable foi obtido da versao preparada para agentes em `.agents/skills/impeccable` no repositorio oficial.

Revise as instrucoes antes de usar. Algumas skills dependem de programas, bibliotecas, autenticacao ou servicos pagos. O download nao instala essas dependencias nem garante compatibilidade de todas as skills com Windows. Skills de mesmo nome provenientes de fontes diferentes foram mantidas separadas para nao sobrescrever suas versoes.
