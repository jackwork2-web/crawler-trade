# BACKLOG

## Concluído
- [x] Criar fotmob_events_import.py
- [x] Mapear eventos do FotMob
- [x] Importar eventos Shotmap para events_v2
- [x] Validar Goal, AttemptSaved e Miss
- [x] Identificar teamId mandante e visitante
- [x] Criar snapshot_builder_v1.py
- [x] Validar Snapshot Builder V1
- [x] Descobrir estrutura do Momentum
- [x] Integrar Momentum aos snapshots
- [x] Criar snapshot_builder_v2.py
- [x] Persistir snapshots na tabela snapshots

## Em andamento
- [ ] Criar Match Mapper (Understat ↔ FotMob)
- [ ] Definir estratégia de captura em lote

## Próximos marcos
- [ ] Automatizar descoberta do fotmob_match_id
- [ ] Batch Capture FotMob
- [ ] Batch Import de eventos
- [ ] Batch Snapshot Builder
- [ ] Importar EPL completa
- [ ] Construir análises Over 0.5 FT
- [ ] Avaliar Momentum como variável preditiva
- [ ] Comparar Touches Box vs Momentum

# HIGH PRIORITY

## Historical Data Expansion

Status: OPEN

Tasks:

* Import EPL 2021/2022
* Import EPL 2022/2023
* Import EPL 2023/2024
* Import EPL 2025/2026
* Expand to additional leagues

Priority: High

---

## Odds Integration

Status: OPEN

Tasks:

* Evaluate odds sources
* Create odds ingestion pipeline
* Link odds to matches table

Priority: High

---

# MEDIUM PRIORITY

## Alternative Snapshot Sources

Status: OPEN

Evaluate:

* SofaScore
* Flashscore
* FBref
* StatsBomb Open Data
* SoccerNet
* API-Football

Goal:

Replace dependence on a single provider.

---

## Snapshot Data Standardization

Status: OPEN

Create a provider-agnostic snapshot schema.

Potential fields:

* minute
* score
* momentum
* attacks
* dangerous attacks
* xG progression

---

# RESEARCH BLOCKED

## FotMob MatchDetails Automation

Status: BLOCKED

Evidence:

* Endpoint discovered
* Historical payload exists
* Current requests return TURNSTILE_REQUIRED

Attempts Completed:

* requests
* custom headers
* x-mas header
* Playwright interception
* browser automation

Current Recommendation:

Pause active investigation.

Resume only after core historical database is completed.

Priority: Deferred
