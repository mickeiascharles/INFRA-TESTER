STYLESHEET = """
QWidget {
    background: #121316;
    color: #e7e8ea;
    font-family: -apple-system, "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

/* ---------- Tela de login ---------- */

#tela-login {
    background: #121316;
}

#cartao-login {
    background: #1a1b1f;
    border: 1px solid #2b2d33;
    border-radius: 12px;
}

#marca-login {
    background: #1fa971;
    border-radius: 8px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
}

#marca-login-titulo {
    font-size: 15px;
    font-weight: 700;
    color: #f2f3f4;
}

#marca-login-subtitulo {
    font-size: 11px;
    color: #85878f;
    font-family: ui-monospace, Consolas, monospace;
}

#login-descricao {
    color: #9a9ba3;
    margin-top: 6px;
    margin-bottom: 4px;
}

#login-rodape {
    color: #c99a3a;
    font-size: 11px;
    margin-top: 8px;
}

/* ---------- Cabeçalho de passo (breadcrumb + título) ---------- */

#breadcrumb {
    font-size: 11px;
    font-weight: 700;
    color: #6f8bff;
    letter-spacing: 0.5px;
}

#breadcrumb-slug {
    color: #4c8dff;
}

#titulo-pagina {
    font-size: 20px;
    font-weight: 700;
    color: #f2f3f4;
}

#passo-badge {
    background: transparent;
    border: 1px solid #34353b;
    border-radius: 10px;
    padding: 2px 10px;
    color: #9a9ba3;
    font-family: ui-monospace, Consolas, monospace;
    font-size: 11px;
    margin-left: 8px;
}

#subtitulo-pagina {
    color: #85878f;
    margin-bottom: 8px;
}

#subtitulo {
    font-size: 11px;
    font-weight: 700;
    color: #6f8bff;
    letter-spacing: 0.5px;
    margin-top: 8px;
}

#dica {
    color: #85878f;
    font-size: 11px;
}

#dica-mono {
    color: #7d8794;
    font-size: 11px;
    font-family: ui-monospace, Consolas, monospace;
    padding: 6px 0 2px 0;
}

#cartao {
    background: #1a1b1f;
    border: 1px solid #2b2d33;
    border-radius: 10px;
}

QLineEdit, QComboBox, QPlainTextEdit, QDateEdit {
    background: #202126;
    color: #e7e8ea;
    border: 1px solid #34353b;
    border-radius: 6px;
    padding: 6px 8px;
    selection-background-color: #2f6fed;
}

QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QDateEdit:focus {
    border: 1px solid #4c8dff;
}

QComboBox::drop-down {
    border: none;
}

QLabel {
    background: transparent;
}

QPushButton#botao-primario {
    background: #2f6fed;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 9px 22px;
    font-weight: 600;
}

QPushButton#botao-primario:hover {
    background: #2457c9;
}

QPushButton#botao-primario:disabled {
    background: #35404f;
    color: #7c8593;
}

QPushButton#botao-executar {
    background: #17a34a;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 9px 22px;
    font-weight: 700;
}

QPushButton#botao-executar:hover {
    background: #128a3e;
}

QPushButton#botao-executar:disabled {
    background: #2a3a30;
    color: #7c8593;
}

QPushButton#botao-secundario {
    background: transparent;
    color: #d6d8dc;
    border: 1px solid #34353b;
    border-radius: 6px;
    padding: 9px 18px;
}

QPushButton#botao-secundario:hover {
    border: 1px solid #4c8dff;
    color: #ffffff;
}

QPushButton#botao-secundario:disabled {
    color: #5b5d66;
}

QLabel#passo-pill {
    background: transparent;
    border: 1px solid #34353b;
    border-radius: 12px;
    padding: 6px 14px;
    color: #85878f;
    margin-right: 4px;
    font-size: 11px;
}

QLabel#passo-pill[estado="atual"] {
    border: 1px solid #4c8dff;
    color: #cfe0ff;
    font-weight: 700;
}

QLabel#passo-pill[estado="concluido"] {
    border: 1px solid #1fa971;
    color: #59d69a;
}

#alerta-erro {
    background: rgba(239, 68, 68, 0.12);
    color: #f28b82;
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 6px;
    padding: 10px 14px;
}

#barra-lateral {
    background: #17181c;
    border-right: 1px solid #24252a;
}

#marca {
    color: #f2f3f4;
    font-weight: 700;
    font-size: 15px;
}

QPushButton#nav-botao {
    background: transparent;
    color: #9a9ba3;
    border: none;
    text-align: left;
    padding: 14px 22px;
    font-size: 13px;
}

QPushButton#nav-botao:hover {
    background: rgba(255, 255, 255, 0.05);
    color: #e7e8ea;
}

QPushButton#nav-botao:checked {
    background: rgba(76, 141, 255, 0.12);
    color: #ffffff;
    font-weight: 700;
    border-left: 3px solid #4c8dff;
}

QPushButton#nav-botao-sair {
    background: transparent;
    color: #7d8794;
    border: none;
    text-align: left;
    padding: 12px 22px;
    font-size: 12px;
}

QPushButton#nav-botao-sair:hover {
    color: #f28b82;
}

#rodape-lateral {
    color: #5b5d66;
    font-size: 11px;
    padding: 16px 22px;
}

QTableWidget {
    background: #1a1b1f;
    border: 1px solid #2b2d33;
    border-radius: 8px;
    gridline-color: #24252a;
    color: #e7e8ea;
}

QHeaderView::section {
    background: #202126;
    color: #9a9ba3;
    padding: 6px 8px;
    border: none;
    font-weight: 600;
}

#console {
    background: #0c0d0f;
    color: #d7e0f0;
    border: 1px solid #2b2d33;
    border-radius: 8px;
    font-family: ui-monospace, Consolas, monospace;
    font-size: 12px;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #34353b;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #454650;
}

/* ---------- Tela de laudo (resultado da execução) ---------- */

#status-badge {
    border-radius: 8px;
    padding: 12px 16px;
}

#status-badge[estado="sucesso"] {
    background: rgba(23, 163, 74, 0.12);
    border: 1px solid rgba(23, 163, 74, 0.4);
}

#status-badge[estado="falha"] {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.4);
}

#status-badge[estado="executando"] {
    background: rgba(76, 141, 255, 0.12);
    border: 1px solid rgba(76, 141, 255, 0.4);
}

#status-badge-titulo {
    font-size: 15px;
    font-weight: 700;
}

#status-badge-titulo[estado="sucesso"] {
    color: #59d69a;
}

#status-badge-titulo[estado="falha"] {
    color: #f28b82;
}

#status-badge-titulo[estado="executando"] {
    color: #8fb6ff;
}

#status-badge-subtitulo {
    color: #9a9ba3;
    font-size: 12px;
}

#tile {
    background: #1a1b1f;
    border: 1px solid #2b2d33;
    border-radius: 8px;
}

#tile-valor {
    font-size: 22px;
    font-weight: 700;
    color: #f2f3f4;
    font-family: ui-monospace, Consolas, monospace;
}

#tile-legenda {
    color: #85878f;
    font-size: 11px;
}

#artefato-nome {
    color: #d6d8dc;
    font-family: ui-monospace, Consolas, monospace;
    font-size: 12px;
}
"""
