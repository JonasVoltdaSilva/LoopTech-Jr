# Ativacao das 832 integracoes

## Concluido

- 832 skills copiadas para `C:\Users\Jhonny\.codex\skills` sem sobrescrever skills existentes.
- MCP global chamado `rube` configurado no Codex com `https://connect.composio.dev/mcp`.
- Backup da configuracao anterior salvo ao lado de `config.toml`, na pasta `.codex`.

## Falta sua autorizacao

No PowerShell, execute:

```powershell
codex mcp login rube
```

Abra o link exibido pelo comando e aprove somente as permissoes que desejar. Nao compartilhe senhas, tokens ou chaves no chat.

Depois reinicie o Codex. Solicite a conexao de cada aplicativo que realmente usa e aprove a autorizacao desse aplicativo. A instalacao das skills nao cria contas, nao concede assinaturas e nao autoriza automaticamente os 832 servicos.

Exemplo de primeiro teste sem alterar dados:

> Descubra as ferramentas disponiveis no MCP rube. Conecte meu Google Drive com minha autorizacao e liste ate cinco arquivos, sem criar, alterar ou excluir nada.

## Compatibilidade pendente

Os arquivos originais usam `https://rube.app/mcp` e nomes de ferramentas `RUBE_*`. Esse dominio antigo nao resolveu nesta maquina. O endereco atual respondeu e ofereceu autenticacao OAuth, mas o login nao foi concluido nesta sessao.

Apos o login, sera necessario verificar os nomes reais das ferramentas e adaptar instrucoes antigas se houver diferencas. Nenhuma das 832 integracoes foi validada ponta a ponta ainda. Use o endpoint atual configurado, nao o endereco antigo presente nos arquivos originais.

## Escopo

Esta instalacao abrange as 832 skills de `awesome-codex-skills/composio-skills`. As demais skills do artigo e da raiz do repositorio continuam apenas baixadas na pasta de trabalho.
