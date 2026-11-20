# Origem dos assets

## Fonte
- **Sora**, The Sora Project Authors. Fonte variável, pesos 100–800, subconjunto Latin com caracteres do português brasileiro.
- Arquivo: `public/fonts/sora-latin-variable.woff2`.
- Origem: `https://fonts.gstatic.com/s/sora/v17/xMQbuFFYT72XzQUpDg.woff2`.
- Licença: SIL Open Font License 1.1, incluída em `public/fonts/OFL.txt`.
- Origem da licença: `https://raw.githubusercontent.com/google/fonts/main/ofl/sora/OFL.txt`.
- Servida localmente; o site não depende do Google Fonts durante o uso.

## Marca
- **Mesma assinatura no topo, Sobre e rodapé:** fonte fornecida pelo usuário, preservada em `public/looptech-logo-reference.png` (1600 × 533). As variantes derivam do mesmo recorte `(165, 168, 1438, 402)`, 1273 × 234. Letras e símbolo não foram redesenhados; fundo branco removido e cores adaptadas à página, conforme o pedido mais recente.
- **Fundos escuros:** `public/looptech-logo-dark.png`, letras `#f5f3ff` e infinito/Tech `#b298ff`. **Fundo claro:** `public/looptech-logo-light.png`, letras `#0b071a` e infinito/Tech `#6545ff`. Os dois arquivos RGBA têm dimensões e canal alfa idênticos. O método recupera a cobertura de bordas do raster sobre branco e elimina a textura de papel; não é um vetor nem uma reprodução pixel a pixel das cores originais.
- As três aplicações compartilham `.wordmark-reference` e `.wordmark-reference-image` em `src/brand.css`, sem fundo, caixa, padding ou filtros CSS. Apenas larguras contextuais variam proporcionalmente. Os dois links têm nome acessível `LoopTech Jr.` sem duplicação; a assinatura de Sobre é decorativa junto à identificação textual da seção.
- **Ícone da aba:** `public/looptech-favicon.png` deriva do infinito do mesmo anexo, recorte `(286, 213, 572, 355)`, também com transparência e roxo do site. Redução proporcional com Lanczos até 224 px e centralização em canvas transparente 256 × 256.
- Geração reproduzível: `.\.venv\Scripts\python.exe tools\build_brand_assets.py`. A fonte é o anexo do usuário, não uma alegação de autenticação de arquivo oficial.
- `public/looptech-logo.png`, `public/looptech-logo-header.png` e `public/favicon.svg` são arquivos históricos sem referências na aplicação atual. A assinatura SVG aproximada e seus estilos foram removidos da implementação para evitar reaplicação acidental.
- Os infinitos grandes e secundários são motivos decorativos autorais, não assinaturas alternativas da marca. Continuam referenciando `#brand-loop` em `index.html`; o hero preserva a continuidade sem cortes claros solicitada anteriormente. O preview fictício Fluxo mantém sua composição própria.
- O master usa um único path, traço de 13 unidades e translação `(4, 2)` dentro de `viewBox="0 0 128 64"`. Não há máscaras, recortes claros ou segmentos para encobrir emendas.
- Se for fornecido um vetor oficial, substituir o raster compartilhado sem redesenhar a marca. O PNG atual não deve ser apresentado como vetor.
- A variante orbital com estrela da última referência não foi misturada com o sistema principal.

## Ícones de interface
- **Lucide 1.75.0**, SVGs oficiais incorporados aos símbolos de `index.html`; sem biblioteca de runtime, pacote adicional ou CDN.
- Fontes: `https://raw.githubusercontent.com/lucide-icons/lucide/1.75.0/icons/{nome}.svg`.
- Nomes utilizados: `house`, `code-xml`, `folder-open`, `users-round`, `message-circle`, `arrow-right`, `arrow-up-right`, `link-2`, `lightbulb`, `graduation-cap`, `panels-top-left`, `pencil-ruler`, `compass`, `check`, `download`.
- Canvas 24 × 24, traço de 2 unidades, terminações e junções arredondadas. Ícones que acompanham rótulos são decorativos para tecnologias assistivas.
- Licenças ISC e MIT dos ícones derivados do Feather: texto completo preservado em `public/licenses/lucide.txt` e copiado para o build.
- Licença verificada: `https://raw.githubusercontent.com/lucide-icons/lucide/1.75.0/LICENSE`.
- O controle de abrir/fechar menu mantém suas duas linhas CSS, com peso de 2 px; não é utilizado como símbolo de marca.

## Previews
- Nexo e Fluxo: composição HTML/CSS autoral, sem imagens externas. As interfaces, nomes e dados são exemplos fictícios, identificados como conceitos demonstrativos, não clientes nem cases entregues.
- Nenhuma prancha inteira foi usada como imagem de fundo, e nenhuma fotografia foi inventada como registro da equipe ou da sede.

## Capturas de teste
- `artifacts/`: screenshots geradas por Playwright no navegador Chrome instalado, usadas somente para revisão. Não entram no build nem são assets da aplicação.
- `artifacts/refinement/`: baseline preservado, capturas finais, 14 comparações pareadas, provas vetoriais em DPR 1/2 e zoom nativo em Chromium isolado. Referências e limites estão em `REFINEMENT.md`.
