# Prompts prontos

[[Skills para Codex/00 - Inicio|Início]] · [[Skills para Codex/02 - Instalar e usar|Instalação]]

Use os exemplos **depois de instalar e confirmar a skill em `/skills`**. Informar um nome no prompt não instala o pacote nem fornece as ferramentas exigidas.

## Capturar conhecimento no Obsidian

```text
$obsidian-capturar-conhecimento
No cofre {{vault_ps}}, transforme o texto que vou enviar em uma nota organizada, com resumo, fontes e próximas ações quando existirem. Não invente informações nem substitua notas existentes.
```

## Organizar notas sem mover arquivos

```text
$obsidian-organizar-cofre
No cofre {{vault_ps}}, faça primeiro um inventário da pasta que eu indicar e crie um índice por assunto. Preserve os arquivos atuais; não altere plugins, configurações ou anexos.
```

## Auditar uma skill antes de instalar

```text
$codex-auditar-skills
Revise a pasta da skill que vou indicar. Confira metadados, instruções, scripts, dependências e permissões. Não execute scripts, não instale nada e não autentique contas. Informe os arquivos analisados e os limites da revisão.
```

## Planejar uma implementação

```text
$create-plan
Inspecione o projeto e proponha um plano curto para [objetivo], incluindo arquivos afetados, critérios de aceite e testes. Não implemente antes de eu aprovar o plano.
```

## Melhorar uma interface

```text
$frontend-design
Melhore [página ou componente] para [público e objetivo]. Respeite a stack e a identidade existentes. Priorize hierarquia visual, acessibilidade e responsividade; valide a implementação antes de concluir.
```

## Testar uma aplicação web local

```text
$webapp-testing
Verifique [fluxo] na aplicação local que vou indicar. Use as ferramentas disponíveis, registre resultados reproduzíveis e diferencie testes executados de testes bloqueados. Não use contas reais nem altere dados de produção.
```

## Preparar passagem de contexto

```text
$handoff
Prepare uma passagem de contexto com objetivo, decisões, arquivos alterados, verificações já executadas, bloqueios e próximos passos. Não inclua segredos nem afirme que testes pendentes foram concluídos.
```

## Consultar uma integração

Escolha o **nome exato** na ficha da integração, em [[Skills para Codex/01 - Catalogo completo|Catálogo completo]]. Não presuma que o serviço esteja disponível só porque existe uma skill.

```text
Descubra as ferramentas realmente disponíveis para [aplicativo] e explique quais permissões seriam necessárias. Não conecte contas nem altere dados antes da minha autorização. Depois de autorizado, comece com uma consulta somente de leitura.
```

## Sequência útil para um projeto

1. `grill-me`: esclarecer o problema e encontrar lacunas.
2. `create-plan`: definir escopo, passos e testes.
3. Skill adequada à tarefa: implementar somente o escopo aprovado.
4. `webapp-testing`, quando aplicável: verificar o comportamento real.
5. `handoff`: registrar o estado do trabalho para continuar depois.
