"""Busca local, somente leitura, na memória autorizada do projeto (sem rede)."""

import argparse
import json
import re
import unicodedata
from pathlib import Path


DEFAULT_MEMORY = (Path.home() / 'OneDrive' / 'Área de Trabalho' / 'Jonas Volt'
                  / 'Skills para Codex' / 'Suporte')
ALLOWED_NOTES = ('Memoria - LoopTech Jr.md',
                 'Conversa - LoopTech Jr - Fonte de contexto.md')


def tokens(text):
    normalized = unicodedata.normalize('NFKD', text.casefold())
    plain = ''.join(c for c in normalized if not unicodedata.combining(c))
    return set(re.findall(r'[a-z0-9]+', plain))


def search(directory, query, limit=5):
    terms = tokens(query)
    matches = []
    for name in ALLOWED_NOTES:
        path = directory / name
        # Do not follow links to files outside the authorized notes directory.
        if path.is_symlink() or not path.is_file():
            continue
        if not path.resolve().is_relative_to(directory.resolve()):
            continue
        lines = path.read_text(encoding='utf-8-sig').splitlines()
        # Small chunks keep context and line citations without loading the vault.
        for start in range(0, len(lines), 12):
            text = '\n'.join(lines[start:start + 12])
            score = len(terms & tokens(text))
            if score:
                matches.append(dict(source=str(path), line_start=start + 1,
                                    line_end=min(start + 12, len(lines)),
                                    score=score, text=text))
    return sorted(matches, key=lambda item: (-item['score'], item['source'],
                                            item['line_start']))[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', help='Palavras a procurar; busca lexical sem acentos.')
    parser.add_argument('--memory-dir', type=Path, default=DEFAULT_MEMORY)
    parser.add_argument('--limit', type=int, default=5)
    args = parser.parse_args()
    if not args.memory_dir.is_dir():
        parser.error('Pasta de memória inacessível: ' + str(args.memory_dir))
    if not 1 <= args.limit <= 20:
        parser.error('--limit deve estar entre 1 e 20')
    if not tokens(args.query):
        parser.error('Informe ao menos uma palavra de busca')
    if not any((args.memory_dir / name).is_file() for name in ALLOWED_NOTES):
        parser.error('Nenhuma nota de memória autorizada foi encontrada')
    print(json.dumps(dict(method='busca lexical local; sem embeddings',
                          results=search(args.memory_dir, args.query, args.limit)),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
