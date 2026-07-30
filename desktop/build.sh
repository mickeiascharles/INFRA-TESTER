#!/usr/bin/env bash
# Empacota o app desktop com PyInstaller.
#
# --collect-all robot / SeleniumLibrary / selenium é obrigatório: o Robot
# Framework carrega BuiltIn, SeleniumLibrary e outras libs dinamicamente por
# nome (não via "import" estático), então o analisador do PyInstaller não as
# detecta sozinho e o binário falha em tempo de execução com
# "Importing library 'robot.libraries.BuiltIn' failed" se essas flags forem
# omitidas.
set -euo pipefail
cd "$(dirname "$0")"

.venv/bin/pyinstaller --noconfirm --clean --name SiscorpPCA \
  --add-data "../robot/cadastrar_pca.robot:robot" \
  --collect-all robot \
  --collect-all SeleniumLibrary \
  --collect-all selenium \
  main.py
