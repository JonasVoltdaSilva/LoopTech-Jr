# Loop Tech Jr.

Site institucional responsivo em português, implementado com HTML, CSS e JavaScript modular. Vite é usado apenas para desenvolvimento e build. Não há framework de interface nem dependências de produção.

## Executar no Windows / PowerShell

Requer Node.js 20.19+ ou 22.12+ (validado com Node 24).

```powershell
cd "C:\Users\Jhonny\OneDrive\Área de Trabalho\SKILLS PARA O CODEX\looptech-site"
npm.cmd ci
npm.cmd run dev
```

Abra `http://127.0.0.1:5173`. O uso de `npm.cmd` evita depender da política de execução de scripts do PowerShell. Não é necessário alterar nenhuma configuração global.

## Build e preview

```powershell
npm.cmd run check
npm.cmd run build
npm.cmd run preview
```

Preview: `http://127.0.0.1:4173`. Os arquivos estáticos para hospedagem ficam em `dist/`. Nenhuma publicação é feita automaticamente. O build utiliza caminhos a partir da raiz; para hospedar em subdiretório, defina a opção `base` do Vite conforme esse destino.

## O que funciona

- Navegação por âncoras, histórico e indicação da seção atual.
- Menu mobile com fechamento por Escape, seleção de link, clique externo ou saída de foco.
- Sidebar dimensionada por altura, modo compacto e menu no fluxo da página em espaço insuficiente, sem eliminar CTA ou informações institucionais.
- Infinito contínuo e assinatura compartilhada no topo, seção Sobre e rodapé; pictogramas oficiais Lucide locais.
- CTAs de serviço selecionam o assunto no formulário.
- Filtros de projetos e detalhes expansíveis operáveis por teclado.
- Validação com mensagens associadas aos campos, contador de caracteres e estados de erro.
- Geração, edição e download local do resumo do projeto em `.txt`.
- Foco visível, link de pular conteúdo, suporte a movimento reduzido e fonte Sora local.

## Limites importantes

**O formulário não envia contato.** As informações ficam somente na memória da página e podem ser baixadas pelo próprio visitante. Não há backend, banco, armazenamento persistente, analytics nem chamadas externas da interface. Sem JavaScript, o botão permanece desativado para evitar envio acidental dos campos pela URL.

Nexo e Fluxo são **conceitos demonstrativos**, não projetos de clientes. Textos complementares e os quatro serviços são propostas editoriais coerentes com as referências, não uma confirmação do catálogo comercial. Não foram inventados depoimentos, resultados, prêmios ou dados de contato.

As sete referências são pranchas de identidade com pequenos exemplos de site, não layouts completos de todas as seções. O site segue especialmente a navegação lateral escura e o hero claro dos exemplos finais. As demais seções e a adaptação mobile são derivadas. Fotografias e logotipos originais não foram encontrados como arquivos separados; a marca vetorial é uma aproximação, pendente de aprovação. Veja `ASSETS.md`.

## Testes reais de navegador

Os testes usam Python Playwright e axe-core (dependência de desenvolvimento). Não são necessários para iniciar o site.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
```

Com o servidor dev ou preview iniciado em outro terminal:

```powershell
.\.venv\Scripts\python.exe tests\test_site.py --url http://127.0.0.1:5173
```

O padrão utiliza o Google Chrome instalado (`--channel chrome`). Sem Chrome, instale o Chromium somente no ambiente de teste e selecione esse canal:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe tests\test_site.py --channel chromium --url http://127.0.0.1:5173
```

A suíte verifica 360, 390, 520, 768, 1024, 1280 e 1440 px; overflow; recursos; fonte; links; menu e teclado; histórico; filtros; validação; resumo; download; conteúdo longo; ausência de transmissão e persistência; movimento reduzido; conteúdo sem JavaScript e regras automatizadas de acessibilidade. Screenshots e relatório JSON ficam em `artifacts/review/` ou no caminho de `--output`.

Última execução do refinamento no build de produção: **4/4 suítes aprovadas** — 67 verificações de regressão/acessibilidade automática, 82 verificações de layout, 26 vetoriais e 38 de zoom nativo. Evidências atuais em `artifacts/refinement/`; o diretório `artifacts/final/` registra a implementação inicial. Cobertura e limites em `TESTING.md` e `REFINEMENT.md`.

Para repetir a matriz completa, com o servidor iniciado em outro terminal:

```powershell
.\.venv\Scripts\python.exe tests\run_refinement.py --url http://127.0.0.1:5173
```

As provas vetoriais também usam Pillow, incluído em `requirements-test.txt`. O teste de zoom usa um Chromium já instalado no cache local e uma extensão sem permissões em perfil temporário; não modifica seu perfil pessoal. Nesta máquina, o executável validado é `chromium-1248/chrome-win64/chrome.exe`. Em outro ambiente, execute `tests/test_zoom.py --executable "caminho\para\chromium\chrome.exe" --url http://127.0.0.1:5173`. O teste é zoom real via `chrome.tabs.setZoom`, não `CSS zoom` nem simples troca de viewport.

As comparações antes/depois estão em `artifacts/refinement/comparisons/`. Não sobrescreva o baseline executando novamente `refinement_audit.py --phase before`; o script recusa essa operação quando já há evidência inicial.

Não há TypeScript ou ESLint configurados. `check` verifica a sintaxe dos quatro módulos JavaScript e de `vite.config.js`; não é apresentado como lint ou verificação de tipos. Os testes automatizados não certificam conformidade WCAG nem substituem avaliação com leitores de tela e dispositivos reais.

## Organização

```text
index.html                 Estrutura, conteúdo e símbolos SVG
src/styles.css             Tokens, layout e responsividade
src/brand.css              Assinatura e variantes controladas
src/navigation.css         Sidebar, modo compacto e fallback no fluxo
src/navigation.js          Menu, foco e seção ativa
src/projects.js            Filtros de conceitos
src/contact.js             Validação e briefing local
src/main.js                Inicialização
public/fonts/              Sora local e licença
tests/test_site.py         Fluxos, layouts, screenshots e axe
tests/run_refinement.py    Matriz de layout, vetores, zoom e comparações
PRODUCT.md                 Contexto e suposições
DESIGN.md                  Sistema visual extraído da implementação
ASSETS.md                  Origem dos materiais
TESTING.md                 Resultados, cobertura e limites dos testes
REFINEMENT.md              Correções, referências, evidências e revisão manual
```

## Skills aplicadas

- **Frontend Design**: skill registrada e instruções locais em `skills-do-artigo/frontend-design/SKILL.md`; direção visual específica, composição e implementação sem template genérico.
- **Impeccable**: leitura manual das instruções locais e referências de novo trabalho, qualidade e documentação; hierarquia, estados, responsividade e revisão visual. O engine/CLI e os agentes especializados do pacote não foram instalados ou executados.
- **Webapp Testing**: instruções e exemplos locais aplicados em uma suíte Python Playwright real. O helper `with_server.py` foi inspecionado antes da execução e usado para validar o build de produção com servidor temporário.

Nenhuma coleção de skills ou configuração global foi alterada. Os arquivos da aplicação foram refinados dentro do escopo solicitado; snapshots dos principais arquivos anteriores estão em `artifacts/refinement/before/source/`.
