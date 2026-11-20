# Instalar e usar no Codex

[[Skills para Codex/00 - Inicio|Início]] · [[Skills para Codex/01 - Catalogo completo|Catálogo]]

## 1. Escolher e revisar

Abra a ficha da skill e depois o link **Abrir SKILL.md original**. Confira os auxiliares, as dependências e as permissões. Para uma revisão guiada, veja [[Skills para Codex/06 - Skills personalizadas|codex-auditar-skills]].

Escolha uma versão por objetivo. O catálogo preserva cópias com nomes iguais para permitir comparação, não para incentivar a instalação de todas.

## 2. Escolher o escopo

Conforme a documentação oficial consultada em **2026-11-18**, os principais caminhos de autoria local são:

| Escopo | Pasta no Windows | Uso |
| --- | --- | --- |
| Usuário | `%USERPROFILE%\.agents\skills\` | Disponível para seus projetos. |
| Projeto | `<pasta-do-projeto>\.agents\skills\` | Restrita ao contexto do projeto. |

Os documentos antigos desta coleção também citam `.codex\skills`. Há arquivos nessa pasta nesta máquina, mas não migramos, removemos nem modificamos essa instalação. Veja os números observados em [[Skills para Codex/08 - Fontes e diagnostico|Fontes e diagnóstico]].

Configurações e versões podem variar. A confirmação final é a lista de skills do seu Codex, não apenas a presença do arquivo em disco.

## 3. Exemplo de instalação manual, sem sobrescrever

O exemplo abaixo copia **somente** a nova skill `obsidian-organizar-cofre`. Ele é uma instrução para você executar se decidir instalar; não foi executado nesta organização.

Leia a skill antes. Depois, no PowerShell:

```powershell
$origem = {{example_skill_ps}}
$raiz = Join-Path $HOME '.agents\skills'
$destino = Join-Path $raiz 'obsidian-organizar-cofre'

if (-not (Test-Path -LiteralPath (Join-Path $origem 'SKILL.md') -PathType Leaf)) {
    throw 'A origem não contém SKILL.md.'
}
if (Test-Path -LiteralPath $destino) {
    throw 'Destino já existe. Compare as versões antes de continuar.'
}

New-Item -ItemType Directory -Path $raiz -Force | Out-Null
Copy-Item -LiteralPath $origem -Destination $destino -Recurse -ErrorAction Stop
```

Para outra skill, ajuste a origem e use no destino o nome declarado no frontmatter `name`. Preserve os scripts, referências e arquivos auxiliares exigidos. Não instale a pasta inteira `awesome-codex-skills` como se fosse uma única skill.

> [!warning] Origem com pasta diferente do nome
> Algumas pastas da coleção não têm o mesmo nome do campo `name`. Outras têm nomes fora do padrão. Essas situações estão destacadas no diagnóstico e precisam de revisão antes da instalação.

## 4. Confirmar e chamar

No Codex CLI ou extensão de IDE, consulte `/skills` ou digite `$` para selecionar uma skill disponível. Exemplo:

```text
$obsidian-organizar-cofre
Crie um índice das notas que eu indicar. Não mova nem exclua arquivos existentes.
```

O Codex também pode selecionar uma skill pela descrição quando a tarefa corresponde ao seu escopo. Se uma instalação não aparecer, reinicie o Codex e confira a versão e o escopo utilizados.

## 5. Validar com uma tarefa pequena

- Comece com leitura ou criação de uma nota de exemplo, sem dados sensíveis.
- Confira o resultado antes de aplicar o fluxo a muitos arquivos.
- Autorize contas e ações externas separadamente, apenas se necessárias.
- Não confunda uma skill instalada com uma integração autenticada e testada.

Referência: https://developers.openai.com/codex/build-skills
