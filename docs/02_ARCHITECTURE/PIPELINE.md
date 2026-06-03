# PIPELINE

## Visão Geral

Understat
        ↓
     Coleta
        ↓
SofaScore
        ↓
     RAW
        ↓
 Validação
        ↓
Transformação
        ↓
 PostgreSQL
        ↓
Dataset Analítico
        ↓
Pesquisa Quantitativa
        ↓
 Modelagem
        ↓
 Produção

## Princípios

- Dados brutos são preservados.
- Transformações são reproduzíveis.
- Cada etapa deve ser auditável.
- Nenhuma análise utiliza diretamente os arquivos RAW.