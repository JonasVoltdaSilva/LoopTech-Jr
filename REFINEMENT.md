# LoopTech Jr. — refinamento e evidências

## Estado atual — logo transparente e cores da página

O usuário rejeitou a caixa branca e pediu também adequação das cores. A aplicação atual não tem fundo, padding, cantos ou filtros: topo/Sobre usam `looptech-logo-dark.png` com letras `#f5f3ff` e lavanda `#b298ff`; rodapé usa `looptech-logo-light.png` com letras `#0b071a` e roxo `#6545ff`. As duas variantes compartilham a silhueta extraída da mesma imagem. O alfa é recuperado do raster com remoção da textura branca e tratamento de bordas, não por redesenho das letras. O favicon também é transparente. A geração está em `tools/build_brand_assets.py`.

Testes desta rodada no build de produção (`http://127.0.0.1:4177/`): sintaxe/build aprovados, **85/85** de marca e transparência, **67/67** de regressão e **26/26** de vetores decorativos. Capturas revisadas em `artifacts/brand-transparent/`. O teste verifica alfa idêntico entre variantes, bordas externas transparentes, cores da paleta, remoção das áreas brancas e três aplicações nos oito tamanhos. Não é alegada igualdade das cores com o raster original: elas foram alteradas a pedido do usuário. Sem nova execução da suíte de zoom nativo, subagentes ou deploy. As caixas brancas documentadas abaixo são histórico rejeitado, não o estado atual.

## Atualização mais recente — consistência de todas as assinaturas

A pedido do usuário, topo, Sobre e rodapé passaram a usar o mesmo arquivo `public/looptech-logo.png`, derivado sem reamostragem do anexo original. Mesma arte, fundo branco, padding de 6 × 8 px, raio de 4 px e escala proporcional; somente as larguras contextuais variam. O ícone da aba agora é `public/looptech-favicon.png`, extraído do infinito desse anexo. A assinatura SVG aproximada e seus estilos foram removidos para evitar versões divergentes. Os vetores decorativos e os previews de projetos fictícios foram preservados.

Validação contra o **build de produção**, servido em `http://127.0.0.1:4177/`: sintaxe e build aprovados, `tests/test_header_logo.py` ampliado para as três aplicações (**79/79**, incluindo origem do favicon e oito viewports), `tests/test_site.py` (**67/67**), `tests/test_vectors.py` (**26/26**). Evidências e comparação visual de Sobre/rodapé em desktop/mobile em `artifacts/brand-consistency/`. A suíte específica de zoom nativo não foi repetida nesta etapa. Sem nova execução de subagentes; Frontend Design aplicado e capturas revisadas pelo agente principal.

As seções seguintes são histórico; sua antiga limitação ao topo não descreve o estado atual.

## Atualização — logo do topo conforme o anexo do usuário

O bloqueio de acesso à imagem foi resolvido. A logo do topo agora usa a própria arte enviada (1600 × 533), preservada em `public/looptech-logo-reference.png`. O arquivo aplicado `public/looptech-logo-header.png` é um recorte de margens externas sem reamostragem (1273 × 234). Letras, símbolo, cores e ausência de ponto terminal não foram redesenhados. Fundo branco preserva as letras escuras na sidebar; a proporção é mantida por largura responsiva e altura automática.

Escopo restrito ao topo: a assinatura SVG em Sobre/rodapé e os demais infinitos continuam como antes. Assim, referências abaixo a três assinaturas SVG compartilhadas e à indisponibilidade desse anexo descrevem o estado histórico anterior, não a implementação atual.

Verificação desta atualização: `npm.cmd run check`, `npm.cmd run build`, `tests/test_header_logo.py` (36/36), `tests/test_site.py` (67/67) e `tests/test_vectors.py` (26/26). Testes de navegador contra `http://127.0.0.1:5173/`. A nova suíte comprova igualdade pixel a pixel com o recorte da referência, carregamento, proporção, nome acessível, ausência de overflow, encaixe da sidebar e navegação nos oito viewports. Não foi reexecutada nesta etapa a suíte de zoom nativo. Evidências próprias em `artifacts/header-logo/`, sem sobrescrever o baseline de refinamento.

Skill aplicada nesta atualização: Frontend Design. Sem nova execução de subagentes. O restante deste documento preserva o histórico da rodada anterior.

## Escopo e estado

Correção integrada da identidade existente, sem redesign: paleta, Sora, estrutura das seções, textos, navegação, filtros e briefing local preservados. Não houve deploy, integração externa, armazenamento ou envio de dados.

As quatro novas imagens mencionadas no pedido **não chegaram como anexos acessíveis**. Os defeitos foram reproduzidos no código e no navegador. As comparações são entre o estado real inicial e o estado corrigido, não uma alegação de inspeção das quatro capturas ausentes.

Sem Git nesta pasta. Os principais arquivos anteriores foram preservados em `artifacts/refinement/before/source/`; nenhuma coleção de skills ou configuração global foi alterada.

## 1. Infinito com listras

**Causa confirmada:** o hero tinha um traço roxo de 62 unidades, uma sobreposição lavanda de 80 e um segundo trecho roxo de 62. A diferença produzia bordas claras diagonais; as extremidades de trechos sobrepostos também podiam expor emendas de rasterização.

**Correção:** remoção dessa construção segmentada. Hero, marca e motivos agora referenciam `#brand-loop`: um único path contínuo, opaco, com traço 13. O hero aplica um único gradiente roxo. Não há pintura da cor do fundo, máscaras, blur, redução de opacidade ou preenchimento dos vazios.

O master inicial também excedia seu enquadramento: pintura horizontal de -1.5 a 121.5 em viewBox de 0 a 120. A geometria foi preservada e transladada `(4, 2)` em um canvas de `128 × 64`, começando em zero. Isso inclui o stroke e evita o deslocamento duplicado que um viewBox negativo pode introduzir quando reutilizado como symbol. Limites pintados finais: x 2.5–125.5; y 3.5–60.5.

## 2. Assinatura tipográfica

Não foi localizado um vetor oficial correto. O defeito era da implementação autoral: símbolo de 39 × 25 px centralizado na caixa de linha, maior que a faixa óptica dos “o”, com tamanhos independentes em cada aplicação.

**Correção:** assinatura única `#looptech-wordmark`, compartilhada no topo, Sobre e rodapé. A Sora real foi carregada antes da medição e revisão. No desenho nominal de 204 × 42: texto Sora 750 a 32 px, baseline em y=30; infinito em x=16.8/y=9.5, dimensão proporcional 46 × 23; sufixo em x=60.5. O tamanho da fita acompanha a altura óptica das minúsculas, não toda a caixa de linha. “Jr.” usa peso 650.

`src/brand.css` controla larguras e variantes claro/escuro. Não há deformação independente dos eixos. O infinito representa os dois “o” uma única vez. Os dois links de marca possuem nome acessível exato **LoopTech Jr.**; a arte interna é decorativa para o leitor de tela. O favicon deriva da mesma geometria.

## 3. Sidebar e limite físico

**Causa confirmada:** padding superior/inferior, margem de 52 px abaixo da identificação, navegação e bloco inferior com min-height/padding excessivos somavam cerca de 748 px. Em viewport de 1280 × 720, o navegador mediu `scrollHeight=748` e `clientHeight=720`; em 1280 × 600, o déficit era de 148 px.

**Correção:** Grid no contêiner, Flexbox no corpo, distribuição vertical consciente, espaçamentos adaptativos em `dvh` e bloco secundário sem altura mínima artificial. O infinito inferior ocupa sua própria célula, ao lado do texto, sem recorte nem sobreposição.

- Até 760 px de altura: modo compacto reduz espaços, mantendo textos e alvos de 44 px ou mais.
- Largura ≤767 px, altura ≤579 px, ou largura ≤959 px com altura ≤699 px: navegação recolhível **no fluxo do documento**, sem uma segunda área de rolagem.
- A identificação institucional, cinco destinos, chamada, CTA e informações inferiores permanecem disponíveis.
- Escape retorna foco visível; o ajuste de rolagem ocorre após layout/ancoragem. Não é menu modal e não exige armadilha de foco.
- A largura do trilho e a margem do conteúdo principal usam a mesma variável.

Não se promete sidebar fixa completa em qualquer altura ou zoom. No fallback, a página tem rolagem vertical normal.

## 4. Ícones

Pictogramas oficiais **Lucide 1.75.0**, incorporados localmente sem dependência de runtime. Canvas 24 × 24, traço 2, caps e joins arredondados. A faixa tem células equilibradas, gap consistente e separadores centralizados de 32 px; em telas estreitas reorganiza-se em duas colunas.

| Conteúdo | Ícone |
| --- | --- |
| Conexão | Link2 |
| Inovação | Lightbulb |
| Aprendizado | GraduationCap |
| Colaboração / Sobre | UsersRound |
| Início | House, nome canônico da família |
| Serviços | CodeXml |
| Projetos | FolderOpen |
| Contato | MessageCircle |

Setas, serviços e confirmação também usam a mesma família. O controle de menu mantém suas duas linhas CSS de 2 px. A biblioteca de pictogramas não substitui a geometria própria da marca. Licenças completas em `public/licenses/lucide.txt`.

## 5. Loops cortados

- **Sidebar:** motivo de 240 px rotacionado dentro de área de cerca de 188 px com overflow oculto. Agora é SVG proporcional de 46/40 px em célula própria; no menu em fluxo, 80 px.
- **Sobre:** posições negativas (`right`, `bottom`) cortavam a fita. Agora o loop ocupa uma célula inferior do grid, com espaço separado para o texto.
- **Contato:** a regra de tablet com `right:-75px` excedia a seção. O motivo agora está no fluxo normal, com largura limitada e margem positiva; também está disponível no mobile.
- **Hero:** dimensão e rotação passam a caber dentro da área reservada, sem cortar a forma.
- **Rodapé e assinaturas:** mesma geometria e viewport seguros, sem correções acidentais de escala.

Não foi aplicado `overflow:visible` global, ocultação de scrollbar ou corte de conteúdo para esconder defeitos.

## Referências realmente consultadas

| Link | Observação / princípio | Aplicação concreta |
| --- | --- | --- |
| [Linear Brand](https://linear.app/brand) | Orienta respiro e distinção entre assinatura, símbolo e versão compacta. | Uma assinatura reutilizável, cores controladas e margens; nenhum asset ou desenho Linear copiado. |
| [Lucide Design Principles](https://lucide.dev/contribute/icons/design-principles) e [catálogo](https://lucide.dev/icons/) | Canvas 24, traço 2, área de segurança e coerência óptica. | SVGs oficiais verificados, normalização de stroke e distribuição dos quatro grupos. |
| [Lucide 1.75.0 / licença](https://raw.githubusercontent.com/lucide-icons/lucide/1.75.0/LICENSE) | ISC e aviso MIT dos derivados de Feather. | Preservação dos dois avisos completos no build. |
| [Carbon — left panel](https://carbondesignsystem.com/building-blocks/core/components/ui-shell-left-panel/guidelines/) e [acessibilidade](https://carbondesignsystem.com/building-blocks/core/components/ui-shell-left-panel/accessibility/) | Navegação por teclado, estado atual e alternativa recolhível para pouco espaço/zoom. | Cinco links preservados, aria-current/expanded, Escape e navegação no fluxo; sem importar aparência de dashboard. |
| [MDN — viewBox](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/viewBox), [preserveAspectRatio](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/preserveAspectRatio), [overflow](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/overflow) | Enquadramento, escala uniforme e clipping real dos viewports SVG. | Master com stroke dentro dos limites, origem zero e `xMidYMid meet`; contenção específica de cada motivo. |
| [WAI — Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | Reorganizar sem perder informação, sem exigir duas direções de rolagem; retirar fixação quando prejudica leitura. | Largura de 320 px testada, fallback por altura e zoom nativo de 100% a 200%. |
| [Phan Bach — xolve](https://www.xolvebranding.com/work/phan-bach/) | Texto do criador descreve continuidade e tipografia desenvolvida em conjunto. | Princípio de unidade entre símbolo e letras; não se copiou sua construção P/B. |
| [Infinite Loop — Alexa Wright Nishimura](https://www.alexa-wright.com/work/logos#infiniteloop-logo) | Portfólio acessível identifica aplicações de uma identidade em vários suportes. | Comparar a marca pequena, intermediária e grande. Não foi usado como prova visual de uma geometria específica de dois vazios. |

A busca de Infinity Logo no Behance e páginas testadas retornaram HTTP 403. Não são alegadas como projetos visualmente analisados. As duas páginas dos criadores acima foram usadas pelos princípios textuais acessíveis, não como licença para reproduzir seus vetores.

## Testes e evidências

Última rodada de produção: `artifacts/refinement/summary.json`, quatro suítes aprovadas.

| Grupo | Resultado |
| --- | --- |
| Fluxos existentes e axe-core | 67/67 |
| Layout e contenção | 82/82 em oito viewports |
| Vetores, repetição e nomes acessíveis | 26/26 |
| Zoom nativo e navegação alternativa | 38/38 |

Viewports: **1280×720, 1366×768, 1440×900, 1920×1080, 1280×600, 768×1024, 390×844 e 320×568**. Em todos os desktops fixos, `scrollHeight` e `clientHeight` da sidebar coincidiram. Não foi encontrado overflow horizontal nessa matriz.

Zoom real em Chromium isolado, através de `chrome.tabs.setZoom`, com janela física constante de 1280×720; fatores confirmados também por `devicePixelRatio`. Viewports CSS resultantes: 1280×720, 1024×576, 853×480 e 640×360. Não se usou CSS zoom nem emulação de viewport para se passar por zoom real. As capturas usam a superfície física completa via CDP para evitar o recorte que a captura por coordenadas CSS pode causar nesse modo.

Vetores renderizados em 36/128/520 px, fundos claro/escuro e DPR 1/2: uma região conectada e dois vazios; teste adicional de distância da pintura às bordas em 128/520 px. Isso complementa, não substitui, a revisão visual.

- `before/`: estado inicial e snapshots de código preservados.
- `after/`: matriz final, menus e recortes de componentes.
- `comparisons/`: **14 pares** nos mesmos viewports/recortes, sem ampliar um lado para simular fidelidade.
- `vectors/`: provas e relatório de topologia.
- `zoom/`: zoom nativo, menu e informações inferiores alcançáveis pela rolagem normal.
- `regression/`: testes de formulário, teclado, filtros, resumo, download, acessibilidade automática e ausência de transmissão/persistência.

Comandos executados: `npm.cmd run check`, `npm.cmd run build`, helper local `with_server.py` previamente inspecionado e `tests/run_refinement.py --url http://127.0.0.1:4175`. O refinamento não adicionou lint ou TypeScript inexistentes. Pillow e Playwright estão apenas no ambiente local de testes.

## Skills, agentes e revisão final

- Frontend Design registrado e local: composição, proporções e linguagem existente.
- Impeccable local, aplicado manualmente: layout, adaptação, polish, audit e revisão por evidência. Engine/CLI e detector não foram executados.
- Webapp Testing local: suíte Python Playwright real, screenshots e fluxos.
- Agente **explore**: inventário e diagnóstico de geometria, clipping e orçamento vertical.
- Agente **general**: pesquisa de marca, vetores, iconografia e licenças.
- Tentativas de QA independente e atualização documental por subagentes foram bloqueadas por cota. Não são contabilizadas como trabalho concluído; a revisão final e esta documentação foram realizadas pelo agente principal.

### persistence
Passa no escopo do refinamento: projeto, baseline, fontes, build e relatórios preservados. Documentação atual dos componentes está neste arquivo e nas atualizações pontuais de DESIGN.md/ASSETS.md. Os exemplos antigos do sidecar estão explicitamente identificados como históricos.

### fidelity
Infinito, assinatura, pictogramas, dimensões da sidebar e motivos completos conferidos nas capturas finais. Tipo e paleta preservados; mudanças de posição/escala e fallback de navegação são adaptações necessárias ao pedido. As quatro imagens novas ausentes não foram comparadas diretamente.

### ceiling
Revisão manual do agente principal, não independente. Limites abaixo permanecem; nenhuma certificação formal é alegada.

### material_fixes
Nenhum bloqueio material identificado nas capturas e verificações revisadas. Veredito manual: **ship**, restrito às correções implementadas e à matriz documentada.

### keep
Preservar identidade roxa/lavanda/escura, Sora, master único, leitura LoopTech Jr. e funcionamento exclusivamente local do briefing.

## Limitações reais

- Sem os quatro novos anexos para conferir as marcações exatas; sem vetor oficial separado para substituir a aproximação autoral.
- Sem revisão independente final por indisponibilidade de cota dos subagentes.
- Sem testes em Safari/Firefox, aparelhos físicos ou leitores de tela reais; axe não certifica WCAG.
- Sem publicação ou envio de formulário. Esses comportamentos não foram adicionados.
