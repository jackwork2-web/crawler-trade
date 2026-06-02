# DATA DISCOVERY

Este documento registra toda nova estatística, campo, endpoint ou métrica descoberta durante o projeto.

## Regras

1. Nenhuma descoberta deve ser perdida.
2. Descobertas não precisam ser implementadas imediatamente.
3. Ao final de cada entrega, novos campos encontrados devem ser registrados aqui.
4. A decisão de coletar ou não será tomada posteriormente.

---

## Descobertas Atuais

# FotMob Discovery Notes – June 2026

## Working Endpoint

Confirmed working:

https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025

### Available Data

fixtures.allMatches includes:

* id
* home team
* away team
* match status
* match date
* pageUrl

The id field corresponds to FotMob Match ID.

---

## Premier League Validation

League:

Premier League

League ID:

47

Season:

2024/2025

Matches discovered:

380

Matches mapped:

369

Unmapped:

11

---

## MatchDetails Investigation

Endpoint:

https://www.fotmob.com/api/data/matchDetails?matchId=XXXX

### Direct Requests

Result:

403

Response:

TURNSTILE_REQUIRED

---

### Playwright Interception

Status:

Partial Success

Observed:

* request URL detected
* endpoint confirmed
* response blocked

---

### Historical Evidence

File:

matchdetails.json

Contains:

* momentum
* expectedGoals
* expectedGoalsOnTarget
* playerStats
* attackingZones
* events
* matchFacts

Conclusion:

MatchDetails payload was successfully captured at least once in the past.

Current reproduction method remains unknown.

---

## Research Direction

Future investigation should focus on:

1. Reproducing historical capture workflow.
2. Browser session persistence.
3. Alternative snapshot providers.
4. Multi-source architecture.


### Momentum
Fonte: FotMob
Status: S

Descrição:
Pressão minuto a minuto.

Faixa observada:
-100 a +100

Observações:
- 94 registros observados em um jogo.
- Inclui acréscimos (ex.: 45.5, 90.25, 90.5, 90.75).
- Única série temporal nativa identificada até o momento.

---

### Goal (Shotmap)
Fonte: FotMob
Status: S

Descrição:
Gols são registrados dentro de shotmap.shots através de eventType='Goal'.

Campos validados:
- min
- minAdded
- teamId
- playerName
- expectedGoals

---

### Touches in Opposition Box
Fonte: FotMob
Status: S

Descrição:
Quantidade de toques na área adversária.

Observação:
Substitui Dangerous Attacks como principal métrica de pressão ofensiva.

---

### Shots on Target
Fonte: FotMob
Status: S

### Total Shots
Fonte: FotMob
Status: S

### Expected Goals (xG)
Fonte: FotMob
Status: S

### Big Chances
Fonte: FotMob
Status: S

---

### PPDA
Fonte: Understat
Status: A

### Deep
Fonte: Understat
Status: A

### Big Chances Missed
Fonte: FotMob
Status: A

### Corners
Fonte: FotMob
Status: A

### xGOT
Fonte: FotMob
Status: A

### Shots Inside Box
Fonte: FotMob
Status: A

---

### Attacking Zones
Fonte: FotMob
Status: B

Descrição:
Distribuição espacial dos ataques por lado do campo.

Observação:
Não é série temporal.

---

### PlayerStats
Fonte: FotMob
Status: B

Descrição:
Estatísticas finais e shotmap individual.

Observação:
Não é série temporal.

---

### Heatmap
Fonte: FotMob
Status: PENDENTE

### Accurate Crosses
Fonte: FotMob
Status: PENDENTE

### Successful Dribbles
Fonte: FotMob
Status: PENDENTE

### Offsides
Fonte: FotMob
Status: PENDENTE
