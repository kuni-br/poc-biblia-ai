import json

with open("data/pt_aa.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

saida = []

for livro in data:
    nome_livro = livro["name"]

    for cap_idx, capitulo in enumerate(livro["chapters"], start=1):
        for ver_idx, texto in enumerate(capitulo, start=1):
            saida.append({
                "livro": nome_livro,
                "capitulo": cap_idx,
                "versiculo": ver_idx,
                "texto": texto
            })

with open("data/biblia_ara.json", "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)