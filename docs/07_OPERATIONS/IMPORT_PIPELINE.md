# IMPORT PIPELINE

## Fluxo

RAW
↓
Validação
↓
Transformação
↓
PostgreSQL
↓
Dataset Analítico

## Objetivo

Separar claramente coleta, armazenamento e análise.

## SofaScore Match Collector V2

Status:
Implementado

Funcionalidades:
- Leitura de inventory.json
- Coleta por event_id
- Coleta:
  - event.json
  - statistics.json
  - incidents.json
  - lineups.json
  - h2h.json
- Skip automático
- Delay configurável

Observação:
Após aproximadamente 250 requisições ocorreu HTTP 403.
Necessário investigar:
- Rate limiting
- Session limiting
- IP limiting
