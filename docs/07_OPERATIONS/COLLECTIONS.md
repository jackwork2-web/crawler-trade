# COLLECTIONS

## Objetivo

Padronizar processos de coleta.

## Fontes

- Understat
- SofaScore
- FotMob

## Regras

- Toda coleta deve ser reproduzível.
- Dados brutos devem ser preservados.
- Não sobrescrever dados sem versionamento.

## Premier League 2025/26

Status:
Em andamento

Season ID:
61627

Artefatos gerados:
- inventory.json
- rounds.json
- round_01_events.json
- ...
- round_38_events.json

Match Collection:
50 partidas coletadas com sucesso

Formato:
matches/{event_id}/
├── event.json
├── statistics.json
├── incidents.json
├── lineups.json
└── h2h.json

Bloqueio encontrado:
HTTP 403 após aproximadamente 250 requisições.
