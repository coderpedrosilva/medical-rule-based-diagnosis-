import os

def export_prism_rules(prism_model, path="reports/rules.txt"):
    folder = os.path.dirname(path)

    # cria a pasta se não existir
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(path, "w", encoding="utf-8") as f:
        for i, (attr, val, target) in enumerate(prism_model.rules, 1):
            rule = f"REGRA {i}: SE {attr} == {val} ENTÃO diabetes = {target}\n"
            f.write(rule)
