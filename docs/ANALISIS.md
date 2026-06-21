# Análisis - AgenciaCode Studio

## Problema
AgenciaCode Studio necesita un sistema centralizado para gestionar 
proyectos, colaboradores, clientes y tareas en lugar de usar Trello y chats.

## Solución
Sistema web MVC con:
- Autenticación de usuarios
- CRUD completo (Clientes, Colaboradores, Proyectos, Tareas)
- Asignación de colaboradores a proyectos (M:M)
- Asignación de tareas a colaboradores
- Reportes de productividad

## Reglas de Negocio
- Max 3 proyectos activos por colaborador
- No tareas en proyectos finalizados
- No eliminar proyectos con tareas en progreso
- Fechas coherentes (inicio < fin)

