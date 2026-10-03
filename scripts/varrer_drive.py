#!/usr/bin/env python3
"""Varre recursivamente uma pasta pública do Google Drive (link "qualquer pessoa").

Usa a visão embutida do Drive (embeddedfolderview), que não exige login nem chave de API.
Grava um JSONL com uma linha por item: caminho, id, tipo, data de modificação e link.

Uso:
    python3 scripts/varrer_drive.py <id_da_pasta_raiz> <saida.jsonl> [--prefixo "GC "]
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://drive.google.com/embeddedfolderview?id={}"
ENTRY_RE = re.compile(
    r'<div class="flip-entry" id="entry-(?P<id>[^"]+)".*?'
    r'<a href="(?P<href>[^"]+)".*?'
    r'<div class="flip-entry-title">(?P<title>.*?)</div>.*?'
    r'<div class="flip-entry-last-modified"><div>(?P<mod>.*?)</div>',
    re.S,
)


def baixar(folder_id, tentativas=5):
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(URL.format(folder_id), timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # rede instável: tenta de novo com espera crescente
            if i == tentativas - 1:
                raise
            time.sleep(2 ** i)


def tipo_do_link(href):
    if "/drive/folders/" in href:
        return "pasta"
    m = re.search(r"docs\.google\.com/(\w+)/", href)
    if m:
        return "google-" + m.group(1)
    return "arquivo"


def listar(folder_id):
    entradas = []
    for m in ENTRY_RE.finditer(baixar(folder_id)):
        href = html.unescape(m.group("href"))
        entradas.append({
            "id": m.group("id"),
            "nome": html.unescape(m.group("title")),
            "tipo": tipo_do_link(href),
            "modificado": m.group("mod"),
            "link": href,
        })
    return entradas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raiz")
    ap.add_argument("saida")
    ap.add_argument("--prefixo", default="", help="no 1º nível, só desce em pastas com este prefixo")
    ap.add_argument("--threads", type=int, default=12)
    a = ap.parse_args()

    raiz = [e for e in listar(a.raiz)
            if e["tipo"] == "pasta" and e["nome"].startswith(a.prefixo)]
    fila = [(e, e["nome"], 1) for e in raiz]
    total = 0
    erros = []
    with open(a.saida, "w", encoding="utf-8") as out, ThreadPoolExecutor(a.threads) as ex:
        for e, caminho, nivel in fila:
            out.write(json.dumps({**e, "caminho": caminho, "nivel": nivel, "pai": ""}, ensure_ascii=False) + "\n")
        while fila:
            pastas = [(e, c, n) for e, c, n in fila if e["tipo"] == "pasta"]
            futuros = {ex.submit(listar, e["id"]): (e, c, n) for e, c, n in pastas}
            fila = []
            for fut, (e, caminho, nivel) in futuros.items():
                try:
                    filhos = fut.result()
                except Exception as err:
                    erros.append((caminho, str(err)))
                    continue
                for f in filhos:
                    c = caminho + " / " + f["nome"]
                    out.write(json.dumps({**f, "caminho": c, "nivel": nivel + 1, "pai": e["id"]},
                                         ensure_ascii=False) + "\n")
                    total += 1
                    fila.append((f, c, nivel + 1))
            print(f"nível concluído: {total} itens até agora, {len(fila)} na próxima rodada", file=sys.stderr)
    for c, err in erros:
        print("ERRO", c, err, file=sys.stderr)
    print(f"total {total} itens, {len(erros)} erros", file=sys.stderr)


if __name__ == "__main__":
    main()
