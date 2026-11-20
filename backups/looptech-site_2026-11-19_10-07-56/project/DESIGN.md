---
name: Loop Tech Jr.
description: "Identidade de referência traduzida em uma interface institucional clara, roxa e conectada."
colors:
  primary: "#6545ff"
  primary-hover: "#5130e0"
  ink: "#0b071a"
  background: "#f5f3ff"
  surface: "#ffffff"
  muted: "#655d77"
  line: "#ded8ec"
  dark-surface: "#191127"
  on-dark: "#f5f3ff"
  muted-on-dark: "#c2b7d7"
  error: "#a22243"
typography:
  display:
    fontFamily: "Sora, 'Segoe UI', sans-serif"
    fontSize: "clamp(46px, 4.8vw, 76px)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Sora, 'Segoe UI', sans-serif"
    fontSize: "clamp(28px, 2.65vw, 39px)"
    fontWeight: 650
    lineHeight: 1.27
    letterSpacing: "-0.04em"
  title:
    fontFamily: "Sora, 'Segoe UI', sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "-0.025em"
  body:
    fontFamily: "Sora, 'Segoe UI', sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.65
  body-copy:
    fontFamily: "Sora, 'Segoe UI', sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.9
  label:
    fontFamily: "Sora, 'Segoe UI', sans-serif"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
rounded:
  small: "8px"
  panel: "16px"
  control: "999px"
  navigation: "12px"
  field: "6px"
  preview: "7px"
spacing:
  "1": "8px"
  "2": "16px"
  "3": "24px"
  "4": "32px"
  "5": "48px"
  "6": "80px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "14px 23px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  text-link:
    textColor: "{colors.ink}"
    padding: "0"
  navigation:
    textColor: "#d0c6e0"
    rounded: "{rounded.navigation}"
    padding: "11px 16px"
  navigation-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
  filter:
    backgroundColor: "transparent"
    textColor: "#d2c5e4"
    rounded: "{rounded.control}"
    padding: "10px 21px"
  filter-selected:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
  field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "12px 13px"
  brief-panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
    padding: "30px"
  project-details:
    textColor: "{colors.on-dark}"
  wordmark:
    backgroundColor: "transparent"
    rounded: "0"
    padding: "0"
---

# Design System: Loop Tech Jr.

## Overview

**Creative North Star: "Conexão que vira tecnologia"**

Trilho escuro, superfícies lavanda claras, roxo saturado e infinito conectam uma interface de densidade moderada. Serviços usam listas abertas; painéis são reservados às ilustrações e ao briefing.

Decisões de implementação derivadas das pranchas fornecidas, não diretrizes oficiais nem aprovação da marca. A construção é orientada pelo código, sobre uma identidade existente, sem comp preciso da página inteira. Extração manual de `src/styles.css`, conferida com `index.html`, módulos de interação e `ASSETS.md`; CLI/engine Impeccable não executado para evitar instalação automática de binário.

Refinamento de marca, iconografia e navegação: fontes atuais também incluem `src/brand.css` e `src/navigation.css`. Decisões, referências e evidências do delta estão em `REFINEMENT.md`. Os exemplos de componentes antigos no sidecar foram preservados como histórico; os arquivos-fonte e este complemento prevalecem para os componentes refinados.

**Key Characteristics:**
- Contraste entre navegação escura e conteúdo claro.
- Sora local, hierarquia fluida e controles compactos.
- Infinito autoral em SVG; miniaturas ilustrativas em HTML/CSS.

## Colors

O frontmatter é normativo; os nomes de cores correspondem às variáveis CSS sem o prefixo `--color-`. Os tons adicionais nos exemplos de componentes são literais do CSS, não uma nova paleta. As rampas OKLCH do sidecar são interpolações para visualização, não tokens usados pela aplicação.

### Primary
- `primary`: ações principais, seleção de navegação, ícones e destaques tipográficos.
- `primary-hover`: resposta de hover da ação principal.

### Neutral
- `ink` e `dark-surface`: texto/trilho lateral e seção escura de conceitos, respectivamente.
- `background` e `surface`: base lavanda e painel branco do briefing.
- `on-dark` e `muted-on-dark`: texto principal e secundário em superfícies escuras.
- `muted` e `line`: texto de apoio, divisórias e limites suaves em superfícies claras.

`error` é uma cor funcional para bordas e mensagens de validação, não um segundo acento de marca.

**The Acento Principal Rule.** Preservar o roxo como acento principal; variações tonais não constituem novas cores institucionais.

## Typography

Sora variável local (pesos 100–800), com fallbacks no frontmatter, servida de `public/fonts/sora-latin-variable.woff2`; licença SIL OFL 1.1 em `public/fonts/OFL.txt`. Não depende de uma requisição ao Google Fonts em produção.

Os papéis do frontmatter registram valores-base: `display` para o título principal, `headline` para seções, `title` para serviços, `body` para a base da página, `body-copy` para parágrafos do hero/sobre e `label` para botões. A marca é uma imagem fornecida pelo usuário, não texto renderizado em Sora. Não há razão modular única; títulos usam balanceamento de linhas e parágrafos, composição de texto mais uniforme.

- Display: em 960–1199 px, `clamp(42px, 4.65vw, 58px)`; em 768–959 px, 52 px; em até 767 px, `clamp(43px, 10.9vw, 64px)` com entrelinha 1.11. As exceções 520–767 px e até 374 px usam 66 px e 42 px, respectivamente.
- Headline: no mobile, 29 px; até 374 px, 27 px. Sobre e contato possuem ajustes próprios no CSS, não uma escala adicional.
- Corpo: base de 14 px no mobile; parágrafos de serviço usam entrelinha 1.85 no desktop e 1.8 no mobile. Medidas de leitura observadas: serviços até 39ch, sobre até 47ch, ampliadas conforme a composição responsiva.
- Navegação: 13 px no desktop, 12 px no tablet, 14 px na navegação recolhível. Campos: 13 px no desktop e 16 px no mobile. Os textos minúsculos dentro dos previews são ilustração, não referência para texto funcional.
- Wordmark: duas variantes transparentes derivadas do anexo, com a mesma silhueta e proporção 1273:234. `public/looptech-logo-dark.png` em topo/Sobre usa letras claras e lavanda; `public/looptech-logo-light.png` no rodapé usa letras escuras e roxo primário. Sem fundo branco, caixa, padding, raio ou filtros CSS. Larguras controladas: 184 px na assinatura-base, 170/154 px nos trilhos estreitos, 180 px em Sobre e 174 px no rodapé. O infinito corresponde apenas aos dois “o”; não há ponto terminal visual. Não reconstruir a assinatura em fontes do site.

## Layout

O trilho lateral é fixo; a margem esquerda do conteúdo acompanha `--sidebar-width`. As larguras abaixo são decisões responsivas reais, não medidas estimadas das pranchas. O contêiner é centralizado dentro da área principal, já descontado o trilho.

| Viewport | Trilho lateral / cabeçalho | Largura do contêiner |
| --- | --- | --- |
| ≥1600 px | 252 px | `min(1120px, calc(100% - 96px))` |
| 1200–1599 px | 232 px | `min(1120px, calc(100% - 96px))` |
| 960–1199 px | 204 px | `calc(100% - 64px)` |
| 768–959 px | 180 px | `calc(100% - 48px)` |
| 520–767 px | trilho 0 px; cabeçalho no fluxo, altura natural | `calc(100% - 64px)` |
| 375–519 px | trilho 0 px; cabeçalho no fluxo, altura natural | `calc(100% - 40px)` |
| ≤374 px | trilho 0 px; cabeçalho no fluxo, altura natural | `calc(100% - 36px)` |

- As seis entradas de `spacing` reproduzem `--space-1` a `--space-6`. O CSS também possui ajustes ópticos fora dessa escala: respiro vertical de seção de 88 px, 64 px no tablet e 57 px no mobile.
- Desktop: hero em `1fr 0.94fr`; serviços em duas colunas com intervalo de 48 px; conceitos em duas colunas com intervalo de 28 px; sobre em `0.95fr 1fr` e contato em `0.9fr 1.15fr`, ambos com intervalo de 64 px. Até 1199 px os intervalos são reduzidos.
- Até 959 px, hero, serviços, conceitos, sobre e contato passam a uma coluna. A faixa de valores tem quatro células no desktop e em 520–767 px; duas em 768–959 px e até 519 px.
- Linhas de formulário: duas colunas em ≥1200 px e 520–959 px; uma em 960–1199 px e até 519 px. No mobile o conteúdo começa abaixo do cabeçalho; âncoras têm margem de rolagem de 89 px, contra 28 px no desktop.

A sidebar usa Grid/Flex, `100dvh` e conteúdo secundário sem alturas mínimas artificiais. Em altura de até 760 px, compacta padding, margens e gaps, mantendo alvos de pelo menos 44 px. O trilho é substituído por disclosure no fluxo quando a largura é ≤767 px, a altura é ≤579 px, ou largura ≤959 px combinada a altura ≤699 px. CSS e JavaScript observam a mesma condição; a margem principal acompanha `--sidebar-width`. Não há rolagem aninhada nem descarte de CTA, identificação ou informações institucionais.

## Elevation & Depth

A profundidade vem sobretudo de contraste tonal, divisórias e sobreposição de geometria. A única sombra, `--shadow-preview`, pertence às miniaturas de navegador HTML; seu valor exato está no sidecar. Gradientes do infinito e da ilustração institucional são tratamento gráfico, não elevação de controles.

**The Camadas Tonais Rule.** Separar superfícies por preenchimento e linha; reservar a sombra de preview às miniaturas ilustrativas.

## Shapes

Os raios do frontmatter têm usos distintos: `small` no link de salto, `panel` nos painéis e ilustrações, `control` em ações e filtros, `navigation` nos links do trilho, `field` nos campos e `preview` nas miniaturas de navegador. Divisórias e bordas de campos são finas (1 px); marcadores, controle de menu e confirmação usam círculos.

A assinatura usa o raster enviado pelo usuário, sem recriação tipográfica, em todas as aplicações. O favicon `public/looptech-favicon.png` extrai somente o infinito desse mesmo anexo. A assinatura SVG aproximada anterior foi removida. Os infinitos decorativos preservam o símbolo autoral `#brand-loop`: um path de traço 13, transladado `(4, 2)` em `viewBox="0 0 128 64"`, pintura única e dois vazios naturais, sem cortes claros. Essas decorações não são assinaturas alternativas. Os pictogramas de interface são Lucide 1.75.0, canvas 24 × 24 e traço 2, com licenças preservadas. Nexo e Fluxo são previews ilustrativos em HTML/CSS; capturas em `artifacts/` não são assets de produção. A origem detalhada permanece em `ASSETS.md`.

## Components

- **Buttons:** ação primária usa `button-primary`, altura mínima de 48 px e ícone de 18 px; hover aplica `button-primary-hover`, pressionamento desloca 1 px para baixo. Desabilitado mantém opacidade 0.6, cursor indisponível e nenhum deslocamento. Links textuais não têm preenchimento de botão; ficam roxos no hover. Área mínima usual de 44 px; o link secundário do hero usa 32 px no desktop e 44 px no mobile.
- **Navigation:** links arredondados, altura mínima de 48 px (44 px no modo compacto); hover tem preenchimento escuro clareado, seleção usa `navigation-active` e `aria-current="location"`. O item inicial possui também um ponto branco. O menu circular tem 44 px; aberto forma um X e revela a navegação no fluxo abaixo do cabeçalho. `aria-expanded` e `inert` acompanham o estado; Escape fecha, devolve foco ao controle e garante sua visibilidade após o ajuste de rolagem. Seleção, clique fora ou saída de foco também fecham o menu.
- **Chips:** filtros contornados sobre fundo escuro; hover clareia o preenchimento, seleção usa `filter-selected` e `aria-pressed`. Filtrar oculta os conceitos fora da categoria, fecha seus detalhes e anuncia a quantidade exibida. Não são categorias de clientes reais.
- **Cards / Containers:** serviços são itens abertos separados por linhas; conceitos têm miniaturas recortadas e metadados fora delas. O painel branco de briefing usa `brief-panel`, sem sombra. Seu padding cai para 24 px até 1199 px; no mobile é `23px 20px`, volta a 30 px em 520–767 px e reduz o eixo horizontal a 18 px até 374 px.
- **Inputs / Fields:** preenchimento branco, borda neutra que escurece no hover, raio `field` e altura mínima de 46 px (48 px no mobile). Textarea tem mínimo de 128 px e redimensionamento vertical. Foco aplica contorno primário de 2 px, afastado 2 px, e borda primária; `aria-invalid` aplica borda `error`, com mensagem associada por `aria-describedby`. Não há variante visual própria de campo desabilitado.
- **Details:** disclosure nativo com summary de altura mínima de 50 px; hover lilás e seta que gira 90° quando aberto. Preservar teclado e semântica de `details`/`summary`.
- **Briefing:** resultado substitui visualmente o formulário, com confirmação circular, resumo textual e ações de baixar/editar. Foco vai ao título do resultado; editar restaura os campos e foca o nome. As mensagens dizem explicitamente que o arquivo é local e nada foi enviado; não existe estado de envio remoto ou carregamento assíncrono.

**Foco e movimento:** contorno geral de 3 px, afastado 5 px, em `primary`; no trilho usa lilás claro (`#c0aaff`) e na seção escura, `#c9b0ff`. O link de salto aparece ao receber foco. Transições usam `--transition` e `--ease-out`, preservados no sidecar; a seta de serviço desloca `(2px, -2px)` no hover. Não há animação contínua. Com `prefers-reduced-motion: reduce`, rolagem passa a `auto` e animações/transições são desativadas globalmente, inclusive em pseudo-elementos.

## Do's and Don'ts

### Do:
- Do preservar a Sora local com sua licença e o infinito integrado ao nome.
- Do manter as larguras responsivas do trilho, contraste e foco visível dos controles.
- Do identificar previews como demonstrativos e o resumo de briefing como arquivo local, sem envio.

### Don't:
- Don't apresentar estes tokens ou o wordmark autoral como diretrizes oficiais aprovadas.
- Don't misturar a variante orbital com estrela ao sistema do infinito integrado.
- Don't usar pranchas/capturas como assets de produção nem conceitos fictícios como entregas de clientes.
