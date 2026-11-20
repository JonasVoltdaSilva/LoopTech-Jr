# Atualizar o catálogo

[[Skills para Codex/00 - Inicio|Início]]

O gerador foi criado especificamente para esta biblioteca. Lê metadados e hashes dos arquivos locais; não executa os scripts das skills, não baixa atualizações e não conecta contas.

## O que entra no inventário

- `skills-do-artigo/`
- `awesome-codex-skills/`
- `skills-personalizadas/`

Outros projetos, como `looptech-site/`, ficam fora do catálogo. Para novas skills locais, crie uma pasta com `SKILL.md` dentro de `skills-personalizadas/`.

## Dependências

Python 3.12 ou superior e PyYAML. Ambos estavam disponíveis na criação inicial. Não é necessário instalar plugins no Obsidian.

Se o Python informar que falta PyYAML, a instalação é uma ação separada, que você pode decidir executar:

```powershell
python -m pip install PyYAML
```

## Simular, sem gravar

```powershell
python {{script_ps}} --vault {{vault_ps}}
```

## Gerar ou atualizar

```powershell
python {{script_ps}} --vault {{vault_ps}} --write
```

## Conferir se o catálogo está atualizado

```powershell
python {{script_ps}} --vault {{vault_ps}} --check
```

O modo `--check` não grava e retorna um código de erro se houver diferenças. A data do inventário também faz parte dos arquivos gerados.

## Executar os testes do gerador

```powershell
python {{tests_ps}} -v
```

Os testes usam pastas temporárias próprias, não as notas reais. Eles verificam metadados, caminhos, simulação, duplicatas e proteção contra sobrescrita.

## Proteção de arquivos

- `Suporte/manifesto.json` guarda hashes dos arquivos gerados.
- Na primeira execução, o gerador recusa sobrescrever arquivos diferentes que já existam.
- Nas próximas execuções, recusa sobrescrever notas geradas que tenham sido editadas manualmente.
- Arquivos que deixarem de fazer parte do inventário são preservados, não excluídos automaticamente.
- Arquivos fora da pasta `Skills para Codex` não são gravados.
- Se houver conflito na conferência inicial, a geração não começa. Se houver alteração concorrente durante a gravação, a operação é interrompida e pode já ter criado parte das notas.

Para anotações pessoais que devam ficar livres de regeneração, crie uma nota separada e coloque um link para a ficha correspondente.

Se quiser modificar um guia gerado permanentemente, edite o modelo equivalente em `ferramentas/modelos-obsidian/` e gere novamente; não substitua silenciosamente uma nota local que já tenha sido alterada.

O manifesto protege contra sobrescrita acidental, mas não substitui backup, controle de versão ou sincronização.
