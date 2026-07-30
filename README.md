<p align="center">
  <img src="infra_logo.png" alt="INFRA TESTER" width="220"/>
</p>

<h1 align="center">INFRA TESTER</h1>

<p align="center">
  Automação de cadastro no SISCORP PCA — frontend, backend e robô Selenium.
</p>

Frontend + backend que colocam um formulário (wizard de 5 passos) na frente do
robô Robot Framework/Selenium (`robot/cadastrar_pca.robot`), que continua sendo
o motor real de automação: ele é quem loga e preenche o SISCORP no navegador,
já que o SISCORP não expõe API própria.

> Documentação técnica completa (arquitetura dos 4 componentes, como rodar
> cada um, como estender, troubleshooting): ver [`ARQUITETURA.md`](ARQUITETURA.md).

## Demonstração e documentação

- 📑 **Arquitetura (PDF):** [`INFRA_TESTER_arquitetura.pdf`](INFRA_TESTER_arquitetura.pdf)
- 🎬 **Vídeo de apresentação:**

  <video src="https://github.com/mickeiascharles/INFRA-TESTER/raw/master/apresentacao.mp4" controls width="600">
    Seu visualizador não suporta vídeo embutido — baixe em <a href="apresentacao.mp4">apresentacao.mp4</a>.
  </video>

  > Se o player acima não carregar, assista/baixe diretamente em [`apresentacao.mp4`](apresentacao.mp4).

## Arquitetura

```
frontend/   React + Vite + TypeScript — wizard de cadastro + histórico de execuções
backend/    FastAPI — recebe os dados do formulário, dispara o robô como
            subprocesso, guarda histórico em SQLite e expõe log/report
robot/      script Robot Framework/Selenium usado pelo backend e pelo desktop
            (motor real da automação — quem loga e preenche o SISCORP)
```

Fluxo: usuário preenche o wizard → backend grava uma `Execution` (status
`pending`) → dispara `robot --variable CHAVE:VALOR ... robot/cadastrar_pca.robot`
em background, injetando a senha via variável de ambiente `SISCORP_SENHA` →
console é gravado em tempo real e pode ser acompanhado pela tela de detalhe da
execução → ao final, `report.html` e `log.html` gerados pelo Robot Framework
ficam disponíveis para download.

Todos os campos do wizard usam os mesmos nomes de variável do `.robot`
original (`ANO_PCA`, `AREA_DEMANDANTE`, `CODIGO_SUBITEM`, etc.), então nenhuma
lógica de preenchimento de tela precisou ser reescrita — o backend só troca os
valores por execução.

## Rodando localmente

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Também é necessário ter um Chrome/Chromium instalado na máquina que vai
executar o robô (o Selenium Manager baixa o chromedriver compatível
automaticamente, na primeira execução, desde que haja acesso à internet).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse `http://localhost:5173`. O frontend espera a API em
`http://localhost:8000` (ajustável via `VITE_API_BASE` em `frontend/.env`).

## Limitação conhecida deste ambiente

Este sandbox de desenvolvimento não tem Chrome instalado nem acesso de rede ao
host real (`siscorp-pca-des.infrasa.gov.br`), então a automação Selenium não
pôde ser validada contra o sistema de verdade a partir daqui. O que foi
validado:

- `robot --variable ...` recebe corretamente todos os campos do formulário
  (confirmado via execução de teste: a senha chegou via `SISCORP_SENHA` e o
  robô iniciou a etapa `Realizar Login no Sistema` normalmente).
- API (`POST/GET /api/executions`, `/console`, `/report`, `/log`) e frontend
  (build de produção + type-check) funcionam de ponta a ponta.

Para validar o cadastro real, rode o backend numa máquina com Chrome instalado
e acesso à rede da INFRA S.A. (VPN, se aplicável) e informe um usuário/senha
válidos do SISCORP no último passo do wizard.

## Segurança

- A senha do SISCORP não é persistida: ela só existe na requisição HTTP e na
  variável de ambiente do processo do robô durante aquela execução.
- `backend/executions.db` e `backend/runs/` (histórico e artefatos de log)
  ficam fora do controle de versão — veja `.gitignore`.
