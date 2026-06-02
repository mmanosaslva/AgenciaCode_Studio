# Modelo Relacional - AgenciaCode Studio

## Tablas

### USERS
- PK: id
- username (UNIQUE, NOT NULL)
- password (NOT NULL)
- role (NOT NULL)

### CLIENTS
- PK: id
- name (NOT NULL)
- email
- sector
- phone

### COLLABORATORS
- PK: id
- name (NOT NULL)
- role (dev/designer/analyst)
- status (active/inactive)
- email
- phone

### PROJECTS
- PK: id
- FK: client_id → CLIENTS
- name (NOT NULL)
- status (active/finalized/cancelled)
- start_date
- end_date

### TASKS
- PK: id
- FK: project_id → PROJECTS
- FK: collaborator_id → COLLABORATORS
- title (NOT NULL)
- status (pending/in_progress/completed/cancelled)
- priority (low/medium/high/critical)
- due_date

### COLLABORATOR_PROJECT (Tabla intermedia M:M)
- PK: id
- FK: collaborator_id → COLLABORATORS
- FK: project_id → PROJECTS
- assigned_date

## Relaciones
- CLIENTS (1) ----< PROJECTS (N)
- PROJECTS (1) ----< TASKS (N)
- COLLABORATORS (M) ----< COLLABORATOR_PROJECT >---- PROJECTS (M)
- COLLABORATORS (1) ----< TASKS (N)
