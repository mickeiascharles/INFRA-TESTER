# Arquitetura — SISCORP PCA Automação de Cadastro

> Documento de referência técnica do projeto. Escrito para ser autodidata: alguém
> sem contexto prévio deve conseguir, só com este arquivo, entender o sistema
> inteiro, rodar cada parte localmente, depurar problemas comuns e estender o
> software com segurança.
>
> Este é um projeto **vivo**: novos campos, passos e integrações serão
> adicionados com o tempo. Sempre que uma mudança arquitetural relevante for
> feita (novo componente, mudança de fluxo, nova dependência de ambiente),
> atualize este documento na mesma tarefa — não depois.

---

## 1. O que este software faz

O SISCORP (sistema de PCA — Plano de Contratações Anual — da INFRA S.A.) **não
expõe nenhuma API própria**. Toda interação com ele é feita preenchendo
formulários web em um navegador. Para automatizar o cadastro de uma nova
demanda no PCA, a única via possível é automação de navegador (RPA):
simular um usuário humano clicando e digitando na tela.

O motor dessa automação é um script **Robot Framework + Selenium**
(`robot/cadastrar_pca.robot`). Ele já existia antes deste projeto e sabe fazer
login no SISCORP e preencher o wizard de 5 passos de cadastro de demanda.

Em cima desse motor, existem **duas interfaces diferentes** para uma pessoa
alimentar os dados sem precisar editar o `.robot` manualmente:

1. **Web** (`frontend/` + `backend/`) — um formulário React servido por um
   backend FastAPI, pensado para múltiplos usuários acessando via navegador,
   com um servidor central rodando o robô.
2. **Desktop** (`desktop/`) — um aplicativo PySide6 standalone, com o mesmo
   wizard e a mesma lógica, mas **sem servidor**: tudo roda no processo local
   do usuário (login, wizard, disparo do robô, histórico). Pensado para rodar
   como um `.exe` numa máquina Windows, sem precisar montar infraestrutura de
   backend.

As duas interfaces são **independentes** — nenhuma depende da outra — mas
**compartilham o mesmo arquivo de automação** (`robot/cadastrar_pca.robot`) e o
mesmo conjunto de variáveis. Se o SISCORP mudar de layout e o `.robot`
precisar de ajuste, o ajuste vale para as duas interfaces ao mesmo tempo.

```
                          ┌─────────────────────────┐
                          │   robot/cadastrar_pca.robot│
                          │  (Robot Framework+Selenium)│
                          │  faz login e preenche o    │
                          │  SISCORP no navegador       │
                          └───────────▲─────────────┘
                                      │ robot --variable CHAVE:VALOR ...
                    ┌─────────────────┴──────────────────┐
                    │                                     │
         ┌──────────┴─────────┐                ┌──────────┴─────────┐
         │   backend/ (FastAPI)│                │  desktop/ (PySide6) │
         │  API HTTP + SQLite  │                │  App standalone,    │
         │  dispara o robô     │                │  roda o robô no     │
         │  como subprocesso   │                │  mesmo processo     │
         └──────────▲─────────┘                └─────────────────────┘
                    │ HTTP (JSON)
         ┌──────────┴─────────┐
         │  frontend/ (React)  │
         │  wizard de 5 passos │
         └─────────────────────┘
```

---

## 2. Estrutura de pastas

```
teste_siscorp/
├── robot/
│   └── cadastrar_pca.robot        # único arquivo de automação — é este que
│                                   # backend/ e desktop/ realmente executam
├── backend/
│   ├── app/
│   │   ├── main.py                 # cria o FastAPI app, CORS, healthcheck
│   │   ├── config.py               # caminhos (ROBOT_FILE, RUNS_DIR, DB_PATH)
│   │   ├── database.py             # engine SQLAlchemy + sessão
│   │   ├── models.py                # tabela `executions` (SQLAlchemy ORM)
│   │   ├── schemas.py               # modelos Pydantic (validação de entrada/saída)
│   │   ├── robot_runner.py          # dispara `robot` como subprocess, grava log
│   │   └── routers/executions.py    # endpoints HTTP
│   ├── requirements.txt
│   ├── executions.db                # SQLite (fora do git, ver .gitignore)
│   └── runs/<id>/                   # console.log, output.xml, log.html, report.html por execução
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # shell + rotas (react-router)
│   │   ├── api.ts                   # client HTTP para o backend
│   │   ├── types.ts                 # tipos TS espelhando os schemas do backend
│   │   ├── pages/                   # NovaDemanda, Execucoes, ExecucaoDetalhe
│   │   └── components/steps/        # Step1..Step5 do wizard
│   └── package.json
└── desktop/
    ├── main.py                      # entry point (QApplication)
    ├── app/
    │   ├── config.py                 # caminhos, com suporte a modo "congelado" (PyInstaller)
    │   ├── models.py                  # dataclasses (equivalentes aos schemas do backend)
    │   ├── db.py                      # SQLite local (execucoes.db), sem SQLAlchemy
    │   ├── robot_runner.py            # roda `robot.run(...)` **in-process**, numa QThread
    │   ├── login_widget.py            # tela de login (usuário/senha/headless)
    │   ├── execucao_atual_widget.py   # tela "executando" + tela de laudo pós-execução
    │   ├── main_window.py             # janela principal, navegação, sessão
    │   ├── styles.py                  # QSS (tema escuro)
    │   └── wizard/
    │       ├── nova_demanda_widget.py  # orquestra os 6 passos do wizard
    │       └── steps.py                # Step1..Step6 (Qt widgets)
    ├── requirements.txt
    ├── build.sh                      # empacota com PyInstaller (ver seção 6)
    ├── execucoes.db                  # SQLite local (fora do git)
    ├── runs/<id>/                    # mesma ideia do backend, mas local
    └── dist/SiscorpPCA/              # gerado pelo build.sh — o app empacotado
```

---

## 3. `robot/cadastrar_pca.robot` — o motor de automação

Este é o único componente que realmente enxerga e mexe no SISCORP. Backend e
desktop são só "controle remoto": eles montam uma lista de variáveis e mandam
o Robot Framework rodar esse arquivo.

### 3.1 Como ele é invocado

```bash
robot --variable CHAVE1:VALOR1 --variable CHAVE2:VALOR2 ... \
      --outputdir <pasta_de_saida> \
      robot/cadastrar_pca.robot
```

A senha **nunca** é passada por `--variable` (isso apareceria em logs de
processo). Ela vai por variável de ambiente `SISCORP_SENHA`, lida pela keyword
`Obter Senha SISCORP` (linha ~348).

### 3.2 Fluxo de alto nível (`*** Test Cases ***`)

```
Cadastrar Nova Demanda no PCA (SISCORP)
  1. Realizar Login no Sistema
  2. Iniciar Cadastro de Demanda
  3. Executar Etapa → Preencher Passo 1 - Dados Basicos
  4. Executar Etapa → Preencher Passo 2 - Itens de Contratacao
  5. Executar Etapa → Preencher Passo 3 - Dados da Contratacao
  6. Executar Etapa → Preencher Passo 4 - Previsao de Duracao
  7. Executar Etapa → Preencher Passo 5 - Previsao de Desembolso
  8. Executar Etapa → Validar Cadastro com Sucesso
  [Teardown] Close Browser
```

`Executar Etapa` (linha ~73) roda cada passo com `Run Keyword And Ignore
Error`: se um passo falhar, ele **loga o aviso e segue em frente** em vez de
abortar o teste inteiro. Isso é proposital — um campo que o SISCORP mudou de
lugar não deve impedir o preenchimento dos outros passos, e o `Validar
Cadastro com Sucesso` final é quem decide se o teste como um todo passou ou
falhou.

### 3.3 Keywords auxiliares mais importantes

| Keyword | Para que serve |
|---|---|
| `Preencher Campo React` | Digita valor em `<input>`/`<textarea>` controlado por React, disparando os eventos `input`/`change` que o React espera (um `Input Text` normal do Selenium não atualiza o state do React) |
| `Selecionar Opcao Dropdown` / `Abrir Dropdown Pelo Label` / `Marcar Opcao Visivel Por Texto` | Lidam com combobox customizados (não são um `<select>` HTML nativo) |
| `Preencher Data Via Datepicker Tolerante` / `Selecionar Dia No Calendario` | Preenchimento de datas via datepicker próprio do SISCORP |
| `Preencher Campo Monetario Por Texto Visual` | Campos de valor em R$ com máscara |
| `Clicar Com JS` / `Clicar Nativo Depois JS` | Fallback: clique nativo do Selenium às vezes não registra em elementos cobertos por overlay; usa `Execute Javascript` para forçar o clique |
| `Fechar Overlays` | Fecha modais/toasts que ficam por cima de campos |
| `Diagnosticar Tela Bloqueada` | Roda quando `Validar Cadastro com Sucesso` não confirma sucesso — tira screenshot e loga pistas para depuração manual |

### 3.4 Variáveis (o "contrato" com backend/desktop)

Toda variável abaixo tem um valor **default de teste** dentro do `.robot`
(seção `*** Variables ***`), mas backend e desktop sempre sobrescrevem todas
elas via `--variable`. Se você adicionar um campo novo no wizard, ele **tem
que virar uma dessas variáveis** — veja a seção 7 (como estender).

| Variável | Preenchida em (passo do wizard) |
|---|---|
| `NAVEGADOR` | `Chrome` ou `headlesschrome` (decidido pelo checkbox "headless") |
| `USUARIO` | Login |
| `STATUS_CONTRATACAO`, `EVENTO`, `ANO_PCA`, `AREA_DEMANDANTE`, `DESCRICAO_OBJETO`, `JUSTIFICATIVA` | Passo 1 — Dados Básicos |
| `ACAO`, `PLANO_ORCAMENTARIO`, `TIPO_NATUREZA`, `NATUREZA_DESCRICAO`, `STATUS_SUBITEM`, `TIPO_SUBITEM`, `CODIGO_SUBITEM`, `DESCRICAO_SUBITEM`, `UNIDADE_MEDIDA`, `PRECO_UNITARIO`, `QUANTIDADE` | Passo 2 — Itens de Contratação |
| `TIPO_LICITACAO`, `DATA_ASSINATURA`, `DATA_ENTREGA_DOC`, `OBJETIVO_ESTRATEGICO`, `PRIORIDADE`, `SIGILOSO` | Passo 3 — Dados da Contratação |
| `VIGENCIA_MESES` | Passo 4 — Previsão de Duração |
| `TIPO_DESEMBOLSO`, `PARCELA_ANUAL`, `VALOR_PARCELA_UNICA` (opcional), `ANO_DESEMBOLSO`, `MES_DESEMBOLSO`, `VALOR_MENSAL_DESEMBOLSO` | Passo 5 — Previsão de Desembolso |

A senha (`SISCORP_SENHA`) é a única exceção: vai por variável de ambiente, não
por `--variable`.

### 3.5 Cuidados de segurança já resolvidos (não reverter)

- **Senha nunca aparece em log**: `Realizar Login no Sistema` e `Obter Senha
  SISCORP` envolvem toda manipulação da senha com `Set Log Level NONE` /
  restauração do nível anterior. Robot Framework loga automaticamente o
  retorno de qualquer `${var}=    Keyword`, então sem esse wrapping a senha
  vazaria em texto puro no `log.html`/`output.xml`. Se adicionar qualquer novo
  passo que toque na senha, replique esse padrão.
- **`--no-sandbox` / `--disable-dev-shm-usage`** em `Open Browser`: o Chrome se
  recusa a abrir com sandbox ativo quando o processo roda como usuário
  `root` (comum em WSL/containers) — sem essas flags, todo cadastro falharia
  com `SessionNotCreatedException: Chrome instance exited`.
- **`Set Window Size 1920 1080` em vez de `Maximize Browser Window`**:
  `Maximize Browser Window` depende de um fallback via JavaScript
  (`Runtime.evaluate` do CDP) que quebra em Chrome headless recente
  (`unknown command: 'Runtime.evaluate' wasn't found`). `Set Window Size` é
  um comando nativo do WebDriver e não tem esse problema.

---

## 4. `backend/` — API web (FastAPI)

### 4.1 Endpoints

Prefixo: `/api/executions`.

| Método | Rota | Faz o quê |
|---|---|---|
| `POST` | `/api/executions` | Recebe um `DemandaPCA` (JSON), cria uma linha `Execution` (status `pending`) e dispara o robô em background |
| `GET` | `/api/executions` | Lista todas as execuções, mais recente primeiro |
| `GET` | `/api/executions/{id}` | Detalhe de uma execução |
| `GET` | `/api/executions/{id}/console` | Texto do console (ao vivo, se ainda rodando; tail salvo, se já terminou) |
| `GET` | `/api/executions/{id}/report` | `report.html` gerado pelo Robot Framework |
| `GET` | `/api/executions/{id}/log` | `log.html` (log detalhado, com screenshots de falha) |
| `GET` | `/api/health` | Healthcheck simples |

### 4.2 Ciclo de vida de uma execução

1. `POST /api/executions` grava no SQLite (`executions.db`) com
   `status="pending"` e `payload_json` (o `DemandaPCA` inteiro, **sem** a
   senha — veja `exclude={"credenciais"}` em `executions.py`).
2. `robot_runner.start_execution` sobe uma `threading.Thread` (não bloqueia a
   requisição HTTP).
3. Essa thread monta `variables = _variables_for(demanda)`, escreve
   `--variable CHAVE:VALOR` para cada uma, e chama
   `subprocess.Popen(["robot", ...], env={**os.environ, "SISCORP_SENHA": senha})`.
4. Cada linha de stdout/stderr do robô é gravada em tempo real em
   `runs/<id>/console.log` (para o endpoint `/console` poder servir ao vivo).
5. Quando o processo termina, `status` vira `success` ou `failed`
   (`return_code == 0` ou não), `log_tail` guarda as últimas ~60 linhas, e
   `finished_at` é gravado.
6. `report.html`/`log.html`/`output.xml` ficam em `runs/<id>/` porque
   `--outputdir` aponta pra lá — os endpoints `/report` e `/log` só servem
   esses arquivos com `FileResponse`.

### 4.3 Como rodar

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Requer Chrome/Chromium instalado na máquina que roda o backend (é essa
máquina que efetivamente abre o navegador e acessa o SISCORP — não o
navegador de quem está preenchendo o formulário React).

---

## 5. `frontend/` — wizard web (React + Vite + TypeScript)

### 5.1 Estrutura de páginas (`react-router`)

| Rota | Página | Faz o quê |
|---|---|---|
| `/nova` (e `/`) | `NovaDemanda.tsx` | Wizard de 5 passos + credenciais, chama `api.criarExecucao` no fim |
| `/execucoes` | `Execucoes.tsx` | Tabela com histórico (via `api.listarExecucoes`) |
| `/execucoes/:id` | `ExecucaoDetalhe.tsx` | Console ao vivo (poll), botões para abrir relatório/log |

### 5.2 Camada de API (`src/api.ts`)

Client HTTP fino, sem biblioteca externa (`fetch` puro). Base URL vem de
`VITE_API_BASE` (padrão `http://localhost:8000`). `types.ts` espelha
manualmente os schemas Pydantic do backend — **se um campo mudar no
backend (`schemas.py`), tem que mudar aqui também**, não há geração
automática de tipos neste projeto.

### 5.3 Como rodar

```bash
cd frontend
npm install
npm run dev       # dev server em http://localhost:5173
npm run build     # build de produção em dist/
```

---

## 6. `desktop/` — app standalone (PySide6)

Mesmo domínio (mesmo wizard, mesmas variáveis do `.robot`), mas **arquitetura
bem diferente do par frontend/backend**: não existe cliente/servidor, tudo
roda no mesmo processo Qt. Pensado para ser distribuído como um único
executável Windows, sem o usuário final precisar instalar Python, subir um
servidor ou abrir porta nenhuma.

### 6.1 Fluxo de telas

```
LoginWidget                 NovaDemandaWidget (6 passos)         ExecucaoAtualWidget
┌─────────────┐   entrar    ┌─────────────────────────┐  executar  ┌──────────────────┐
│ usuário      │ ─────────▶ │ 1 Dados Básicos          │ ─────────▶│ console ao vivo   │
│ senha        │            │ 2 Itens de Contratação   │           │  (enquanto roda)  │
│ headless?    │            │ 3 Dados da Contratação   │           ├──────────────────┤
└─────────────┘             │ 4 Previsão de Duração    │           │ Laudo (ao fim)    │
                            │ 5 Previsão de Desembolso │           │  status + tiles   │
                            │ 6 Revisão e Execução     │           │  abrir relatório/  │
                            └─────────────────────────┘           │  log · nova exec. │
                                                                    └──────────────────┘
                                          ▲                                  │
                                          └───────── "Nova execução" ────────┘

Barra lateral, sempre visível após login: [Nova Demanda] [Execuções] ... [Sair]
```

- **Login é feito uma vez por sessão do app** (diferente do backend/frontend,
  onde a senha é digitada a cada execução). A senha fica só em memória
  (`Credenciais` em `app/models.py`), nunca é gravada em disco. "Sair" limpa
  esse estado e volta pra tela de login.
- `NovaDemandaWidget.definir_sessao(...)` (chamado por `MainWindow`
  logo após o login) é quem injeta usuário/senha/headless no `DemandaPCA`
  do wizard.
- Ao clicar em "Executar no SISCORP" (último passo), `NovaDemandaWidget`
  grava a execução no SQLite local (`app/db.py`), sobe uma `RobotRunnerThread`
  e a `MainWindow` navega para `ExecucaoAtualWidget`.

### 6.2 Como o robô roda aqui (diferença chave vs. o backend)

O backend chama `robot` **como processo separado** (`subprocess.Popen`). O
desktop chama `robot.run(...)` **in-process, dentro de uma `QThread`**
(`app/robot_runner.py`, classe `RobotRunnerThread`). Isso evita depender de
`robot` estar no `PATH` do sistema (importante para o `.exe` empacotado, que
carrega o Robot Framework embutido) e permite capturar cada linha de saída via
um objeto `_StreamAoVivo` (file-like) que grava em `console.log` **e** emite
um sinal Qt (`linha_recebida`) por linha, atualizando a UI em tempo real.

### 6.3 Persistência local

`app/db.py` usa `sqlite3` puro (sem SQLAlchemy/Pydantic — mais leve para
empacotar). Schema equivalente ao do backend (`Execucao` dataclass), mas sem
FastAPI/Pydantic no meio.

### 6.4 Caminhos e o modo "congelado" (`app/config.py`)

Esse arquivo é o ponto mais delicado de todo o desktop, porque ele se
comporta diferente rodando com `python main.py` (dev) vs. rodando o `.exe`
empacotado:

| | Modo dev (`python main.py`) | Modo empacotado (`sys.frozen`) |
|---|---|---|
| `ROBOT_FILE` | `../robot/cadastrar_pca.robot` (pasta irmã de `desktop/`) | `robot/cadastrar_pca.robot` dentro do bundle do PyInstaller (`sys._MEIPASS`) |
| `RUNS_DIR` / `DB_PATH` | Dentro de `desktop/` | Ao lado do executável (`sys.executable.parent`) — assim o histórico sobrevive a um `--onefile` que se descompacta em pasta temporária a cada execução |

**Se você mexer em `config.py`, sempre teste os dois modos** (rodando
`python main.py` e depois reempacotando com `build.sh`).

### 6.5 Como rodar em desenvolvimento

```bash
cd desktop
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Em WSL2 com WSLg (Windows 11), a janela aparece direto na área de trabalho
Windows sem configuração extra — só precisa de `DISPLAY`/`WAYLAND_DISPLAY`
já setados pelo ambiente (o WSLg faz isso sozinho).

### 6.6 Como empacotar (`build.sh`)

```bash
cd desktop
./build.sh
```

Isso roda:

```bash
pyinstaller --noconfirm --clean --name SiscorpPCA \
  --add-data "../robot/cadastrar_pca.robot:robot" \
  --collect-all robot \
  --collect-all SeleniumLibrary \
  --collect-all selenium \
  main.py
```

**As três flags `--collect-all` são obrigatórias e não intuitivas.** O Robot
Framework carrega bibliotecas como `BuiltIn`/`SeleniumLibrary` **dinamicamente
por nome**, não por `import` estático — o analisador de dependências do
PyInstaller não enxerga isso sozinho. Sem essas flags, o `.exe` compila
normalmente mas falha em runtime com:

```
[ ERROR ] Importing library 'robot.libraries.BuiltIn' failed:
Module 'robot.libraries' does not contain 'BuiltIn'.
```

O resultado fica em `desktop/dist/SiscorpPCA/`. **Rodar `build.sh` num Linux
gera um binário Linux; para gerar o `.exe` Windows, `build.sh` precisa ser
executado numa máquina/VM Windows** (PyInstaller não faz cross-compile) — no
Windows o separador do `--add-data` é `;`, não `:`.

### 6.7 Atalho de desktop (Windows)

Um atalho clicável foi criado na Área de Trabalho do Windows
(`SISCORP PCA.lnk`) que roda, oculto (sem janela de console), o binário em
`desktop/dist/SiscorpPCA/SiscorpPCA` via `wsl.exe -d Ubuntu`. Ele **não se
atualiza sozinho** — todo novo `build.sh` precisa ser rodado antes de o
atalho refletir mudanças de código.

---

## 7. Como estender o projeto

### 7.1 Adicionar um campo novo ao wizard

Um campo novo sempre toca **quatro lugares**, porque não há geração de código
entre as camadas:

1. **`robot/cadastrar_pca.robot`**: adicionar `${NOVA_VARIAVEL}` em
   `*** Variables ***` (com um valor default de teste) e usá-la na keyword do
   passo correspondente (ex. `Preencher Passo 2 - Itens de Contratacao`).
2. **Backend**: `schemas.py` (novo campo no sub-modelo Pydantic certo) +
   `robot_runner.py` (`_variables_for`, adicionar `"NOVA_VARIAVEL": ...`).
3. **Frontend**: `types.ts` (mesmo campo) + o `StepN...tsx` correspondente
   (novo `<Field>`).
4. **Desktop**: `app/models.py` (dataclass) + `variaveis_robot()` +
   `app/wizard/steps.py` (novo widget no `StepN...` certo).

Dica: use `grep -rn "NOME_DA_VARIAVEL_PARECIDA"` nos quatro componentes antes
de começar — copiar o padrão de um campo existente do mesmo tipo (texto,
combobox, data, monetário) é mais seguro que escrever do zero.

### 7.2 Adicionar um passo novo ao wizard

- No `.robot`: nova keyword `Preencher Passo N - <Nome>` + chamada dela em
  `Executar Etapa` dentro do `*** Test Cases ***`.
- Frontend: novo `StepN.tsx` + registrar em `NovaDemanda.tsx` (state machine
  de passos) + `StepIndicator.tsx`.
- Desktop: nova classe `StepN...` em `wizard/steps.py` + adicionar à lista em
  `STEP_META`/construção de `self.stepN` em `nova_demanda_widget.py`.

### 7.3 Se o layout do SISCORP mudar (seletores quebrarem)

O `.robot` é a única coisa que precisa mudar — nem backend, nem frontend, nem
desktop sabem como o SISCORP é feito por dentro, eles só passam variáveis.
Ajuste a keyword afetada em `robot/cadastrar_pca.robot`, rode
`robot --dryrun` para validar sintaxe, teste manualmente (veja seção 8), e
**lembre de reempacotar o desktop** (`./build.sh`) já que ele carrega uma
cópia embutida do arquivo.

---

## 8. Ambiente necessário e diagnóstico de problemas

### 8.1 Requisitos

- **Python 3.10+** (backend e desktop têm seus próprios `venv`/`requirements.txt`)
- **Node 18+** (frontend)
- **Chrome ou Chromium instalado** na máquina que efetivamente roda o robô
  (a do backend, ou a do usuário do app desktop) — `selenium` usa o Selenium
  Manager para baixar um `chromedriver` compatível automaticamente, desde
  que haja acesso à internet na primeira execução.
- **Acesso de rede** a `siscorp-pca-des.infrasa.gov.br` (VPN da INFRA S.A.,
  se aplicável) — sem isso, o robô abre o navegador mas nunca alcança a
  página de login.

### 8.2 Problemas já enfrentados neste projeto (e a causa raiz)

| Sintoma | Causa raiz | Correção |
|---|---|---|
| `[ ERROR ] Importing library 'robot.libraries.BuiltIn' failed` (só no `.exe` empacotado) | PyInstaller não inclui libs carregadas dinamicamente pelo Robot Framework | `--collect-all robot/SeleniumLibrary/selenium` no `build.sh` (ver 6.6) |
| `SessionNotCreatedException: Chrome instance exited` | Chrome recusa abrir com sandbox ativo rodando como `root` | `options=add_argument("--no-sandbox");add_argument("--disable-dev-shm-usage")` em `Open Browser` |
| Mesmo erro acima, mesmo com `--no-sandbox` | Binário do Chrome baixado pelo Selenium Manager estava **corrompido/incompleto** (download interrompido — `file` acusava "missing section headers", tamanho muito menor que o esperado) | Apagar `~/.cache/selenium` e instalar o Google Chrome oficial via `.deb`/pacote do sistema em vez de depender do download automático |
| `WebDriverException: unknown command: 'Runtime.evaluate' wasn't found` logo após abrir o navegador | `Maximize Browser Window` usa fallback via JS (CDP `Runtime.evaluate`) incompatível com Chrome headless recente | Trocado por `Set Window Size 1920 1080` (comando nativo do WebDriver) |
| Senha aparecendo em texto puro em `log.html`/`output.xml`/console | Robot Framework loga automaticamente o valor de retorno de `${var}=  Keyword`, e também o valor lido de volta de campos de senha via `Get Value` | `Set Log Level NONE` / restaurar em volta de toda manipulação da senha (ver 3.5) |

### 8.3 Como testar o `.robot` isoladamente (sem subir backend nem desktop)

```bash
# valida sintaxe sem executar de verdade
python3 -m robot --dryrun --outputdir /tmp/out robot/cadastrar_pca.robot

# execução real, sobrescrevendo variáveis específicas
SISCORP_SENHA="sua_senha" python3 -m robot \
  --variable USUARIO:seu.usuario \
  --variable NAVEGADOR:headlesschrome \
  --outputdir /tmp/out \
  robot/cadastrar_pca.robot
```

Depois, `/tmp/out/log.html` mostra passo a passo o que a automação fez
(incluindo screenshots automáticos em pontos de falha).

---

## 9. Segurança — regras que não devem ser quebradas

- A senha do SISCORP **nunca é persistida em disco** em nenhum dos três
  componentes (backend, frontend, desktop). Ela só existe: (a) na requisição
  HTTP/na tela de login, (b) na variável de ambiente `SISCORP_SENHA` do
  processo do robô durante aquela execução, (c) em memória, na sessão do app
  desktop.
- O `.robot` nunca deve logar a senha (ver 3.5). Qualquer keyword nova que
  manipule `${SENHA}`/`${senha_final}` precisa do mesmo wrapping
  `Set Log Level NONE`.
- `backend/executions.db`, `backend/runs/`, `desktop/execucoes.db` e
  `desktop/runs/` ficam fora do controle de versão (`.gitignore`) — eles
  acumulam histórico de execuções reais, que pode conter dados sensíveis do
  PCA.
