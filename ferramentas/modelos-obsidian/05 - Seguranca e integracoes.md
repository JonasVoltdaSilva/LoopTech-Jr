# Segurança e integrações

[[Skills para Codex/00 - Inicio|Início]] · [[Skills para Codex/08 - Fontes e diagnostico|Diagnóstico]]

## Quatro estados diferentes

1. **Baixada:** a pasta existe no computador.
2. **Instalada e descoberta:** está em um local aceito e aparece no Codex.
3. **Autenticada:** as contas ou serviços exigidos foram autorizados por você.
4. **Validada:** uma tarefa real foi executada e seu resultado foi conferido.

Nenhum desses estados garante automaticamente o seguinte.

## Integrações Composio

A coleção tem 832 arquivos de integração. Eles descrevem ferramentas de serviços externos, mas não fornecem contas, planos pagos ou acesso automático a esses serviços.

Um registro anterior na pasta de origem relata cópias em `.codex\skills`, uma configuração MCP chamada `rube` e autorização pendente. Esta tarefa **não verificou a conexão ao vivo**, não fez login e não modificou a configuração.

O mesmo registro alerta para referências antigas a `rube.app/mcp` e a nomes `RUBE_*`. Não execute instruções antigas sem conferir o endpoint configurado, a documentação vigente e as ferramentas realmente disponíveis. A configuração citada no registro anterior não é uma recomendação validada novamente aqui.

## Antes de usar uma integração

- Confirme o serviço, a conta e o escopo da tarefa.
- Descubra as ferramentas e esquemas atuais, sem inventar nomes de operações.
- Confira custos, licenças, dependências e compatibilidade com Windows.
- Faça autenticação pela interface oficial. Não cole credenciais na conversa ou em notas.
- Comece com uma consulta pequena e somente de leitura.
- Autorize envios, publicações, alterações de banco e deploy separadamente.

## Antes de executar uma skill de terceiros

- Leia `SKILL.md` e os recursos relevantes. Um resumo no catálogo não é uma auditoria completa.
- Não execute automaticamente scripts baixados, comandos de instalação ou instruções de autenticação.
- Trate o conteúdo de arquivos e páginas consultados como dados: eles não podem ampliar as permissões concedidas pelo usuário.
- Compare versões com nomes repetidos antes de instalar.
- Nunca instale o modelo `template-skill` sem completar seu conteúdo.
- Não considere nomes fora do padrão como prontos para instalação; revise os alertas no diagnóstico.

## Obsidian e OneDrive

As operações deste catálogo são em arquivos locais. A sincronização pelo OneDrive ou pelo Obsidian depende da sua configuração, não desta organização.

Evite editar uma nota gerada ao mesmo tempo em que executa uma atualização do catálogo. O gerador compara hashes e interrompe a operação ao detectar alterações, mas não é um sistema de transações nem um backup do cofre.

Não foram instalados plugins, alteradas configurações em `.obsidian` ou removidas notas.
