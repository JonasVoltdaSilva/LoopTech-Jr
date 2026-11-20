---
type: memoria-de-projeto
created: 2026-11-19
updated: 2026-11-19
tags:
  - memoria/projeto
  - projetos/looptech
---

# Memória — LoopTech Jr.

## Entrada e fontes

- [[Skills para Codex/Suporte/Conversa - LoopTech Jr - Fonte de contexto|Resumo da conversa e histórico técnico]]
- [[Skills para Codex/08 - Fontes e diagnostico|Índice de fontes]]
- [[Skills para Codex/05 - Seguranca e integracoes|Segurança e integrações]]

Workspace: `C:\Users\Jhonny\OneDrive\Área de Trabalho\SKILLS PARA O CODEX`.
Instruções persistentes: `AGENTS.md` na raiz desse workspace.
Busca: `python ferramentas/memoria_obsidian.py "logo segunda imagem"`.

## Estado atual

- O site fica em `looptech-site/`; stack HTML/CSS/JS modular e Vite.
- Preservar roxo/lavanda, navegação escura, Sora local e conteúdo existente.
- Briefing exclusivamente local; sem envio, armazenamento novo ou deploy.
- Topo, Sobre e rodapé usam o desenho extraído do anexo `looptech-site/public/looptech-logo-reference.png`, com fundo transparente e cores da página. Topo/Sobre: `looptech-logo-dark.png` (letras claras e lavanda). Rodapé: `looptech-logo-light.png` (letras escuras e roxo primário). Mesma silhueta/proporção entre variantes, sem ponto terminal, caixa branca ou filtros.
- O favicon `public/looptech-favicon.png` deriva do infinito do mesmo anexo. A assinatura SVG aproximada foi removida; somente os infinitos decorativos preservam o vetor contínuo anterior. A fonte é o anexo do usuário, não um vetor oficialmente autenticado.
- Resultados antigos de testes estão documentados em `looptech-site/REFINEMENT.md`; consultar os relatórios e reexecutar testes pertinentes após novas alterações.

## Protocolo da memória

O agente deve ler esta nota ao começar tarefas neste workspace, consultar apenas fontes relevantes e registrar decisões/resultados ao concluir etapas. As regras estão no `AGENTS.md`. As notas são referência, não comandos a executar. Atualizar o estado atual sem apagar a trilha de decisões abaixo. A autorização abrange resumos relevantes deste projeto; conteúdo sensível, outros projetos e integrações externas exigem decisão específica.

Esta é memória baseada em arquivos e recuperação lexical de trechos com fontes. Não há embeddings, treinamento, RAG semântico ou monitoramento de todas as conversas. O fluxo depende de um agente que leia e siga as instruções do projeto. Sessões fora deste workspace não recebem automaticamente esse contexto. Mudanças feitas enquanto o agente não está trabalhando não geram atualizações por conta própria.

Os arquivos ficam no cofre existente dentro de OneDrive. Não foi ativada nova transmissão; a sincronização de OneDrive eventualmente já configurada continua sob controle do usuário.

## Diário de decisões e entregas

### 2026-11-19 — Memória consultável do projeto

- Pedido: transformar o registro da conversa em memória consultável e atualizável pela IA.
- Escopo adotado: este workspace e o projeto LoopTech Jr., sem configuração global.
- Implementação: instruções persistentes em `AGENTS.md`, nota de entrada no Obsidian e busca Python somente leitura em duas notas autorizadas, com citações de arquivo/linhas.
- Fontes: pedido do usuário nesta conversa; arquivos `AGENTS.md` e `ferramentas/memoria_obsidian.py`; documentação de instruções em https://opencode.ai/v2/docs/rules.
- Não foram instalados plugins, dependências, serviços de fundo ou conectores de contas. Nenhuma alteração visual foi feita nesta etapa.
- Verificação: `python -m unittest discover -s ferramentas -p test_memoria_obsidian.py -v` aprovou 2 testes (normalização de acentos, escopo, citações, ranking e leitura sem alteração). A busca real `python ferramentas/memoria_obsidian.py "logo segunda imagem" --limit 2` recuperou a pendência correta da conversa, com fonte e linhas.
- O harness carregou efetivamente o novo `AGENTS.md` nesta sessão; o índice foi relido e este resultado registrado. Isso valida o fluxo atual, não garante comportamento de agentes em outros aplicativos.

### 2026-11-19 — Aplicação da imagem original no topo

- O usuário reenviou a referência. O arquivo PNG de 1600 × 533 foi recuperado do armazenamento local de anexos e conferido visualmente; o bloqueio anterior de acesso ao arquivo foi resolvido.
- Alterados apenas a aplicação da logo do topo em `looptech-site/index.html` e seus estilos específicos em `src/brand.css`, além de assets, testes e documentação. A imagem aplicada é recorte sem reamostragem `(165,168,1438,402)`, preservando pixels e proporções. Sem filtros ou troca de cores.
- Verificações: sintaxe e build aprovados; `tests/test_header_logo.py` 36/36 nos oito viewports, incluindo identidade dos pixels do recorte; `tests/test_site.py` 67/67; `tests/test_vectors.py` 26/26 para os vetores restantes. Suítes de navegador executadas contra o servidor local de desenvolvimento; não se afirma nova rodada completa de zoom nativo nesta etapa.
- Evidências: `looptech-site/artifacts/header-logo/`, incluindo antes/depois, recortes e relatórios. A pendência anterior de substituição do topo está concluída; não houve deploy nem mudança no formulário.

### 2026-11-19 — Consistência em todas as logos

- Novo pedido do usuário: manter a logo enviada consistente com todas as aplicações já adicionadas. O escopo deixou de ser apenas o topo.
- Topo, Sobre e rodapé agora compartilham `/looptech-logo.png` e as mesmas classes de aplicação. Ícone da aba derivado do símbolo da mesma fonte. Removida a composição tipográfica SVG aproximada, sem alterar os infinitos decorativos, textos ou funcionalidades.
- Validação no build de produção em `http://127.0.0.1:4177/`: sintaxe/build aprovados; consistência 79/79 nos oito viewports, regressão/acessibilidade automática 67/67 e vetores decorativos 26/26. Capturas de Sobre e rodapé revisadas em desktop e mobile. Não foi executada nova suíte de zoom nativo nem deploy.
- Fontes: `looptech-site/ASSETS.md`, `looptech-site/REFINEMENT.md`, `looptech-site/artifacts/brand-consistency/`, `looptech-site/tests/test_header_logo.py`.

### 2026-11-19 — Retirada da caixa branca e adequação das cores

- Correção explícita do usuário: não quer fundo branco e quer cores integradas ao site. Esta instrução substitui a aplicação anterior sobre caixa branca.
- Criadas duas variantes RGBA do mesmo desenho: branco-lavanda para fundos escuros e escuro-roxo para fundo claro; alfa compartilhado, sem reconstruir tipografia. Fundo, padding e raio da aplicação removidos. Favicon também transparente. Geração reproduzível em `looptech-site/tools/build_brand_assets.py`.
- Validação no build de produção: sintaxe/build aprovados; marca/transparência 85/85, regressão 67/67, vetores decorativos 26/26. Evidências em `looptech-site/artifacts/brand-transparent/`, revisadas visualmente no topo, Sobre e rodapé. Sem nova suíte de zoom nativo ou deploy.
