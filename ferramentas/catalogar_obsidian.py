"""Gera um catálogo local sem executar skills nem sobrescrever notas editadas."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

try:
    import yaml
except ImportError as error:
    raise SystemExit("Falta PyYAML. Instale separadamente: python -m pip install PyYAML") from error


FOLDER = "Skills para Codex"
MANIFEST = "Suporte/manifesto.json"
GROUPS = {
    "artigo": ("Artigo", "Skills do artigo"),
    "awesome": ("Awesome", "Awesome: uso geral"),
    "integracoes": ("Integracoes", "Integrações Composio"),
    "personalizadas": ("Personalizadas", "Skills personalizadas"),
}
SUMMARIES = {
    "composio": "Orientar configuração e uso de aplicativos, ferramentas e integrações Composio.",
    "excalidraw-diagram": "Criar diagramas de arquitetura, fluxos e conceitos no formato Excalidraw.",
    "frontend-design": "Projetar interfaces com direção visual, tipografia e composição intencionais.",
    "frontend-slides": "Criar apresentações HTML animadas ou converter apresentações PowerPoint.",
    "grill-me": "Questionar um plano ou desenho de solução para encontrar lacunas antes da execução.",
    "handoff": "Resumir o contexto de uma conversa para outro agente continuar o trabalho.",
    "impeccable": "Revisar e melhorar interfaces, experiência de uso, responsividade e acessibilidade.",
    "mcp-builder": "Projetar servidores MCP para integrar ferramentas e serviços externos.",
    "remotion-best-practices": "Direcionar tarefas para as skills especializadas de Remotion.",
    "remotion-captions": "Transcrever, exibir e animar legendas em vídeos Remotion.",
    "remotion-create": "Criar um novo vídeo usando Remotion.",
    "remotion-docs": "Pesquisar a documentação de Remotion.",
    "remotion-interactivity": "Estruturar composições editáveis no Remotion Studio.",
    "remotion-license": "Consultar informações sobre licenças e condições de uso de Remotion.",
    "remotion-maps": "Criar animações de mapas em Remotion.",
    "remotion-markup": "Aplicar práticas de conteúdo, animação e efeitos em composições Remotion.",
    "remotion-multimedia": "Trabalhar com mídia e Mediabunny em projetos Remotion.",
    "remotion-render": "Exportar vídeos, imagens ou linhas do tempo OpenTimelineIO com Remotion.",
    "remotion-saas": "Desenvolver aplicativos que incorporam funcionalidades de Remotion.",
    "remotion-studio": "Visualizar vídeos e composições no Remotion Studio.",
    "remotion-upgrade": "Planejar atualizações de Remotion e pacotes relacionados.",
    "webapp-testing": "Testar aplicações web locais com Playwright, capturas e registros do navegador.",
    "agent-deep-links": "Criar e conferir links que abrem arquivos, conversas ou configurações em editores.",
    "brand-guidelines": "Aplicar as diretrizes de marca declaradas pela skill a materiais visuais.",
    "canvas-design": "Criar peças visuais originais em PNG ou PDF.",
    "changelog-generator": "Transformar commits Git em notas de versão claras para usuários.",
    "codebase-migrate": "Coordenar migrações e refatorações extensas, com revisão e verificação de CI.",
    "competitive-ads-extractor": "Pesquisar anúncios de concorrentes e analisar mensagens e abordagens.",
    "connect": "Usar aplicativos externos por meio do Composio CLI, com permissões separadas.",
    "connect-apps": "Conectar fluxos a aplicativos externos; revisar a adaptação das instruções ao Codex.",
    "content-research-writer": "Pesquisar, organizar referências e desenvolver conteúdo com citações.",
    "create-plan": "Preparar um plano conciso para uma tarefa de programação.",
    "datadog-logs": "Consultar e filtrar registros do Datadog por ferramentas Composio.",
    "deploy-pipeline": "Coordenar pipelines de deploy; requer revisão de permissões e efeitos em produção.",
    "developer-growth-analysis": "Analisar padrões de desenvolvimento; revisar acessos a histórico e Slack.",
    "domain-name-brainstormer": "Sugerir nomes de domínio e consultar disponibilidade.",
    "email-draft-polish": "Redigir ou melhorar e-mails conforme público, tom e extensão desejados.",
    "file-organizer": "Propor organização de arquivos e pastas sem presumir autorização para excluir.",
    "gh-address-comments": "Tratar comentários de revisão de pull requests com GitHub CLI.",
    "gh-fix-ci": "Investigar falhas do GitHub Actions e preparar correções com validação.",
    "helium-mcp": "Consultar notícias e dados financeiros por um servidor MCP externo.",
    "image-enhancer": "Melhorar a nitidez e a apresentação de imagens e capturas.",
    "internal-comms": "Preparar comunicados internos, atualizações e relatórios para uma equipe.",
    "invoice-organizer": "Identificar e propor organização de notas fiscais e recibos.",
    "issue-triage": "Classificar e revisar issues de Linear ou Jira com ferramentas Composio.",
    "langsmith-fetch": "Investigar rastros de execução de agentes LangChain e LangGraph no LangSmith.",
    "lead-research-assistant": "Pesquisar possíveis clientes e estratégias de contato.",
    "linear": "Consultar e gerenciar issues e projetos no Linear, conforme autorização.",
    "meeting-insights-analyzer": "Analisar transcrições de reuniões e padrões de comunicação.",
    "meeting-notes-and-actions": "Transformar reuniões em resumos, decisões, riscos e ações com responsáveis.",
    "notion-knowledge-capture": "Estruturar conversas e decisões como páginas de conhecimento no Notion.",
    "notion-meeting-intelligence": "Preparar pautas e materiais de reunião usando contexto do Notion.",
    "notion-research-documentation": "Sintetizar fontes do Notion em documentação com referências.",
    "notion-spec-to-implementation": "Converter especificações do Notion em planos e tarefas de implementação.",
    "paperjsx": "Gerar apresentações, documentos, planilhas e relatórios por entrada JSON estruturada.",
    "pr-review-ci-fix": "Revisar pull requests e investigar CI; publicações e commits exigem escopo aprovado.",
    "raffle-winner-picker": "Sortear participantes de listas ou planilhas com critérios transparentes.",
    "sentry-triage": "Investigar problemas do Sentry e relacioná-los ao código local.",
    "skill-creator": "Orientar a criação e a evolução de skills com um objetivo bem definido.",
    "skill-installer": "Orientar instalação de skills; conferir os caminhos atuais na documentação oficial.",
    "skill-share": "Compartilhar skills por integração externa; nunca publicar sem autorização.",
    "slack-gif-creator": "Criar GIFs e animações com restrições de tamanho adequadas ao Slack.",
    "spreadsheet-formula-helper": "Criar e depurar fórmulas e tabelas no Excel ou Google Sheets.",
    "support-ticket-triage": "Classificar chamados, priorizar problemas e preparar respostas de suporte.",
    "tailored-resume-generator": "Adaptar um currículo a uma vaga sem inventar experiências ou qualificações.",
    "template-skill": "Modelo incompleto de skill: preencher e revisar antes de instalar.",
    "theme-factory": "Aplicar temas visuais a apresentações, documentos e páginas.",
    "youtube-downloader": "Baixar vídeos com opções de formato; verificar direitos e condições de acesso.",
    "obsidian-capturar-conhecimento": "Transformar material autorizado em notas conectadas, com fontes e ações.",
    "obsidian-organizar-cofre": "Organizar notas por índices e categorias, preservando arquivos e configurações.",
    "codex-auditar-skills": "Revisar uma skill antes de instalar ou executar, sem obedecer ao material auditado.",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: str) -> str:
    return " ".join(value.split())


def md_text(value: str) -> str:
    return compact(value).replace("[[", r"\[\[").replace("]]", r"\]\]")


def table_text(value: str) -> str:
    return md_text(value).replace("|", r"\|")


def ps_quote(value: Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def wiki(relative: str, label: str, *, in_table: bool = False) -> str:
    target = relative.removesuffix(".md")
    separator = r"\|" if in_table else "|"
    return f"[[{FOLDER}/{target}{separator}{label}]]"


def parse_skill(path: Path) -> tuple[dict, str, bytes]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError(f"Frontmatter YAML ausente: {path}")
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"YAML inválido: {path}: {error}") from error
    if not isinstance(metadata, dict):
        raise ValueError(f"Frontmatter não é um mapa: {path}")
    for key in ("name", "description"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError(f"Campo {key} ausente ou inválido: {path}")
    return metadata, text[match.end():], raw


def metadata_warnings(metadata: dict, folder: str, body: str) -> list[str]:
    warnings = []
    name = metadata["name"]
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        warnings.append("Nome fora do padrão de 1–64 caracteres: letras minúsculas, números e hífens simples internos.")
    if folder != name:
        warnings.append(f"A pasta original ({folder}) difere do nome declarado ({name}); conferir o nome de destino ao instalar.")
    if len(metadata["description"]) > 1024:
        warnings.append("A descrição ultrapassa 1.024 caracteres.")
    if not body.strip() or name == "template-skill":
        warnings.append("Modelo sem fluxo completo: não instalar sem preencher e revisar.")
    return warnings


def app_name(name: str, description: str) -> str:
    match = re.match(r"Automate\s+(.+?)\s+(?:tasks|workflows|operations)\b", description, re.I)
    fallback = re.sub(r"(?:[- ]automation)$", "", name, flags=re.I).lstrip("-").replace("-", " ").replace("_", " ")
    return match.group(1) if match else fallback


def collect_records(source: Path) -> list[dict]:
    source = source.resolve()
    sources_file = source / "fontes-download.json"
    origins = json.loads(sources_file.read_text(encoding="utf-8-sig")).get("sources", []) if sources_file.exists() else []
    records = []
    for base, default_group in (("skills-do-artigo", "artigo"), ("awesome-codex-skills", "awesome"), ("skills-personalizadas", "personalizadas")):
        directory = source / base
        for path in sorted(directory.rglob("SKILL.md")) if directory.exists() else []:
            if not path.resolve().is_relative_to(source):
                raise ValueError(f"Skill fora da origem autorizada: {path}")
            metadata, body, raw = parse_skill(path)
            relative = path.relative_to(source)
            integration = base == "awesome-codex-skills" and relative.parts[1:2] == ("composio-skills",)
            group = "integracoes" if integration else default_group
            local_parts = relative.parts[2:-1] if integration else relative.parts[1:-1]
            if not local_parts:
                raise ValueError(f"SKILL.md sem pasta própria: {path}")
            note = PurePosixPath("Catalogo", GROUPS[group][0], *local_parts[:-1], local_parts[-1] + ".md").as_posix()
            name, description = metadata["name"], compact(metadata["description"])
            warnings = metadata_warnings(metadata, path.parent.name, body)
            if group == "personalizadas" and warnings:
                raise ValueError(f"Skill personalizada inválida: {path}: {warnings}")
            application = app_name(name, description) if integration else ""
            summary = f"Consultar ou automatizar {application} por Composio; requer ferramentas e permissões verificadas." if integration else SUMMARIES.get(name, description)
            origin_matches = [entry for entry in origins if relative.as_posix().startswith(entry["destination"].rstrip("/") + "/")]
            origin = max(origin_matches, key=lambda item: len(item["destination"])) if origin_matches else {}
            records.append({
                "name": name, "description": description, "summary": summary,
                "group": group, "application": application, "source_relative": relative.as_posix(),
                "source_path": str(path), "source_uri": path.as_uri(), "folder_uri": path.parent.as_uri(),
                "source_sha256": digest(raw), "note": note, "warnings": warnings,
                "repository": origin.get("repository", ""), "snapshot": origin.get("snapshot", ""),
            })
    if not records:
        raise ValueError("Nenhum SKILL.md encontrado nas três pastas de origem esperadas.")
    paths = Counter(record["note"].casefold() for record in records)
    if any(count > 1 for count in paths.values()):
        raise ValueError("Colisão de nomes de notas no catálogo (incluindo diferenças de maiúsculas).")
    return records


def installed_inventory(home: Path) -> dict:
    result = {}
    for scope, folder in (("atual", home / ".agents" / "skills"), ("legado", home / ".codex" / "skills")):
        files = []
        for path in sorted(folder.rglob("SKILL.md")) if folder.exists() else []:
            files.append({"path": str(path), "sha256": digest(path.read_bytes())})
        result[scope] = {"root": str(folder), "count": len(files), "files": files}
    return result


def render_skill(record: dict, siblings: list[dict], installed: dict) -> str:
    metadata = {"tipo": "skill", "nome": record["name"], "colecao": GROUPS[record["group"]][1], "tags": ["codex", "skills", record["group"]]}
    frontmatter = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items())
    lines = ["---", frontmatter, "---", "", f"# {md_text(record['name'])}", "", record["summary"], "", "## Descrição declarada pelo autor", "", "> " + md_text(record["description"]), "", "## Arquivos e procedência", "", f"- [Abrir SKILL.md original]({record['source_uri']})", f"- [Abrir pasta completa e auxiliares]({record['folder_uri']})", f"- Caminho na coleção: `{record['source_relative']}`."]
    if record["repository"]:
        lines += [f"- Repositório: https://github.com/{record['repository']}", f"- Snapshot registrado: `{record['snapshot']}`."]
    else:
        lines += ["- Origem: autoria local; nenhuma publicação externa realizada."]
    copies = [(scope, item["path"]) for scope, inventory in installed.items() for item in inventory["files"] if item["sha256"] == record["source_sha256"]]
    lines += ["", "## Estado observado", ""]
    if copies:
        for scope, path in copies:
            label = "pasta atual de skills do usuário" if scope == "atual" else "pasta .codex/skills (configuração anterior/legado)"
            lines += [f"- Existe um `SKILL.md` idêntico na {label}: `{path}`."]
        lines += ["- A comparação cobre apenas `SKILL.md`, não os auxiliares. Arquivo em disco não comprova carregamento, autenticação ou funcionamento."]
    else:
        lines += ["- Não foi encontrada cópia idêntica de `SKILL.md` nas duas pastas de usuário verificadas; outros escopos ou versões podem existir."]
    lines += ["- Nenhuma instalação ou autorização foi feita durante a criação deste catálogo."]
    if record["group"] == "personalizadas":
        lines += ["- Metadados e estrutura revisados; o fluxo ainda precisa de teste de uso em um exemplo escolhido por você."]
    else:
        lines += ["- Skill de terceiros: instruções e auxiliares não foram auditados integralmente nem executados nesta organização."]
    if record["warnings"]:
        lines += ["", "## Revisar antes de usar", ""] + ["- " + warning for warning in record["warnings"]]
    if siblings:
        lines += ["", "## Outras versões com o mesmo nome", "", "Não instalar todas automaticamente: comparar e escolher a versão desejada.", ""]
        lines += ["- " + wiki(item["note"], item["source_relative"]) for item in siblings]
    valid_name = bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", record["name"])) and len(record["name"]) <= 64
    if valid_name and record["name"] != "template-skill":
        if record["group"] == "integracoes":
            prompt = f"Identifique as ferramentas disponíveis para {record['application']} e as permissões necessárias. Depois da minha autorização, faça somente uma consulta de leitura. Não envie mensagens nem altere dados."
        elif record["group"] == "personalizadas":
            prompt = {
                "obsidian-capturar-conhecimento": "Transforme o texto que vou fornecer em uma nota no cofre autorizado, preservando as fontes e sem inventar informações.",
                "obsidian-organizar-cofre": "Crie um índice das notas da pasta indicada no cofre autorizado, sem mover, excluir ou sobrescrever arquivos existentes.",
                "codex-auditar-skills": "Audite a skill que vou indicar. Leia os arquivos relevantes, não execute scripts e relate riscos com evidências.",
            }.get(record["name"], "Aplique esta skill apenas à tarefa e aos arquivos que eu indicar.")
        else:
            prompt = "Objetivo: " + record["summary"] + " Confirme o escopo e as dependências antes de executar ações."
        lines += ["", "## Exemplo de pedido", "", "Depois de instalar, confirme que a skill aparece em `/skills`:", "", "```text", "$" + record["name"], prompt, "```"]
    lines += ["", "## Navegação", "", "- " + wiki("00 - Inicio.md", "Início"), "- " + wiki("01 - Catalogo completo.md", "Catálogo completo"), "- " + wiki("02 - Instalar e usar.md", "Instalar e usar"), "- " + wiki("05 - Seguranca e integracoes.md", "Segurança e integrações"), ""]
    return "\n".join(lines)


def render_catalog(records: list[dict], source: Path, installed: dict, today: str) -> dict[str, str]:
    counts = Counter(record["group"] for record in records)
    by_name = defaultdict(list)
    for record in records:
        by_name[record["name"]].append(record)
    notes = {record["note"]: render_skill(record, [other for other in by_name[record["name"]] if other["note"] != record["note"]], installed) for record in records}
    index = ["# Catálogo completo", "", f"Inventário gerado em **{today}**, lendo somente as pastas de skills indicadas. São **{len(records)} arquivos SKILL.md** e **{len(by_name)} nomes distintos**; versões repetidas permanecem separadas.", "", "| Coleção | Arquivos |", "| --- | ---: |"]
    index += [f"| {label} | {counts[group]} |" for group, (_, label) in GROUPS.items()]
    index += ["", "Descrições em português são resumos de navegação, não garantias de compatibilidade. Cada nota preserva a descrição original e aponta para os arquivos completos.", "", "> Não instale a coleção inteira automaticamente. Escolha poucas skills relevantes e confirme o que aparece em `/skills`."]
    for group in ("personalizadas", "artigo", "awesome"):
        index += ["", "## " + GROUPS[group][1], "", "| Skill | Para que serve |", "| --- | --- |"]
        index += [f"| {wiki(record['note'], record['name'], in_table=True)} | {table_text(record['summary'])} |" for record in records if record["group"] == group]
    letters = defaultdict(list)
    for record in records:
        if record["group"] == "integracoes":
            first = record["application"][:1].upper()
            letters[first if re.fullmatch("[A-Z]", first) else "0-9"].append(record)
    index += ["", "## Integrações por nome do aplicativo", "", "As notas de integração exigem descoberta das ferramentas reais e autorização separada de cada conta. A presença no catálogo não comprova suporte atual do serviço.", ""]
    for letter, items in sorted(letters.items()):
        note = f"Indices/Integracoes - {letter}.md"
        index += [f"- {wiki(note, letter)} — {len(items)} arquivos."]
        lines = [f"# Integrações — {letter}", "", wiki("01 - Catalogo completo.md", "Voltar ao catálogo"), "", "Todas exigem conferência de ferramentas, contas e permissões antes do uso.", "", "| Aplicativo | Skill |", "| --- | --- |"]
        lines += [f"| {table_text(item['application'])} | {wiki(item['note'], item['name'], in_table=True)} |" for item in sorted(items, key=lambda item: item["application"].casefold())]
        notes[note] = "\n".join(lines) + "\n"
    notes["01 - Catalogo completo.md"] = "\n".join(index) + "\n"
    diagnostic = ["# Fontes e diagnóstico", "", f"Data do inventário: **{today}**.", "", f"- Origem local: `{source}`.", f"- Arquivos de terceiros: **{len(records) - counts['personalizadas']}**.", f"- Skills de autoria local: **{counts['personalizadas']}**.", f"- Nomes repetidos: **{sum(len(items) > 1 for items in by_name.values())}**.", "- Nada foi baixado, instalado, autenticado ou publicado para gerar o catálogo.", "- Somente metadados, caminhos e hashes foram inventariados; isso não é uma auditoria de segurança integral.", "", "## Pastas de usuário observadas", "", "| Escopo | Pasta | Arquivos SKILL.md |", "| --- | --- | ---: |"]
    diagnostic += [f"| {scope} | `{inventory['root']}` | {inventory['count']} |" for scope, inventory in installed.items()]
    diagnostic += ["", "A contagem indica arquivos em disco, não skills carregadas ou integrações conectadas. Não foram consultados tokens, contas nem o conteúdo de config.toml.", "", "## Nomes com mais de uma versão", ""]
    for name, items in sorted(by_name.items()):
        if len(items) > 1:
            diagnostic += [f"### {name}", ""] + ["- " + wiki(item["note"], item["source_relative"]) for item in items] + [""]
    diagnostic += ["## Pontos de estrutura a revisar", ""]
    warnings_found = False
    for record in records:
        if record["warnings"]:
            warnings_found = True
            diagnostic += ["- " + wiki(record["note"], record["name"]) + ": " + " ".join(record["warnings"])]
    if not warnings_found:
        diagnostic += ["Nenhum alerta nas verificações estruturais implementadas."]
    source_file = source / "fontes-download.json"
    if source_file.exists():
        diagnostic += ["", "## Procedência dos downloads", "", f"[Abrir fontes-download.json]({source_file.as_uri()}). Snapshots e hashes de downloads são registros anteriores; os arquivos ZIP não foram baixados novamente nem revalidados."]
    activation = source / "ATIVAR-INTEGRACOES.md"
    if activation.exists():
        diagnostic += ["", f"[Abrir registro anterior de integrações]({activation.as_uri()}). Esse documento relata configuração e autorização pendente de uma tarefa anterior; não é uma verificação do estado atual da conexão."]
    diagnostic += ["", "## Referências oficiais consultadas", "", "- https://developers.openai.com/codex/build-skills", "- https://agentskills.io/specification", "", "As instruções deste catálogo foram preparadas em 2026-11-18. Antes de mudar instalações ou endpoints, confira a documentação vigente.", ""]
    notes["08 - Fontes e diagnostico.md"] = "\n".join(diagnostic)
    data = {"schema_version": 1, "generated_on": today, "source_root": str(source), "counts": dict(counts), "distinct_names": len(by_name), "skills": records, "installed_observation": {scope: {key: value for key, value in inventory.items() if key != "files"} for scope, inventory in installed.items()}}
    notes["Suporte/catalogo.json"] = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    return notes


def load_guides(source: Path, vault: Path, records: list[dict], today: str) -> dict[str, str]:
    counts = Counter(record["group"] for record in records)
    replacements = {
        "date": today, "count_originals": str(len(records) - counts["personalizadas"]),
        "count_total": str(len(records)), "count_custom": str(counts["personalizadas"]),
        "source_root": str(source), "source_uri": source.as_uri(),
        "script_ps": ps_quote(source / "ferramentas" / "catalogar_obsidian.py"),
        "tests_ps": ps_quote(source / "ferramentas" / "test_catalogar_obsidian.py"),
        "source_ps": ps_quote(source), "vault_ps": ps_quote(vault),
        "example_skill_ps": ps_quote(source / "skills-personalizadas" / "obsidian-organizar-cofre"),
    }
    notes = {}
    for template in sorted((Path(__file__).parent / "modelos-obsidian").glob("*.md")):
        text = template.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace("{{" + key + "}}", value)
        if re.search(r"\{\{[a-z_]+\}\}", text):
            raise ValueError(f"Variável não preenchida no guia: {template}")
        notes[template.name] = text
    return notes


def safe_target(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts or "\\" in relative or ":" in relative:
        raise ValueError(f"Caminho de saída inválido: {relative}")
    path = root.joinpath(*rel.parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Saída escapa da pasta autorizada: {relative}")
    return path


def apply_notes(root: Path, notes: dict[str, str], write: bool, today: str) -> dict:
    if root.is_symlink() or root.is_junction():
        raise ValueError("A pasta de saída não pode ser um link simbólico ou junction.")
    if len({relative.casefold() for relative in notes}) != len(notes):
        raise ValueError("Colisão de caminhos de saída no Windows.")
    manifest_path = safe_target(root, MANIFEST)
    old_files = {}
    if manifest_path.exists():
        old_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if old_manifest.get("generator") != "catalogar_obsidian.py" or not isinstance(old_manifest.get("files"), dict):
            raise ValueError("Manifesto desconhecido; preservar e revisar antes de continuar.")
        old_files = old_manifest["files"]
    desired = {relative: text.replace("\r\n", "\n").encode("utf-8") for relative, text in notes.items()}
    new_manifest = {"generator": "catalogar_obsidian.py", "schema_version": 1, "generated_on": today, "files": {relative: digest(raw) for relative, raw in sorted(desired.items())}}
    desired[MANIFEST] = (json.dumps(new_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    changes, conflicts, observed = {}, [], {}
    for relative, raw in desired.items():
        target = safe_target(root, relative)
        if target.exists() and not target.is_file():
            conflicts.append(relative)
            continue
        before = target.read_bytes() if target.exists() else None
        observed[relative] = before
        if before == raw:
            continue
        if before is not None and relative != MANIFEST and digest(before) != old_files.get(relative):
            conflicts.append(relative)
        else:
            changes[relative] = raw
    if conflicts:
        raise ValueError("Arquivos existentes ou editados manualmente foram preservados. Conflitos: " + ", ".join(conflicts[:12]))
    if write:
        for relative, raw in changes.items():
            target = safe_target(root, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            current = target.read_bytes() if target.exists() else None
            if current != observed[relative]:
                raise ValueError(f"Arquivo mudou durante a geração; operação interrompida: {relative}")
            if current is None:
                with target.open("xb") as stream:
                    stream.write(raw)
            else:
                target.write_bytes(raw)
    return {"write": write, "managed_files": len(notes), "pending_files": len(changes), "preserved_stale_paths": sorted(set(old_files) - set(notes)), "output": str(root)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--vault", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Gravar após conferir conflitos. Sem esta opção, apenas simular.")
    mode.add_argument("--check", action="store_true", help="Simular e falhar se os arquivos gerados estiverem desatualizados.")
    args = parser.parse_args()
    source, vault = args.source_root.resolve(), args.vault.resolve()
    if not vault.is_dir() or not (vault / ".obsidian").is_dir():
        parser.error("Informe uma pasta de cofre existente que contenha .obsidian.")
    try:
        today = date.today().isoformat()
        records = collect_records(source)
        notes = render_catalog(records, source, installed_inventory(Path.home()), today)
        notes.update(load_guides(source, vault, records, today))
        result = apply_notes(vault / FOLDER, notes, args.write, today)
        result["skill_files"] = len(records)
        result["distinct_names"] = len({record["name"] for record in records})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.check and result["pending_files"] else 0
    except (ValueError, OSError, UnicodeError) as error:
        print(f"Catálogo não concluído: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
