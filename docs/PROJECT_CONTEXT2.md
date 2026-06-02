# LateGoalResearch - Project Context

## Objetivo
Construir uma base histórica completa de futebol para pesquisa quantitativa.

Foco inicial:
- Over 0.5 FT
- Gols tardios
- Pressão ofensiva

## Stack
- Python 3.12
- PostgreSQL
- SQLAlchemy
- Playwright
- Understat
- FotMob

## Estado Atual

### Banco
Database: late_goal_research

Tabelas existentes:
- matches
- team_match_stats
- snapshots
- events
- results

### Understat
Concluído.

Dados EPL 2024/2025 importados.

- 380 partidas
- 760 registros team_match_stats

Campos validados:
- xG
- xGA
- npxG
- npxGA
- PPDA
- PPDA Allowed
- Deep
- Deep Allowed
- xPts
- npxGD

### FotMob
Concluído acesso via Playwright.

Endpoint validado:
matchDetails

Estrutura validada:
- shotmap
- stats
- momentum
- matchFacts.events
- playerStats
- lineup
- attackingZones

## Descobertas

### Momentum
Disponível minuto a minuto.

Faixa observada:
-100 a +100

Interpretação:
-100 = pressão visitante
0 = equilíbrio
+100 = pressão mandante

### Shotmap
Disponível para cada finalização.

Campos relevantes:
- minute
- xG
- expectedGoalsOnTarget
- isOnTarget
- teamId
- situation
- shotType

### Events
Tipos observados:
- Comment
- Substitution
- Card
- AddedTime
- Half
- Red
- Yellow

## Decisões Arquiteturais

1. Salvar snapshots minuto a minuto.
2. Incluir acréscimos.
3. Não reduzir volume de dados nesta fase.
4. Priorizar coleta completa antes de modelagem.

## Próximos Marcos

MARCO 4
- fotmob_events_import.py

MARCO 5
- snapshot_builder.py

MARCO 6
- importação histórica FotMob

MARCO 7
- análises quantitativas

MARCO 8
- modelos preditivos

## Regras para Agentes

Antes de iniciar qualquer tarefa:
1. Ler este arquivo.
2. Consultar BACKLOG.md.
3. Preservar decisões registradas em DECISIONS.md.
4. Não remover dados sem aprovação humana.
5. Priorizar coleta e qualidade da base histórica.
