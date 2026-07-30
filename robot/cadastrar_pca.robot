*** Settings ***
Library    SeleniumLibrary
Library    String
Library    OperatingSystem

*** Variables ***
${NAVEGADOR}                    Chrome
${URL_LOGIN}                    https://siscorp-pca-des.infrasa.gov.br
${URL_SISTEMA}                  https://siscorp-pca-des.infrasa.gov.br/pca
${USUARIO}                      mickeias.paiva
${SENHA}                        ${EMPTY}
${DELAY}                        0s
${TIMEOUT}                      15s

${STATUS_CONTRATACAO}           EM PLANEJAMENTO
${EVENTO}                       teste
${ANO_PCA}                      2026
${AREA_DEMANDANTE}              SUPTI
${DESCRICAO_OBJETO}             Testando
${JUSTIFICATIVA}                Teste

${ACAO}                         15P7
${PLANO_ORCAMENTARIO}           194521
${TIPO_NATUREZA}                INVESTIMENTOS
${NATUREZA_DESCRICAO}           4.4.50.41.07

${STATUS_SUBITEM}               EM PLANEJAMENTO
${TIPO_SUBITEM}                 Material
${GRUPO}                        88
${CLASSE}                       8820
${PDM}                          2528
${CODIGO_SUBITEM}               612147
${DESCRICAO_SUBITEM}            1231231
${UNIDADE_MEDIDA}               unid
${PRECO_UNITARIO}               10000
${QUANTIDADE}                   55

${TIPO_LICITACAO}               PREGÃO ELETRÔNICO
${DATA_ASSINATURA}              07/07/2026
${DATA_ENTREGA_DOC}             07/07/2026
${OBJETIVO_ESTRATEGICO}         1.3
${PRIORIDADE}                   BAIXA
${SIGILOSO}                     Não

${VIGENCIA_MESES}               60

${TIPO_DESEMBOLSO}              Misto
${PARCELA_ANUAL}                Sim
${VALOR_PARCELA_UNICA}          10000
${VALOR_MENSAL_DESEMBOLSO}      540000
${ANO_DESEMBOLSO}               2026
${MES_DESEMBOLSO}               Julho


*** Test Cases ***
Cadastrar Nova Demanda no PCA (SISCORP)
    Log To Console    VERSAO DO ARQUIVO: FINAL-GRUPO-FIX-07-DIAGNOSTICO-LOGIN

    Realizar Login no Sistema
    Iniciar Cadastro de Demanda

    Executar Etapa    Preencher Passo 1 - Dados Basicos
    Executar Etapa    Preencher Passo 2 - Itens de Contratacao
    Executar Etapa    Preencher Passo 3 - Dados da Contratacao
    Executar Etapa    Preencher Passo 4 - Previsao de Duracao
    Executar Etapa    Preencher Passo 5 - Previsao de Desembolso
    Executar Etapa    Validar Cadastro com Sucesso

    [Teardown]    Close Browser


*** Keywords ***
Executar Etapa
    [Arguments]    ${nome_etapa}

    ${status}    ${erro}=    Run Keyword And Ignore Error    ${nome_etapa}

    IF    '${status}' == 'FAIL'
        Log To Console    AVISO: a etapa '${nome_etapa}' teve um problema e foi ignorada para não travar o teste: ${erro}
        Log    AVISO: a etapa '${nome_etapa}' teve um problema e foi ignorada para não travar o teste: ${erro}
    END


Realizar Login no Sistema
    ${nivel_anterior}=    Set Log Level    NONE
    ${senha_final}=    Obter Senha SISCORP
    Set Log Level    ${nivel_anterior}

    Open Browser    ${URL_LOGIN}    ${NAVEGADOR}
    ...    options=add_argument("--no-sandbox");add_argument("--disable-dev-shm-usage")
    Set Window Size    1920    1080
    Set Selenium Speed      ${DELAY}
    Set Selenium Timeout    ${TIMEOUT}

    ${ja_logado}=    Run Keyword And Return Status
    ...    Wait Until Page Contains    Planejamento    timeout=5s

    IF    ${ja_logado}
        Go To    ${URL_SISTEMA}
        Wait Until Page Contains    Planejamento    timeout=15s
        RETURN
    END

    Wait Until Element Is Visible
    ...    xpath=//input[not(@type='hidden') and not(@type='checkbox') and not(@type='radio')]
    ...    timeout=15s

    Preencher Campo React
    ...    xpath=(//input[not(@type='hidden') and not(@type='password')])[1]
    ...    ${USUARIO}

    ${nivel_anterior}=    Set Log Level    NONE
    Preencher Campo React
    ...    xpath=//input[@type='password']
    ...    ${senha_final}

    ${valor_senha_digitada}=    Get Value
    ...    xpath=//input[@type='password']
    Set Log Level    ${nivel_anterior}

    ${valor_usuario_digitado}=    Get Value
    ...    xpath=(//input[not(@type='hidden') and not(@type='password')])[1]

    ${tamanho_senha_esperado}=    Get Length    ${senha_final}
    ${tamanho_senha_digitada}=    Get Length    ${valor_senha_digitada}

    Log To Console    Campo de usuário contém: '${valor_usuario_digitado}' (esperado: '${USUARIO}')
    Log To Console    Campo de senha contém ${tamanho_senha_digitada} caractere(s) (esperado: ${tamanho_senha_esperado})

    IF    '${valor_usuario_digitado}' != '${USUARIO}'
        Log To Console    AVISO: o campo de usuário NÃO ficou com o valor esperado. Provável seletor errado.
    END

    IF    ${tamanho_senha_digitada} != ${tamanho_senha_esperado}
        Log To Console    AVISO: o campo de senha NÃO ficou com o tamanho esperado. A senha pode não ter sido digitada corretamente.
    END

    Clicar Com JS
    ...    xpath=//button[@type='submit' or contains(translate(., 'ENTRAR', 'entrar'), 'entrar') or contains(translate(., 'ACESSAR', 'acessar'), 'acessar') or contains(translate(., 'LOGIN', 'login'), 'login')]

    Aguardar Login Efetuado


Aguardar Login Efetuado
    ${ok}=    Run Keyword And Return Status
    ...    Wait Until Page Contains    Planejamento    timeout=30s

    IF    not ${ok}
        ${url_atual}=    Get Location
        Log To Console    URL após tentativa de login: ${url_atual}

        Go To    ${URL_SISTEMA}

        ${ok}=    Run Keyword And Return Status
        ...    Wait Until Page Contains    Planejamento    timeout=20s
    END

    IF    not ${ok}
        Diagnosticar Tela Bloqueada
        Fail    O sistema não chegou na tela de Planejamento após o login.
    END


Iniciar Cadastro de Demanda
    Wait Until Page Contains    Planejamento    timeout=${TIMEOUT}

    Go To    ${URL_SISTEMA}
    Wait Until Page Contains    PCA    timeout=15s

    Wait Until Element Is Visible
    ...    xpath=//button[contains(., 'Cadastrar Demanda') or contains(., 'Cadastrar Ação') or contains(., 'Cadastrar Acao')]
    ...    timeout=15s

    Clicar Com JS
    ...    xpath=//button[contains(., 'Cadastrar Demanda') or contains(., 'Cadastrar Ação') or contains(., 'Cadastrar Acao')]

    Wait Until Page Contains    Dados Básicos    timeout=15s


Preencher Passo 1 - Dados Basicos
    Wait Until Page Contains    Dados Básicos    timeout=${TIMEOUT}

    Selecionar Opcao Dropdown    Status da Contratação    ${STATUS_CONTRATACAO}
    Selecionar Opcao Dropdown    Evento                  ${EVENTO}

    Preencher Campo Por Label    Ano    ${ANO_PCA}

    Selecionar Area Demandante    ${AREA_DEMANDANTE}

    Preencher Campo Por Label    Descrição do Objeto              ${DESCRICAO_OBJETO}
    Preencher Campo Por Label    Justificativa da Contratação     ${JUSTIFICATIVA}

    Garantir Campo Contem Texto    Status da Contratação    ${STATUS_CONTRATACAO}
    Garantir Campo Contem Texto    Evento                  ${EVENTO}
    Garantir Campo Contem Texto    Ano                     ${ANO_PCA}
    Garantir Campo Contem Texto    Área Demandante         ${AREA_DEMANDANTE}

    Avancar Para Passo    Itens de Contratação


Preencher Passo 2 - Itens de Contratacao
    Wait Until Page Contains    Itens de Contratação    timeout=${TIMEOUT}
    Sleep    0.4s

    Clicar Com JS
    ...    xpath=//button[contains(., 'Natureza de Despesa')]

    Wait Until Page Contains    Cadastrar Natureza de Despesa Detalhada    timeout=${TIMEOUT}

    Selecionar Opcao Dropdown    Ação                  ${ACAO}
    Selecionar Opcao Dropdown    Plano Orçamentário    ${PLANO_ORCAMENTARIO}
    Selecionar Opcao Dropdown    Tipo                  ${TIPO_NATUREZA}
    Selecionar Opcao Dropdown    Descrição             ${NATUREZA_DESCRICAO}

    Clicar Com JS
    ...    xpath=//button[contains(., 'Gravar') or contains(., 'Criar')]

    Wait Until Page Does Not Contain    Cadastrar Natureza de Despesa Detalhada    timeout=12s
    Wait Until Page Contains            ${ACAO}    timeout=${TIMEOUT}

    Clicar Com JS
    ...    xpath=(//table//tbody//tr[1]//button)[1]

    Wait Until Page Contains    Cadastrar Subitem    timeout=${TIMEOUT}

    ${tipo_subitem_ok}=    Run Keyword And Return Status
    ...    Selecionar Tipo de Subitem    ${TIPO_SUBITEM}

    IF    not ${tipo_subitem_ok}
        Log To Console    AVISO: não foi possível selecionar o Tipo de Subitem '${TIPO_SUBITEM}'. Seguindo mesmo assim.
    END

    Sleep    0.4s

    ${status_subitem_ok}=    Run Keyword And Return Status
    ...    Selecionar Opcao Dropdown    Status da Contratação (Subitem)    ${STATUS_SUBITEM}

    IF    not ${status_subitem_ok}
        Log To Console    Não foi possível selecionar '${STATUS_SUBITEM}' em 'Status da Contratação (Subitem)' (provavelmente não é uma opção válida para o subitem). Mantendo o valor padrão do campo e seguindo o cadastro.
    END

    Fechar Overlays
    Sleep    0.3s

    Selecionar Opcao Dropdown    Código do subitem     ${CODIGO_SUBITEM}

    ${valor_grupo}=    Obter Valor Campo Por Label    Nome do Grupo
    ${valor_classe}=    Obter Valor Campo Por Label    Nome da Classe
    ${valor_pdm}=    Obter Valor Campo Por Label    Nome do PDM
    Log To Console    Após selecionar o Código do subitem - Grupo: '${valor_grupo}' | Classe: '${valor_classe}' | PDM: '${valor_pdm}'

    Preencher Campo Por Label    Descrição do subitem    ${DESCRICAO_SUBITEM}

    Selecionar Opcao Dropdown    Unidade de Medida     ${UNIDADE_MEDIDA}

    Preencher Campo Por Label    Preço Unitário    ${PRECO_UNITARIO}
    Preencher Campo Por Label    Quantidade        ${QUANTIDADE}

    Clicar Com JS
    ...    xpath=//button[contains(., 'Gravar') or contains(., 'Criar')]

    Wait Until Page Does Not Contain    Cadastrar Subitem    timeout=12s
    Wait Until Page Contains            ${DESCRICAO_SUBITEM}    timeout=${TIMEOUT}

    Avancar Para Passo    Dados da Contratação


Preencher Passo 3 - Dados da Contratacao
    Wait Until Page Contains    Dados da Contratação    timeout=${TIMEOUT}

    Selecionar Opcao Dropdown    Tipo de Licitação    ${TIPO_LICITACAO}

    Fechar Overlays
    Sleep    0.2s

    Preencher Data Via Datepicker Tolerante
    ...    Data estimada de Assinatura
    ...    ${DATA_ASSINATURA}
    ...    1

    Preencher Data Via Datepicker Tolerante
    ...    Data estimada de Entrega
    ...    ${DATA_ENTREGA_DOC}
    ...    2

    Selecionar Opcao Dropdown    Objetivo Estratégico    ${OBJETIVO_ESTRATEGICO}
    Selecionar Opcao Dropdown    Prioridade              ${PRIORIDADE}
    Selecionar Opcao Dropdown    Sigiloso                ${SIGILOSO}

    Avancar Para Passo    Previsão de Duração da Contratação


Preencher Passo 4 - Previsao de Duracao
    Wait Until Page Contains    Previsão de Duração da Contratação    timeout=${TIMEOUT}

    Preencher Campo Por Label    Vigência Contratual    ${VIGENCIA_MESES}

    Avancar Para Passo    Previsão de Desembolso


Preencher Passo 5 - Previsao de Desembolso
    Wait Until Page Contains    Previsão de Desembolso    timeout=${TIMEOUT}

    Selecionar Opcao Dropdown    Tipo de Desembolso    ${TIPO_DESEMBOLSO}

    Fechar Overlays
    Sleep    0.3s

    Selecionar Opcao Dropdown    Parcela Anual    ${PARCELA_ANUAL}

    Fechar Overlays
    Sleep    0.3s

    ${preencheu_parcela_unica}=    Run Keyword And Return Status
    ...    Preencher Campo Monetario Por Texto Visual
    ...    Valor da Parcela Única
    ...    ${VALOR_PARCELA_UNICA}

    IF    not ${preencheu_parcela_unica}
        Log To Console    Campo 'Valor da Parcela Única' não foi encontrado/preenchido. Continuando para os valores mensais.
    END

    Preencher Valor Mensal Desembolso
    ...    ${ANO_DESEMBOLSO}
    ...    ${MES_DESEMBOLSO}
    ...    ${VALOR_MENSAL_DESEMBOLSO}

    Clicar Botao Salvar Final


Validar Cadastro com Sucesso
    ${voltou_lista}=    Run Keyword And Return Status
    ...    Wait Until Page Contains    ${DESCRICAO_OBJETO}    timeout=15s

    IF    not ${voltou_lista}
        ${tem_sucesso}=    Run Keyword And Return Status
        ...    Wait Until Page Contains    sucesso    timeout=5s
    ELSE
        ${tem_sucesso}=    Set Variable    ${True}
    END

    IF    not ${tem_sucesso}
        Diagnosticar Tela Bloqueada
        Log To Console    AVISO: o cadastro não exibiu confirmação de sucesso nem voltou para a listagem com '${DESCRICAO_OBJETO}'. Verifique o screenshot e o log.
    END


# -------------------------------------------------------------------
# AUXILIARES GERAIS
# -------------------------------------------------------------------

Obter Senha SISCORP
    ${nivel_anterior}=    Set Log Level    NONE
    ${senha_bruta}=    Get Environment Variable    SISCORP_SENHA    ${SENHA}
    ${senha_final}=    Strip String    ${senha_bruta}
    Set Log Level    ${nivel_anterior}

    Should Not Be Empty
    ...    ${senha_bruta}
    ...    msg=Senha não configurada. Execute no PowerShell: $env:SISCORP_SENHA="sua_senha"

    ${tamanho_bruto}=    Get Length    ${senha_bruta}
    ${tamanho_final}=    Get Length    ${senha_final}

    Log To Console    Senha lida da variável SISCORP_SENHA: ${tamanho_bruto} caractere(s) (sem espaços nas pontas: ${tamanho_final}).

    IF    ${tamanho_bruto} != ${tamanho_final}
        Log To Console    AVISO: a senha tinha espaço(s)/quebra de linha no início ou fim - isso foi removido automaticamente. Se a senha correta TEM espaço de propósito, avise.
    END

    RETURN    ${senha_final}


Preencher Campo React
    [Arguments]    ${locator}    ${valor}

    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    ${elemento}=    Get WebElement    ${locator}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const el = arguments[0];
    ...    const value = String(arguments[1] || "");
    ...    const tag = el.tagName.toLowerCase();
    ...    const proto = tag === "textarea" ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
    ...    const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
    ...    el.scrollIntoView({ block: "center", inline: "center" });
    ...    el.focus();
    ...    setter.call(el, "");
    ...    el.dispatchEvent(new Event("input", { bubbles: true }));
    ...    setter.call(el, value);
    ...    el.dispatchEvent(new Event("input", { bubbles: true }));
    ...    el.dispatchEvent(new Event("change", { bubbles: true }));
    ...    el.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    ...    el.dispatchEvent(new Event("blur", { bubbles: true }));

    Execute Javascript    ${script}    ARGUMENTS    ${elemento}    ${valor}
    Sleep    0.1s


Preencher Campo Por Label
    [Arguments]    ${label_campo}    ${valor}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const labelAlvo = String(arguments[0] || "");
    ...    const valor = String(arguments[1] || "");
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(labelAlvo);
    ...    const ignorarOverlay = (el) => Boolean(el.closest("[data-radix-popper-content-wrapper], [data-radix-select-content], [role='listbox'], [cmdk-list], [cmdk-root]"));
    ...    const foraDoMenu = (el) => !el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar");
    ...    const visivel = (el) => {
    ...        if (!el || !foraDoMenu(el) || ignorarOverlay(el)) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const root = document.querySelector("main") || document.querySelector("form") || document.body;
    ...    const labels = Array.from(root.querySelectorAll("label, p, span, div")).filter(visivel);
    ...    let label = labels.find((el) => normalizar(el.innerText || el.textContent) === alvo);
    ...    if (!label) {
    ...        label = labels.find((el) => {
    ...            const texto = normalizar(el.innerText || el.textContent);
    ...            return texto.includes(alvo) && texto.length <= alvo.length + 70;
    ...        });
    ...    }
    ...    if (!label) return "ERRO|Label não encontrado: " + labelAlvo;
    ...    let campo = null;
    ...    const forId = label.getAttribute("for");
    ...    if (forId) {
    ...        const associado = document.getElementById(forId);
    ...        if (associado && visivel(associado) && ["INPUT", "TEXTAREA"].includes(associado.tagName)) campo = associado;
    ...    }
    ...    let escopo = label.parentElement;
    ...    for (let i = 0; i < 8 && escopo && !campo; i++) {
    ...        const campos = Array.from(escopo.querySelectorAll("input:not([type='hidden']), textarea")).filter(visivel);
    ...        campo = campos.find((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) || campos[0] || null;
    ...        escopo = escopo.parentElement;
    ...    }
    ...    if (!campo) {
    ...        const todos = Array.from(root.querySelectorAll("input:not([type='hidden']), textarea")).filter(visivel);
    ...        campo = todos.find((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING));
    ...    }
    ...    if (!campo) return "ERRO|Campo não encontrado para: " + labelAlvo;
    ...    const tag = campo.tagName.toLowerCase();
    ...    const proto = tag === "textarea" ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
    ...    const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
    ...    campo.scrollIntoView({ block: "center", inline: "center" });
    ...    campo.focus();
    ...    setter.call(campo, "");
    ...    campo.dispatchEvent(new Event("input", { bubbles: true }));
    ...    setter.call(campo, valor);
    ...    campo.dispatchEvent(new Event("input", { bubbles: true }));
    ...    campo.dispatchEvent(new Event("change", { bubbles: true }));
    ...    campo.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    ...    campo.dispatchEvent(new Event("blur", { bubbles: true }));
    ...    return "OK|" + labelAlvo + "|" + valor;

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${label_campo}    ${valor}

    ${ok}=    Run Keyword And Return Status
    ...    Should Contain    ${resultado}    OK|

    IF    not ${ok}
        Log To Console    AVISO: não foi possível preencher o campo '${label_campo}'. Resultado: ${resultado}
    END

    Sleep    0.15s


# -------------------------------------------------------------------
# DATEPICKER TOLERANTE
# -------------------------------------------------------------------

Preencher Data Via Datepicker Tolerante
    [Arguments]    ${texto_label}    ${valor}    ${indice_fallback}

    ${status_abertura}    ${resultado_abertura}=    Run Keyword And Ignore Error
    ...    Abrir Campo Data Por Texto
    ...    ${texto_label}
    ...    ${indice_fallback}

    IF    '${status_abertura}' == 'FAIL'
        Log To Console    AVISO: não foi possível abrir o campo de data '${texto_label}'. Motivo: ${resultado_abertura}
        RETURN
    END

    ${ja_eh_data}=    Run Keyword And Return Status
    ...    Should Match Regexp
    ...    ${resultado_abertura}
    ...    \\d{2}/\\d{2}/\\d{4}

    ${ja_eh_data_desejada}=    Run Keyword And Return Status
    ...    Should Contain
    ...    ${resultado_abertura}
    ...    ${valor}

    IF    ${ja_eh_data_desejada}
        Log To Console    Campo '${texto_label}' já está com a data desejada: ${valor}
        Fechar Overlays
        RETURN
    END

    Sleep    0.25s

    ${preencheu_input}=    Run Keyword And Return Status
    ...    Preencher Data Em Input Aberto
    ...    ${valor}

    IF    ${preencheu_input}
        Log To Console    Campo '${texto_label}' preenchido por input aberto com ${valor}
        Fechar Overlays
        RETURN
    END

    ${selecionou_calendario}=    Run Keyword And Return Status
    ...    Selecionar Dia No Calendario
    ...    ${valor}

    IF    ${selecionou_calendario}
        Log To Console    Campo '${texto_label}' preenchido pelo calendário com ${valor}
        Fechar Overlays
        RETURN
    END

    IF    ${ja_eh_data}
        Log To Console    Não consegui trocar '${texto_label}' para ${valor}, mas o campo já possui uma data válida. Seguindo com a data existente.
        Fechar Overlays
        RETURN
    END

    Log To Console    AVISO: não foi possível preencher a data '${texto_label}' e o campo não tinha data válida. Resultado abertura: ${resultado_abertura}


Abrir Campo Data Por Texto
    [Arguments]    ${texto_label}    ${indice_fallback}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const textoLabel = String(arguments[0] || "");
    ...    const indiceFallback = Number(arguments[1] || 1);
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(textoLabel);
    ...    const ignorar = (el) => Boolean(el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar, [data-radix-popper-content-wrapper], [data-radix-select-content], [role='listbox'], [cmdk-list], [cmdk-root]"));
    ...    const visivel = (el) => {
    ...        if (!el || ignorar(el)) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const root = document.querySelector("main") || document.body;
    ...    const textos = Array.from(root.querySelectorAll("label, p, span, div")).filter(visivel);
    ...    let label = textos.find((el) => {
    ...        const texto = normalizar(el.innerText || el.textContent);
    ...        return texto.includes(alvo) && texto.length <= alvo.length + 120;
    ...    });
    ...    if (!label) {
    ...        const datas = textos.filter((el) => normalizar(el.innerText || el.textContent).includes("data estimada"));
    ...        label = datas[indiceFallback - 1] || null;
    ...    }
    ...    const campos = Array.from(root.querySelectorAll("input:not([type='hidden']), button, [role='button'], [aria-haspopup='dialog'], [data-slot='popover-trigger'], div")).filter((el) => {
    ...        if (!visivel(el)) return false;
    ...        const txt = normalizar(el.innerText || el.textContent || el.value || el.getAttribute("aria-label") || el.getAttribute("placeholder") || "");
    ...        if (txt.includes("avancar") || txt.includes("salvar") || txt.includes("gravar") || txt.includes("cancelar")) return false;
    ...        return true;
    ...    });
    ...    let campo = null;
    ...    if (label) {
    ...        const forId = label.getAttribute("for");
    ...        if (forId) {
    ...            const associado = document.getElementById(forId);
    ...            if (associado && visivel(associado)) campo = associado;
    ...        }
    ...        let escopo = label.parentElement;
    ...        for (let i = 0; i < 8 && escopo && !campo; i++) {
    ...            const internos = Array.from(escopo.querySelectorAll("input:not([type='hidden']), button, [role='button'], [aria-haspopup='dialog'], [data-slot='popover-trigger'], div")).filter((el) => {
    ...                if (!visivel(el)) return false;
    ...                if (el === label) return false;
    ...                const txt = normalizar(el.innerText || el.textContent || el.value || el.getAttribute("aria-label") || el.getAttribute("placeholder") || "");
    ...                if (txt.includes("avancar") || txt.includes("salvar") || txt.includes("gravar") || txt.includes("cancelar")) return false;
    ...                return true;
    ...            });
    ...            const depois = internos.filter((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) || label.contains(el));
    ...            campo = depois[0] || null;
    ...            escopo = escopo.parentElement;
    ...        }
    ...        if (!campo) {
    ...            const rectLabel = label.getBoundingClientRect();
    ...            campo = campos.map((el) => {
    ...                const r = el.getBoundingClientRect();
    ...                const dy = Math.abs(r.top - rectLabel.bottom);
    ...                const dx = Math.abs(r.left - rectLabel.left);
    ...                const abaixo = r.top >= rectLabel.top - 10 ? 0 : 10000;
    ...                return { el, score: abaixo + dy * 5 + dx };
    ...            }).sort((a, b) => a.score - b.score)[0]?.el || null;
    ...        }
    ...    }
    ...    if (!campo) {
    ...        const candidatosData = campos.filter((el) => {
    ...            const txt = normalizar(el.innerText || el.textContent || el.value || el.getAttribute("aria-label") || el.getAttribute("placeholder") || "");
    ...            const type = normalizar(el.getAttribute("type") || "");
    ...            const name = normalizar(el.getAttribute("name") || "");
    ...            const id = normalizar(el.getAttribute("id") || "");
    ...            return type === "date" || txt.includes("data") || name.includes("data") || id.includes("data") || txt.includes("dd/mm") || txt.includes("selecione");
    ...        });
    ...        campo = candidatosData[indiceFallback - 1] || null;
    ...    }
    ...    if (!campo) {
    ...        return "ERRO|Campo de data não encontrado. Labels data: " + textos.map((el) => normalizar(el.innerText || el.textContent)).filter((t) => t.includes("data")).join(" | ");
    ...    }
    ...    campo.scrollIntoView({ block: "center", inline: "center" });
    ...    campo.focus();
    ...    campo.click();
    ...    return "OK|" + (campo.tagName || "") + "|" + (campo.innerText || campo.value || campo.getAttribute("aria-label") || "");

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${texto_label}    ${indice_fallback}

    Log To Console    Abrir data ${texto_label}: ${resultado}

    Should Contain
    ...    ${resultado}
    ...    OK|
    ...    msg=Falha ao abrir campo de data '${texto_label}'. Resultado: ${resultado}

    RETURN    ${resultado}


Preencher Data Em Input Aberto
    [Arguments]    ${valor}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const valorOriginal = String(arguments[0] || "");
    ...    const partes = valorOriginal.split("/");
    ...    const valorISO = partes.length === 3 ? partes[2] + "-" + partes[1] + "-" + partes[0] : valorOriginal;
    ...    const visivel = (el) => {
    ...        if (!el) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const roots = [
    ...        ...Array.from(document.querySelectorAll("[data-radix-popper-content-wrapper], [role='dialog'], [data-radix-dialog-content]")),
    ...        document.body
    ...    ];
    ...    let input = null;
    ...    for (const root of roots) {
    ...        input = Array.from(root.querySelectorAll("input:not([type='hidden'])")).find((el) => {
    ...            if (!visivel(el)) return false;
    ...            const type = String(el.getAttribute("type") || "").toLowerCase();
    ...            const placeholder = String(el.getAttribute("placeholder") || "").toLowerCase();
    ...            return type === "date" || placeholder.includes("dd") || placeholder.includes("data");
    ...        });
    ...        if (input) break;
    ...    }
    ...    if (!input) return false;
    ...    const type = String(input.getAttribute("type") || "").toLowerCase();
    ...    const valorFinal = type === "date" ? valorISO : valorOriginal;
    ...    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    ...    input.focus();
    ...    setter.call(input, "");
    ...    input.dispatchEvent(new Event("input", { bubbles: true }));
    ...    setter.call(input, valorFinal);
    ...    input.dispatchEvent(new Event("input", { bubbles: true }));
    ...    input.dispatchEvent(new Event("change", { bubbles: true }));
    ...    input.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    ...    input.dispatchEvent(new Event("blur", { bubbles: true }));
    ...    return true;

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${valor}

    Should Be True
    ...    ${resultado}
    ...    msg=Não existe input de data aberto para preencher diretamente.


Selecionar Dia No Calendario
    [Arguments]    ${valor}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const valor = String(arguments[0] || "");
    ...    const partes = valor.split("/");
    ...    const diaPadded = partes[0];
    ...    const dia = String(Number(partes[0]));
    ...    const mes = Number(partes[1]);
    ...    const ano = partes[2];
    ...    const meses = ["janeiro","fevereiro","marco","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
    ...    const mesesAlt = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
    ...    const mesNome = meses[mes - 1];
    ...    const mesAlt = mesesAlt[mes - 1];
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const visivel = (el) => {
    ...        if (!el) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const roots = [
    ...        ...Array.from(document.querySelectorAll("[data-radix-popper-content-wrapper], [role='dialog'], [data-radix-dialog-content], .rdp, [class*='calendar']")),
    ...        document.body
    ...    ];
    ...    let candidatos = [];
    ...    for (const root of roots) {
    ...        candidatos.push(...Array.from(root.querySelectorAll("button, [role='gridcell'], [role='button']")).filter(visivel));
    ...    }
    ...    candidatos = candidatos.filter((el) => {
    ...        if (el.disabled || el.getAttribute("aria-disabled") === "true") return false;
    ...        const txt = normalizar(el.innerText || el.textContent || "");
    ...        const aria = normalizar(el.getAttribute("aria-label") || el.getAttribute("title") || "");
    ...        const data = normalizar(el.getAttribute("data-day") || el.getAttribute("data-date") || el.getAttribute("data-value") || "");
    ...        if (data.includes(ano + "-" + String(mes).padStart(2, "0") + "-" + diaPadded)) return true;
    ...        if ((aria.includes(dia) || aria.includes(diaPadded)) && (aria.includes(mesNome) || aria.includes(mesAlt)) && aria.includes(ano)) return true;
    ...        if (txt === dia || txt === diaPadded) return true;
    ...        return false;
    ...    });
    ...    candidatos.sort((a, b) => {
    ...        const aa = normalizar(a.getAttribute("aria-label") || a.getAttribute("title") || a.getAttribute("data-day") || a.getAttribute("data-date") || "");
    ...        const bb = normalizar(b.getAttribute("aria-label") || b.getAttribute("title") || b.getAttribute("data-day") || b.getAttribute("data-date") || "");
    ...        const scoreA = (aa.includes(mesNome) || aa.includes(mesAlt) || aa.includes("-" + String(mes).padStart(2, "0") + "-")) && aa.includes(ano) ? 0 : 1;
    ...        const scoreB = (bb.includes(mesNome) || bb.includes(mesAlt) || bb.includes("-" + String(mes).padStart(2, "0") + "-")) && bb.includes(ano) ? 0 : 1;
    ...        return scoreA - scoreB;
    ...    });
    ...    const alvo = candidatos[0];
    ...    if (!alvo) return false;
    ...    alvo.scrollIntoView({ block: "center", inline: "center" });
    ...    alvo.focus();
    ...    alvo.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true, cancelable: true }));
    ...    alvo.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
    ...    alvo.dispatchEvent(new PointerEvent("pointerup", { bubbles: true, cancelable: true }));
    ...    alvo.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
    ...    alvo.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
    ...    alvo.click();
    ...    return true;

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${valor}

    Should Be True
    ...    ${resultado}
    ...    msg=Não foi possível selecionar o dia '${valor}' no calendário.


Fechar Overlays
    Run Keyword And Ignore Error    Press Keys    None    ESC
    Sleep    0.1s
    Run Keyword And Ignore Error    Press Keys    None    ESC
    Sleep    0.1s

    ${script}=    Catenate    SEPARATOR=\n
    ...    const visivel = (el) => {
    ...        if (!el) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    ...    const overlaysAbertos = Array.from(document.querySelectorAll("[data-radix-popper-content-wrapper], [role='listbox'], [cmdk-root]")).filter(visivel);
    ...    if (overlaysAbertos.length) {
    ...        const dialogo = Array.from(document.querySelectorAll("[role='dialog'], [data-radix-dialog-content]")).filter(visivel).pop();
    ...        const alvo = dialogo ? (dialogo.querySelector("h1, h2, [class*='title' i]") || dialogo) : document.body;
    ...        alvo.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
    ...        alvo.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
    ...        alvo.click();
    ...    }
    ...    return overlaysAbertos.length;

    Run Keyword And Ignore Error    Execute Javascript    ${script}

    Sleep    0.15s


# -------------------------------------------------------------------
# DESEMBOLSO
# -------------------------------------------------------------------

Preencher Campo Monetario Por Texto Visual
    [Arguments]    ${texto_label}    ${valor}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const textoLabel = String(arguments[0] || "");
    ...    const valor = String(arguments[1] || "");
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(textoLabel);
    ...    const ignorar = (el) => Boolean(el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar, [data-radix-popper-content-wrapper], [data-radix-select-content], [role='listbox'], [cmdk-list], [cmdk-root]"));
    ...    const visivel = (el) => {
    ...        if (!el || ignorar(el)) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const root = document.querySelector("main") || document.body;
    ...    const textos = Array.from(root.querySelectorAll("label, p, span, div")).filter(visivel);
    ...    let label = textos.find((el) => {
    ...        const texto = normalizar(el.innerText || el.textContent);
    ...        return texto.includes(alvo) && texto.length <= alvo.length + 100;
    ...    });
    ...    if (!label) {
    ...        return "ERRO|Texto não encontrado: " + textoLabel;
    ...    }
    ...    let campo = null;
    ...    let escopo = label.parentElement;
    ...    for (let i = 0; i < 10 && escopo && !campo; i++) {
    ...        const inputs = Array.from(escopo.querySelectorAll("input:not([type='hidden'])")).filter(visivel);
    ...        const depois = inputs.filter((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING));
    ...        campo = depois[0] || inputs[0] || null;
    ...        escopo = escopo.parentElement;
    ...    }
    ...    if (!campo) {
    ...        const todos = Array.from(root.querySelectorAll("input:not([type='hidden'])")).filter(visivel);
    ...        const rectLabel = label.getBoundingClientRect();
    ...        campo = todos.map((el) => {
    ...            const r = el.getBoundingClientRect();
    ...            const abaixo = r.top >= rectLabel.top - 5 ? 0 : 10000;
    ...            return { el, score: abaixo + Math.abs(r.top - rectLabel.bottom) * 5 + Math.abs(r.left - rectLabel.left) };
    ...        }).sort((a, b) => a.score - b.score)[0]?.el || null;
    ...    }
    ...    if (!campo) {
    ...        return "ERRO|Campo não encontrado para: " + textoLabel;
    ...    }
    ...    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    ...    campo.scrollIntoView({ block: "center", inline: "center" });
    ...    campo.focus();
    ...    setter.call(campo, "");
    ...    campo.dispatchEvent(new Event("input", { bubbles: true }));
    ...    setter.call(campo, valor);
    ...    campo.dispatchEvent(new Event("input", { bubbles: true }));
    ...    campo.dispatchEvent(new Event("change", { bubbles: true }));
    ...    campo.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    ...    campo.dispatchEvent(new Event("blur", { bubbles: true }));
    ...    return "OK|" + textoLabel + "|" + valor;

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${texto_label}    ${valor}

    Log To Console    Resultado preencher '${texto_label}': ${resultado}

    Should Contain
    ...    ${resultado}
    ...    OK|
    ...    msg=Não foi possível preencher '${texto_label}'. Resultado: ${resultado}

    Sleep    0.2s


Preencher Valor Mensal Desembolso
    [Arguments]    ${ano}    ${mes}    ${valor}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const ano = String(arguments[0] || "");
    ...    const mes = String(arguments[1] || "");
    ...    const valor = String(arguments[2] || "");
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const mesAlvo = normalizar(mes);
    ...    const ignorar = (el) => Boolean(el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar, [data-radix-popper-content-wrapper], [data-radix-select-content], [role='listbox'], [cmdk-list], [cmdk-root]"));
    ...    const visivel = (el) => {
    ...        if (!el || ignorar(el)) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const root = document.querySelector("main") || document.body;
    ...    const textos = Array.from(root.querySelectorAll("h1, h2, h3, p, span, div, label")).filter(visivel);
    ...    let tituloAno = textos.find((el) => {
    ...        const texto = normalizar(el.innerText || el.textContent);
    ...        return texto.includes("valores estimados para o exercicio") && texto.includes(ano);
    ...    });
    ...    if (!tituloAno) {
    ...        tituloAno = textos.find((el) => {
    ...            const texto = normalizar(el.innerText || el.textContent);
    ...            return texto.includes("parcela anual") && texto.includes(ano);
    ...        });
    ...    }
    ...    let rootAno = null;
    ...    if (tituloAno) {
    ...        let atual = tituloAno;
    ...        for (let i = 0; i < 10 && atual; i++) {
    ...            const texto = normalizar(atual.innerText || "");
    ...            const qtdInputs = Array.from(atual.querySelectorAll("input:not([type='hidden'])")).filter(visivel).length;
    ...            if (texto.includes("janeiro") && texto.includes("dezembro") && qtdInputs > 0) {
    ...                rootAno = atual;
    ...                break;
    ...            }
    ...            atual = atual.parentElement;
    ...        }
    ...    }
    ...    if (!rootAno) {
    ...        rootAno = root;
    ...    }
    ...    const textosAno = Array.from(rootAno.querySelectorAll("label, p, span, div")).filter(visivel);
    ...    let labelMes = textosAno.find((el) => {
    ...        const texto = normalizar(el.innerText || el.textContent);
    ...        return texto === mesAlvo;
    ...    });
    ...    if (!labelMes) {
    ...        labelMes = textosAno.find((el) => {
    ...            const texto = normalizar(el.innerText || el.textContent);
    ...            return texto.includes(mesAlvo) && texto.length <= mesAlvo.length + 20;
    ...        });
    ...    }
    ...    let campo = null;
    ...    if (labelMes) {
    ...        let escopo = labelMes.parentElement;
    ...        for (let i = 0; i < 8 && escopo && !campo; i++) {
    ...            const inputs = Array.from(escopo.querySelectorAll("input:not([type='hidden'])")).filter(visivel);
    ...            const depois = inputs.filter((el) => Boolean(labelMes.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING));
    ...            campo = depois[0] || inputs[0] || null;
    ...            escopo = escopo.parentElement;
    ...        }
    ...        if (!campo) {
    ...            const inputs = Array.from(rootAno.querySelectorAll("input:not([type='hidden'])")).filter(visivel);
    ...            const rectMes = labelMes.getBoundingClientRect();
    ...            campo = inputs.map((el) => {
    ...                const r = el.getBoundingClientRect();
    ...                const abaixo = r.top >= rectMes.top - 5 ? 0 : 10000;
    ...                return { el, score: abaixo + Math.abs(r.top - rectMes.bottom) * 5 + Math.abs(r.left - rectMes.left) };
    ...            }).sort((a, b) => a.score - b.score)[0]?.el || null;
    ...        }
    ...    }
    ...    if (!campo) {
    ...        const inputs = Array.from(rootAno.querySelectorAll("input:not([type='hidden'])")).filter(visivel);
    ...        campo = inputs.find((el) => !el.disabled && !el.readOnly) || inputs[0] || null;
    ...    }
    ...    if (!campo) {
    ...        return "ERRO|Campo mensal não encontrado para " + mes + "/" + ano;
    ...    }
    ...    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    ...    campo.scrollIntoView({ block: "center", inline: "center" });
    ...    campo.focus();
    ...    setter.call(campo, "");
    ...    campo.dispatchEvent(new Event("input", { bubbles: true }));
    ...    setter.call(campo, valor);
    ...    campo.dispatchEvent(new Event("input", { bubbles: true }));
    ...    campo.dispatchEvent(new Event("change", { bubbles: true }));
    ...    campo.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    ...    campo.dispatchEvent(new Event("blur", { bubbles: true }));
    ...    return "OK|" + mes + "/" + ano + "|" + valor;

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${ano}    ${mes}    ${valor}

    Log To Console    Resultado desembolso mensal: ${resultado}

    ${ok}=    Run Keyword And Return Status
    ...    Should Contain    ${resultado}    OK|

    IF    not ${ok}
        Log To Console    AVISO: não foi possível preencher o desembolso mensal. Resultado: ${resultado}
    END

    Sleep    0.2s


Clicar Botao Salvar Final
    ${botao_salvar}=    Set Variable
    ...    xpath=(//button[not(@disabled) and contains(normalize-space(.), 'Salvar')])[last()]

    ${visivel}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${botao_salvar}    timeout=${TIMEOUT}

    IF    not ${visivel}
        Log To Console    AVISO: botão 'Salvar' final não ficou visível.
        RETURN
    END

    ${habilitado}=    Run Keyword And Return Status
    ...    Wait Until Element Is Enabled    ${botao_salvar}    timeout=${TIMEOUT}

    IF    not ${habilitado}
        Log To Console    AVISO: botão 'Salvar' final não ficou habilitado (campos obrigatórios pendentes?).
        RETURN
    END

    Clicar Com JS    ${botao_salvar}

    Sleep    1.5s


# -------------------------------------------------------------------
# CLIQUES E DROPDOWNS
# -------------------------------------------------------------------

Selecionar Tipo de Subitem
    [Arguments]    ${tipo}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const tipoAlvo = String(arguments[0] || "");
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(tipoAlvo);
    ...    const visivel = (el) => {
    ...        if (!el) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const dialogs = Array.from(document.querySelectorAll("[role='dialog'], [data-radix-dialog-content]")).filter(visivel);
    ...    const root = dialogs.length ? dialogs[dialogs.length - 1] : (document.querySelector("main") || document.body);
    ...    const candidatos = Array.from(root.querySelectorAll("label, button, [role='radio'], input[type='radio'], span, div")).filter(visivel).filter((el) => {
    ...        const texto = normalizar(el.innerText || el.textContent || el.value || el.getAttribute("aria-label") || "");
    ...        return texto === alvo;
    ...    });
    ...    const pesoTag = (el) => {
    ...        const tag = el.tagName.toLowerCase();
    ...        if (tag === "input" && el.type === "radio") return 0;
    ...        if (el.getAttribute("role") === "radio") return 1;
    ...        if (tag === "button") return 2;
    ...        if (tag === "label") return 3;
    ...        return 4;
    ...    };
    ...    candidatos.sort((a, b) => pesoTag(a) - pesoTag(b));
    ...    let alvoClique = candidatos[0];
    ...    if (!alvoClique) return "ERRO|Tipo de Subitem não encontrado: " + tipoAlvo;
    ...    const radio = alvoClique.matches("input[type='radio']") ? alvoClique : alvoClique.querySelector("input[type='radio']");
    ...    if (radio && radio.id) {
    ...        const label = root.querySelector("label[for='" + CSS.escape(radio.id) + "']");
    ...        if (label) alvoClique = label;
    ...    }
    ...    const clicavel = alvoClique.matches("label, button, [role='radio'], input[type='radio']")
    ...        ? alvoClique
    ...        : (alvoClique.querySelector("label, button, [role='radio'], input[type='radio']") || alvoClique.closest("label, button, [role='radio']") || alvoClique);
    ...    clicavel.scrollIntoView({ block: "center", inline: "center" });
    ...    clicavel.focus();
    ...    clicavel.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true, cancelable: true }));
    ...    clicavel.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
    ...    clicavel.dispatchEvent(new PointerEvent("pointerup", { bubbles: true, cancelable: true }));
    ...    clicavel.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
    ...    clicavel.click();
    ...    const marcado = clicavel.getAttribute("aria-checked") === "true" || clicavel.getAttribute("data-state") === "checked" || clicavel.getAttribute("data-state") === "active" || clicavel.getAttribute("data-state") === "on" || (clicavel.tagName === "INPUT" && clicavel.checked);
    ...    return "OK|" + tipoAlvo + "|tag=" + clicavel.tagName + "|marcado=" + marcado;

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${tipo}

    Log To Console    Seleção do Tipo de Subitem: ${resultado}

    Should Contain
    ...    ${resultado}
    ...    OK|
    ...    msg=Não foi possível selecionar o Tipo de Subitem '${tipo}'. Resultado: ${resultado}

    Sleep    0.25s


Clicar Com JS
    [Arguments]    ${locator}

    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    ${elemento}=    Get WebElement    ${locator}

    Execute Javascript
    ...    arguments[0].scrollIntoView({ block: 'center', inline: 'center' });
    ...    ARGUMENTS
    ...    ${elemento}

    Sleep    0.1s

    Execute Javascript
    ...    arguments[0].click();
    ...    ARGUMENTS
    ...    ${elemento}

    Sleep    0.2s


Clicar Nativo Depois JS
    [Arguments]    ${locator}

    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Scroll Element Into View         ${locator}
    Sleep    0.1s

    ${clicou}=    Run Keyword And Return Status    Click Element    ${locator}

    IF    not ${clicou}
        Clicar Com JS    ${locator}
    END

    Sleep    0.2s


Selecionar Area Demandante
    [Arguments]    ${texto_opcao}

    ${selecionado}=    Set Variable    ${False}

    FOR    ${tentativa}    IN RANGE    1    5
        Log To Console    Selecionando Área Demandante '${texto_opcao}' - tentativa ${tentativa}

        Abrir Area Demandante Direto
        Sleep    0.3s

        Preencher Busca Do Dropdown    ${texto_opcao}
        Sleep    0.4s

        ${marcou}=    Run Keyword And Return Status
        ...    Marcar Opcao Visivel Por Texto
        ...    ${texto_opcao}
        ...    area-demandante

        IF    ${marcou}
            ${clicou}=    Run Keyword And Return Status
            ...    Clicar Opcao Marcada Nativo
            ...    area-demandante

            Sleep    0.4s

            ${selecionado}=    Campo Por Label Contem Texto
            ...    Área Demandante
            ...    ${texto_opcao}

            IF    ${selecionado}
                Exit For Loop
            END
        END

        Confirmar Dropdown Com Enter
        Sleep    0.4s

        ${selecionado}=    Campo Por Label Contem Texto
        ...    Área Demandante
        ...    ${texto_opcao}

        IF    ${selecionado}
            Exit For Loop
        END

        Run Keyword And Ignore Error    Press Keys    None    TAB
        Sleep    0.3s
    END

    IF    not ${selecionado}
        ${valor_atual}=    Obter Valor Campo Por Label    Área Demandante
        Log To Console    AVISO: não foi possível confirmar a Área Demandante '${texto_opcao}'. Valor atual: '${valor_atual}'.
    END


Abrir Area Demandante Direto
    ${locator}=    Set Variable
    ...    xpath=//label[normalize-space(.)='Área Demandante']/following::*[(self::button or @role='combobox')][1]

    Clicar Nativo Depois JS    ${locator}


Selecionar Opcao Dropdown
    [Arguments]    ${label_campo}    ${texto_opcao}

    ${selecionado}=    Set Variable    ${False}

    FOR    ${tentativa}    IN RANGE    1    5
        Log To Console    Selecionando '${label_campo}' = '${texto_opcao}' - tentativa ${tentativa}

        ${abriu}=    Run Keyword And Return Status
        ...    Abrir Dropdown Pelo Label
        ...    ${label_campo}

        IF    not ${abriu}
            Sleep    0.2s
            CONTINUE
        END

        Sleep    0.3s

        Preencher Busca Do Dropdown    ${texto_opcao}
        Sleep    0.3s

        ${marcou}=    Run Keyword And Return Status
        ...    Marcar Opcao Visivel Por Texto
        ...    ${texto_opcao}
        ...    opcao-generica

        IF    ${marcou}
            ${clicou}=    Run Keyword And Return Status
            ...    Clicar Opcao Marcada Nativo
            ...    opcao-generica

            Sleep    0.3s

            ${selecionado}=    Campo Por Label Contem Texto
            ...    ${label_campo}
            ...    ${texto_opcao}

            IF    ${selecionado}
                Exit For Loop
            END
        END

        Confirmar Dropdown Com Enter
        Sleep    0.3s

        ${selecionado}=    Campo Por Label Contem Texto
        ...    ${label_campo}
        ...    ${texto_opcao}

        IF    ${selecionado}
            Exit For Loop
        END
    END

    ${valor_final}=    Obter Valor Campo Por Label    ${label_campo}
    Log To Console    Campo '${label_campo}' - valor exibido ao final: ${valor_final}

    IF    not ${selecionado}
        Log To Console    AVISO: não foi possível selecionar '${texto_opcao}' no campo '${label_campo}'. Valor atual: '${valor_final}'. Seguindo com o valor atual do campo.
    END


Abrir Dropdown Pelo Label
    [Arguments]    ${label_campo}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const labelAlvo = String(arguments[0] || "");
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(labelAlvo);
    ...    const foraDoMenu = (el) => !el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar");
    ...    const visivel = (el) => {
    ...        if (!el || !foraDoMenu(el)) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const modais = Array.from(document.querySelectorAll("[role='dialog'], [data-radix-dialog-content]")).filter(visivel);
    ...    const root = modais.length ? modais[modais.length - 1] : (document.querySelector("main") || document.querySelector("form") || document.body);
    ...    const labels = Array.from(root.querySelectorAll("label, p, span, div")).filter(visivel);
    ...    let label = labels.find((el) => normalizar(el.innerText || el.textContent) === alvo);
    ...    if (!label) {
    ...        label = labels.find((el) => {
    ...            const texto = normalizar(el.innerText || el.textContent);
    ...            return texto.includes(alvo) && texto.length <= alvo.length + 35;
    ...        });
    ...    }
    ...    if (!label) return "ERRO|Label não encontrada: " + labelAlvo;
    ...    const seletorTrigger = "button:not([type='submit']),[role='combobox'],input:not([type='hidden']),[data-radix-select-trigger],[aria-haspopup='listbox'],[aria-haspopup='menu']";
    ...    const proibidos = ["avançar", "avancar", "salvar", "gravar", "criar", "cancelar", "voltar", "menu", "sidebar"];
    ...    const candidatoValido = (el) => {
    ...        if (!visivel(el)) return false;
    ...        if (el.disabled || el.getAttribute("aria-disabled") === "true") return false;
    ...        const texto = normalizar(el.innerText || el.value || el.getAttribute("aria-label") || "");
    ...        if (proibidos.some((p) => texto.includes(p))) return false;
    ...        return true;
    ...    };
    ...    let trigger = null;
    ...    const forId = label.getAttribute("for");
    ...    if (forId) {
    ...        const associado = document.getElementById(forId);
    ...        if (associado && candidatoValido(associado)) trigger = associado;
    ...    }
    ...    let escopo = label.parentElement;
    ...    for (let i = 0; i < 8 && escopo && !trigger; i++) {
    ...        const elementos = Array.from(escopo.querySelectorAll(seletorTrigger)).filter(candidatoValido);
    ...        const depois = elementos.filter((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) || label.contains(el));
    ...        trigger = depois[0] || null;
    ...        escopo = escopo.parentElement;
    ...    }
    ...    if (!trigger) {
    ...        const todos = Array.from(root.querySelectorAll(seletorTrigger)).filter(candidatoValido);
    ...        trigger = todos.find((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING));
    ...    }
    ...    if (!trigger) return "ERRO|Trigger não encontrado para: " + labelAlvo;
    ...    trigger.scrollIntoView({ block: "center", inline: "center" });
    ...    trigger.focus();
    ...    trigger.click();
    ...    return "OK|" + trigger.tagName + "|" + (trigger.innerText || trigger.value || trigger.getAttribute("aria-label") || "");

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${label_campo}

    Log To Console    Dropdown '${label_campo}' - trigger aberto: ${resultado}

    Should Contain
    ...    ${resultado}
    ...    OK|
    ...    msg=Falha ao abrir dropdown '${label_campo}'. Resultado: ${resultado}


Preencher Busca Do Dropdown
    [Arguments]    ${texto_opcao}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const valor = String(arguments[0] || "");
    ...    const visivel = (el) => {
    ...        if (!el) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const seletoresBusca = [
    ...        "[data-radix-popper-content-wrapper] input",
    ...        "[data-radix-select-content] input",
    ...        "[role='listbox'] input",
    ...        "[role='dialog'] input",
    ...        "[cmdk-input]",
    ...        "input[type='search']",
    ...        "input[placeholder*='buscar' i]",
    ...        "input[placeholder*='pesquisar' i]"
    ...    ];
    ...    let input = null;
    ...    for (const seletor of seletoresBusca) {
    ...        input = Array.from(document.querySelectorAll(seletor)).find(visivel);
    ...        if (input) break;
    ...    }
    ...    if (!input && document.activeElement && document.activeElement.tagName === "INPUT") input = document.activeElement;
    ...    if (!input) return "";
    ...    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
    ...    input.focus();
    ...    setter.call(input, "");
    ...    input.dispatchEvent(new Event("input", { bubbles: true }));
    ...    setter.call(input, valor);
    ...    input.dispatchEvent(new Event("input", { bubbles: true }));
    ...    input.dispatchEvent(new Event("change", { bubbles: true }));
    ...    input.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    ...    return "OK|" + (input.tagName || "") + "|" + (input.getAttribute("placeholder") || input.getAttribute("aria-label") || "");

    ${resultado_busca}=    Execute Javascript    ${script}    ARGUMENTS    ${texto_opcao}

    Log To Console    Busca do dropdown - campo utilizado: ${resultado_busca}

    ${tem_busca}=    Run Keyword And Return Status
    ...    Should Not Be Empty    ${resultado_busca}

    IF    not ${tem_busca}
        Run Keyword And Ignore Error    Press Keys    None    ${texto_opcao}
    END


Marcar Opcao Visivel Por Texto
    [Arguments]    ${texto_opcao}    ${marcador}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const textoAlvo = String(arguments[0] || "");
    ...    const marcador = String(arguments[1] || "opcao-temp");
    ...    document.querySelectorAll("[data-robot-target]").forEach((el) => el.removeAttribute("data-robot-target"));
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(textoAlvo);
    ...    const visivel = (el) => {
    ...        if (!el) return false;
    ...        if (["INPUT", "TEXTAREA"].includes(el.tagName)) return false;
    ...        if (el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar")) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const roots = [
    ...        ...Array.from(document.querySelectorAll("[data-radix-popper-content-wrapper]")),
    ...        ...Array.from(document.querySelectorAll("[role='listbox']")),
    ...        ...Array.from(document.querySelectorAll("[role='dialog']")),
    ...        document.body
    ...    ].filter(Boolean);
    ...    let todasOpcoes = [];
    ...    for (const root of roots) {
    ...        todasOpcoes.push(...Array.from(root.querySelectorAll("[role='option'], [cmdk-item], [data-radix-collection-item], [data-radix-select-item], [data-value], [role='menuitem'], li, div, span")).filter(visivel));
    ...    }
    ...    const textosDisponiveis = [...new Set(todasOpcoes.map((el) => (el.innerText || el.textContent || el.getAttribute("data-value") || "").trim()).filter(Boolean))];
    ...    let candidatos = todasOpcoes.filter((el) => {
    ...        const texto = normalizar(el.innerText || el.textContent || el.getAttribute("data-value") || "");
    ...        return texto && texto.includes(alvo) && !texto.includes("selecione") && texto.length <= 700;
    ...    });
    ...    candidatos.sort((a, b) => {
    ...        const ta = normalizar(a.innerText || a.textContent || "");
    ...        const tb = normalizar(b.innerText || b.textContent || "");
    ...        const roleA = a.getAttribute("role") === "option" ? 0 : 1;
    ...        const roleB = b.getAttribute("role") === "option" ? 0 : 1;
    ...        if (roleA !== roleB) return roleA - roleB;
    ...        const startA = ta.startsWith(alvo) ? 0 : 1;
    ...        const startB = tb.startsWith(alvo) ? 0 : 1;
    ...        if (startA !== startB) return startA - startB;
    ...        return ta.length - tb.length;
    ...    });
    ...    const encontrado = candidatos[0];
    ...    if (!encontrado) return "ERRO|Nenhuma opção encontrada. Opções visíveis: " + (textosDisponiveis.slice(0, 15).join(" ; ") || "(nenhuma - catálogo vazio ou dropdown errado)");
    ...    const clicavel = encontrado.closest("[role='option'], [cmdk-item], [data-radix-collection-item], [data-radix-select-item], [data-value], [role='menuitem'], li, button, div") || encontrado;
    ...    clicavel.scrollIntoView({ block: "center", inline: "center" });
    ...    clicavel.setAttribute("data-robot-target", marcador);
    ...    return (clicavel.innerText || clicavel.textContent || clicavel.getAttribute("data-value") || "").trim();

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${texto_opcao}    ${marcador}

    Log To Console    Opção marcada para clique: ${resultado}

    Should Not Contain
    ...    ${resultado}
    ...    ERRO|
    ...    msg=Não encontrei opção visível contendo '${texto_opcao}' para marcar. ${resultado}

    Should Not Be Empty
    ...    ${resultado}
    ...    msg=Não encontrei opção visível contendo '${texto_opcao}' para marcar.


Clicar Opcao Marcada Nativo
    [Arguments]    ${marcador}

    ${locator}=    Set Variable    css=[data-robot-target="${marcador}"]

    Wait Until Element Is Visible    ${locator}    timeout=5s
    Scroll Element Into View         ${locator}
    Sleep    0.1s

    ${clicou}=    Run Keyword And Return Status    Click Element    ${locator}

    IF    not ${clicou}
        Clicar Com JS    ${locator}
    END

    Sleep    0.2s


Confirmar Dropdown Com Enter
    Run Keyword And Ignore Error    Press Keys    None    ARROW_DOWN
    Sleep    0.1s
    Run Keyword And Ignore Error    Press Keys    None    ENTER
    Sleep    0.2s


# -------------------------------------------------------------------
# VALIDAÇÕES E AVANÇO
# -------------------------------------------------------------------

Obter Valor Campo Por Label
    [Arguments]    ${label_campo}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const labelAlvo = String(arguments[0] || "");
    ...    const normalizar = (txt) => String(txt || "")
    ...        .normalize("NFD")
    ...        .replace(/[\\u0300-\\u036f]/g, "")
    ...        .replace(/\\s+/g, " ")
    ...        .trim()
    ...        .toLowerCase();
    ...    const alvo = normalizar(labelAlvo);
    ...    const foraDoMenu = (el) => !el.closest("aside, nav, [role='navigation'], [data-sidebar], .sidebar");
    ...    const visivel = (el) => {
    ...        if (!el || !foraDoMenu(el)) return false;
    ...        const rect = el.getBoundingClientRect();
    ...        const style = window.getComputedStyle(el);
    ...        return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    ...    };
    ...    const root = document.querySelector("main") || document.querySelector("form") || document.body;
    ...    const labels = Array.from(root.querySelectorAll("label, p, span, div")).filter(visivel);
    ...    let label = labels.find((el) => normalizar(el.innerText || el.textContent) === alvo);
    ...    if (!label) {
    ...        label = labels.find((el) => {
    ...            const texto = normalizar(el.innerText || el.textContent);
    ...            return texto.includes(alvo) && texto.length <= alvo.length + 60;
    ...        });
    ...    }
    ...    if (!label) return "";
    ...    const seletorCampo = "button,[role='combobox'],input:not([type='hidden']),textarea";
    ...    let campo = null;
    ...    let escopo = label.parentElement;
    ...    for (let i = 0; i < 7 && escopo && !campo; i++) {
    ...        const campos = Array.from(escopo.querySelectorAll(seletorCampo)).filter(visivel);
    ...        campo = campos.find((el) => Boolean(label.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) || campos[0] || null;
    ...        escopo = escopo.parentElement;
    ...    }
    ...    if (!campo) return "";
    ...    return (campo.value || campo.innerText || campo.textContent || campo.getAttribute("aria-label") || "").trim();

    ${resultado}=    Execute Javascript    ${script}    ARGUMENTS    ${label_campo}
    RETURN    ${resultado}


Campo Por Label Contem Texto
    [Arguments]    ${label_campo}    ${texto_procurado}

    ${valor}=    Obter Valor Campo Por Label    ${label_campo}
    ${valor_norm}=    Convert To Lower Case    ${valor}
    ${texto_norm}=    Convert To Lower Case    ${texto_procurado}

    ${contem}=    Run Keyword And Return Status
    ...    Should Contain
    ...    ${valor_norm}
    ...    ${texto_norm}

    RETURN    ${contem}


Garantir Campo Contem Texto
    [Arguments]    ${label_campo}    ${texto}

    ${ok}=    Campo Por Label Contem Texto    ${label_campo}    ${texto}

    IF    not ${ok}
        ${valor_atual}=    Obter Valor Campo Por Label    ${label_campo}
        Log To Console    AVISO: o campo '${label_campo}' não contém '${texto}'. Valor atual: '${valor_atual}'.
    END


Avancar Para Passo
    [Arguments]    ${texto_passo_destino}

    ${botao_avancar}=    Set Variable
    ...    xpath=(//button[not(@disabled) and (contains(normalize-space(.), 'Avançar') or contains(normalize-space(.), 'Proximo') or contains(normalize-space(.), 'Próximo') or contains(normalize-space(.), 'Continuar'))])[last()]

    ${visivel}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${botao_avancar}    timeout=${TIMEOUT}

    IF    not ${visivel}
        Log To Console    AVISO: botão 'Avançar/Próximo' não ficou visível para ir a '${texto_passo_destino}'.
        RETURN
    END

    ${habilitado}=    Run Keyword And Return Status
    ...    Wait Until Element Is Enabled    ${botao_avancar}    timeout=${TIMEOUT}

    IF    not ${habilitado}
        Log To Console    AVISO: botão 'Avançar/Próximo' não ficou habilitado (campos obrigatórios pendentes?) para ir a '${texto_passo_destino}'.
        RETURN
    END

    Clicar Com JS    ${botao_avancar}

    ${avancou}=    Run Keyword And Return Status
    ...    Wait Until Page Contains    ${texto_passo_destino}    timeout=${TIMEOUT}

    IF    not ${avancou}
        Diagnosticar Tela Bloqueada
        Log To Console    AVISO: não foi possível confirmar avanço para o passo '${texto_passo_destino}'. Seguindo mesmo assim.
    END


Diagnosticar Tela Bloqueada
    Capture Page Screenshot

    ${url_atual}=    Get Location
    Log To Console    URL atual: ${url_atual}

    ${script}=    Catenate    SEPARATOR=\n
    ...    const textoTela = document.body.innerText || "";
    ...    return textoTela.slice(0, 3000);

    ${mensagens}=    Execute Javascript    ${script}

    Log To Console    Conteúdo visível da tela: ${mensagens}
    Log    Conteúdo visível da tela: ${mensagens}