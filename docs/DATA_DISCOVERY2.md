# DATA DISCOVERY

Este documento registra toda nova estatística, campo, endpoint ou métrica descoberta durante o projeto.

## Regras

1. Nenhuma descoberta deve ser perdida.
2. Descobertas não precisam ser implementadas imediatamente.
3. Ao final de cada entrega, novos campos encontrados devem ser registrados aqui.
4. A decisão de coletar ou não será tomada posteriormente.

---

## Descobertas Atuais

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

---

### FotMob matches by date
Fonte: FotMob
Status: S

URL:
https://www.fotmob.com/api/matches?date=YYYYMMDD

Descricao:
Endpoint historicamente usado para listar partidas por data. A estrutura esperada contem `leagues[].matches[]`, com `match_id`/`id`, mandante, visitante, liga e status.

Utilidade:
Permite descobrir `fotmob_match_id` cruzando data, time mandante e time visitante.

Observacoes:
- Em 2026-06-02, o endpoint retornou HTML/404 no ambiente testado.
- O mapper implementado mantem suporte ao endpoint, mas tambem aceita cache CSV/RDS.

---

### worldfootballR_data FotMob cache
Fonte: worldfootballR_data
Status: S

URL:
https://github.com/JaseZiv/worldfootballR_data/releases/download/fotmob_matches_by_date/47_matches_by_date.rds

Dados encontrados:
- `date`
- `home_name`
- `away_name`
- `match_id`
- `match_status_utc_time`
- `match_status_score_str`
- liga e pais

Utilidade:
Fonte auxiliar para mapeamento historico Understat x FotMob quando o endpoint ao vivo estiver bloqueado. Validado em 10 partidas da EPL 2024/25 com 100% de sucesso.

---

### Datarium FotMob proxy
Fonte: Datarium
Status: A

URL:
https://datarium.top/

Dados encontrados:
Documentacao publica menciona endpoints de proxy para FotMob, incluindo detalhes de partidas, ligas, standings e fixtures.

Potencial utilidade:
Pode ser alternativa para descoberta de partidas e enriquecimento de detalhes se o endpoint direto do FotMob ficar instavel. Nao implementado nesta fase.

---

### SportsAPI Pro football match endpoints
Fonte: SportsAPI Pro
Status: A

URL:
https://docs.sportsapipro.com/api-reference/football-v2/match

Dados encontrados:
Documentacao cita endpoints para schedule por data, match details, analytics, odds, lineups e shotmaps.

Potencial utilidade:
Pode ser alternativa paga/externa para timeline de estatisticas e busca de match ids. Nao implementado nesta fase.
