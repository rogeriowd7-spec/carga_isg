# Estrutura do Drive "Gerencia de contratos" — pastas GC

Varredura feita em 03/10/2026 com `scripts/varrer_drive.py` sobre a pasta pública
`11x0ks5TF3Td1vZJ6LfmJEsDn9CwAskDH`, só nas 13 pastas que começam com "GC ".
Níveis 1 a 6 lidos por completo (~207 mil itens); abaixo disso são processos de
pagamento, notas e certidões, que não mudam o diagnóstico.

## O padrão que existe por baixo

Quase todas as unidades guardam cada contrato como uma **pasta de processo**, com o
mesmo miolo (é o fluxo de `GC SEDE / 8. MODELOS / Processo de contratação`):

```
<nº>-<ano> - <objeto> (<empresa>)
    Andamento do processo
    Propostas
    Documentos da empresa
    Contrato  |  Contrato e Aditivos      <- o arquivo que interessa ao Fluig
    Processo Integral ... .pdf
```

O que muda de unidade para unidade é o que está **em volta** desse miolo.

## As três variações

1. **Hierarquia acima do processo** (como chegar até a pasta do contrato)
2. **Nome da pasta do processo** (onde estão número, ano, objeto, empresa e status)
3. **Onde fica o arquivo do contrato** dentro da pasta

## Unidade por unidade

| Unidade | Caminho até o contrato | Nome da pasta do processo | Vigente x encerrado |
|---|---|---|---|
| SEDE | `1. CONTRATOS / <ano>` | `001-2025 Objeto (EMPRESA) 🚨/OK` | emoji no nome |
| HRSJC | `1.CONTRATOS / PJ MÉDICA - <ano>` e `SERVIÇOS - <ano>` | `Contrato 002-2020_Objeto_EMPRESA[_Cancelado]` | sufixo `_Cancelado` |
| HRLN | `N.0 Contratos <ano> - HRLN / Médicos / Não Médicos` | `Contrato 001-2025 - Objeto[ - CANCELADO ❌]` | sufixo |
| AME SJC | `Contratos [Nao] Medicos - AMESJC / <ano>` | `Processo 002-2025_Objeto_Empresa` | subpasta `_Rescindidos e Encerrados`, `_Contratacoes Canceladas` |
| AME PA | `Contratos AMEPA / Contratos - [Não] Médicos / 0N - Contratos <ano>` | `001.2024 - Objeto` ou `Contrato 001-2022 - Objeto - Rescindido` | sufixo; subpastas numeradas `00 - Contrato` |
| HRCFVH | `1 - CONTRATOS / 1 - SERVIÇOS MÉDICOS_FISIO` (sem ano) e `2 - SERVIÇOS NÃO MÉDICO / <ano>` | `001.2025 - Objeto (EMPRESA)` e `001-2026 - Objeto` | sufixo `- encerrado`/`- Cancelado` |
| HRJR | `HRJR / 1.Contratos Medicos / Contratos Médicos <ano>` e `2.Contratos Serviços / Contratos <ano>` | `01-24 Objeto` (ano com 2 dígitos) ou `CONTRATO 001-2019 OBJETO` | pasta `2. SERVIÇOS FINALIZADOS OU RESCINDIDOS`; planilha `1.Contratos Vigentes - HRJR.xlsx` |
| HRR | `CONTRATOS [NÃO] MÉDICOS / <ano>` + `CONTRATOS HRR` (100 PDFs soltos por empresa) | `CONTRATO 001-2022 OBJETO` | não marca; `RELAÇÃO DE CONTRATOS HRR.xlsx` |
| HDT | `HDT / 01. CONTRATOS VIGENTES / <tipo>` e `05. CONTRATOS ENCERRADOS` | `Objeto - EMPRESA (003.2026)` — número no fim, entre parênteses | **pasta própria de vigentes**, separada por tipo (Fornecimento, Locação, Médicos, Não Médicos) |
| CEAP-SOL | `1.Contratos Aditivos Ceap-Sol / <Empresa>` | pasta por **empresa**, contrato e aditivos como arquivo solto | subpasta `Contrato antigo` |
| HEAL | `Diversos / <Empresa>`, `Aditivos diversos`, `Assinados` | arquivos soltos (`CONTRATO_ARSERVICE_023.2021.pdf`) | nada após 2022 |
| HERC | `Processos digitalizados - HERC / CAIXA NN` | processos digitalizados 2013–2016 | acervo |
| HRLN 1 | vazia | — | — |

## O que isso significa para a carga no Fluig

- **A unidade de carga é a pasta do processo**, não o arquivo. Em 10 das 13 pastas ela
  existe; em CEAP-SOL e HEAL é a pasta da empresa; HERC e HRLN 1 ficam fora.
- **Número e ano saem do nome da pasta** com 4 formatos: `001-2025`, `001.2025`,
  `01-24` e `(003.2026)` no fim. Objeto e empresa vêm em posições diferentes por unidade.
- **Status (vigente, cancelado, encerrado) está em 4 lugares diferentes**: sufixo no nome,
  emoji, subpasta de encerrados ou pasta própria de vigentes (HDT). Não dá para confiar
  num único critério — é a pergunta que a unidade precisa responder.
- **O arquivo do contrato fica dentro de `Contrato`/`Contrato e Aditivos`/`00 - Contrato`/
  `3. Contrato`**, quase sempre com versões `.docx`, `.pdf` e `_ASS.pdf`. Escolher qual é o
  assinado é decisão da unidade, não do script.
- Várias unidades já mantêm planilha de vigentes (`Contratos Vigentes.xlsx` no HRCFVH,
  `1.Contratos Vigentes - HRJR.xlsx`, `Vigencia de contratos.xlsx` no AME SJC,
  `GC SEDE / 9. UNIDADES / Contratos ATUAL`). Servem para pré-preencher, não como verdade.
