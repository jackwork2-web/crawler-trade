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

Descrição:
Indicador de intensidade de pressão.

---

### Deep
Fonte: Understat
Status: A

Descrição:
Entradas em zonas ofensivas profundas.

---

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
Status: PENDENTE

### Heatmap
Fonte: FotMob
Status: PENDENTE

### PlayerStats
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