-- ============================================
-- AGENCIACODE STUDIO - DATOS DE PRUEBA
-- ============================================
SET NAMES utf8mb4;
USE agenciacode_db;

-- USUARIOS
INSERT INTO users (username, password_hash, role, name, email) VALUES
('admin', '$2b$12$cWqUmg1O0LjX34nC3Bm.eOENCmTp4bIPBqIsevI1hrdyeKLFcA2Ui', 'admin', 'Administrador', 'admin@agenciacode.com'),
('usuario1', '$2b$12$nD.JV1UbUTM1EKdEQb9LV..er2WiDTjy4vxfHsddOmjgf3HBvzOOa', 'user', 'Usuario Prueba', 'usuario1@agenciacode.com');

-- CLIENTES
INSERT INTO clients (name, sector, email, phone, contact_person) VALUES
('TechCorp Solutions', 'Tecnología', 'contacto@techcorp.com', '555-0101', 'Laura Martínez'),
('DesignLab Studio', 'Diseño', 'info@designlab.com', '555-0202', 'Carlos Vega'),
('FinanceGroup SA', 'Finanzas', 'admin@financegroup.com', '555-0303', 'Ana Torres'),
('HealthFirst Inc', 'Salud', 'contact@healthfirst.com', '555-0404', 'Pedro López'),
('EduLearn Platform', 'Educación', 'info@edulearn.com', '555-0505', 'Sofía Ruiz');

-- COLABORADORES
INSERT INTO collaborators (name, role, status, email, phone, hire_date) VALUES
('Juan Pérez', 'desarrollador', 'activo', 'juan.perez@agenciacode.com', '555-1001', '2025-01-15'),
('María García', 'diseniador', 'activo', 'maria.garcia@agenciacode.com', '555-1002', '2025-02-01'),
('Carlos López', 'analista', 'activo', 'carlos.lopez@agenciacode.com', '555-1003', '2025-03-10'),
('Ana Rodríguez', 'desarrollador', 'activo', 'ana.rodriguez@agenciacode.com', '555-1004', '2025-04-20'),
('Luis Fernández', 'diseniador', 'inactivo', 'luis.fernandez@agenciacode.com', '555-1005', '2025-05-05'),
('Elena Martínez', 'analista', 'activo', 'elena.martinez@agenciacode.com', '555-1006', '2025-06-15'),
('Diego Sánchez', 'desarrollador', 'activo', 'diego.sanchez@agenciacode.com', '555-1007', '2025-07-01'),
('Sofía Torres', 'diseniador', 'activo', 'sofia.torres@agenciacode.com', '555-1008', '2025-08-10');

-- PROYECTOS
INSERT INTO projects (name, client_id, status, start_date, end_date, description) VALUES
('Rediseño Web Corporativo', 1, 'activo', '2026-01-01', '2026-06-30', 'Rediseño completo del sitio web corporativo de TechCorp'),
('App Móvil de Gestión', 1, 'activo', '2026-02-01', '2026-08-31', 'Aplicación móvil para gestión de inventarios'),
('Plataforma E-learning', 5, 'activo', '2026-03-01', '2026-09-30', 'Plataforma de cursos en línea para EduLearn'),
('Dashboard Financiero', 3, 'planificacion', '2026-04-01', '2026-10-31', 'Dashboard de indicadores financieros en tiempo real'),
('Sistema de Turnos Médicos', 4, 'activo', '2026-01-15', '2026-07-15', 'Sistema de gestión de turnos para clínicas'),
('Branding y Manual Corporativo', 2, 'finalizado', '2025-11-01', '2026-02-28', 'Desarrollo de identidad visual completa'),
('ERP Interno', 3, 'activo', '2026-05-01', '2026-12-31', 'Sistema ERP para FinanceGroup'),
('Landing Page', 2, 'cancelado', '2026-01-01', '2026-01-31', 'Landing page promocional');

-- ASIGNACIONES COLABORADOR-PROYECTO
INSERT INTO collaborator_project (collaborator_id, project_id, assigned_date) VALUES
(1, 1, '2026-01-02'), (2, 1, '2026-01-05'), (3, 1, '2026-01-10'),
(1, 2, '2026-02-05'), (4, 2, '2026-02-10'), (7, 2, '2026-02-15'),
(5, 3, '2026-03-05'), (6, 3, '2026-03-10'), (8, 3, '2026-03-15'),
(2, 4, '2026-04-05'), (4, 5, '2026-01-20'), (7, 5, '2026-01-25'),
(1, 6, '2025-11-05'), (2, 6, '2025-11-10'),
(3, 7, '2026-05-05'), (6, 7, '2026-05-10'), (8, 7, '2026-05-15'),
(5, 8, '2026-01-02');

-- TAREAS
INSERT INTO tasks (project_id, collaborator_id, title, description, priority, status, due_date) VALUES
(1, 1, 'Configurar servidor web', 'Instalar y configurar Apache/Nginx', 'alta', 'completada', '2026-02-01'),
(1, 1, 'Desarrollar componentes frontend', 'Crear componentes React del dashboard', 'alta', 'en_progreso', '2026-04-30'),
(1, 2, 'Diseñar mockups de páginas', 'Diseños en Figma para todas las páginas', 'media', 'completada', '2026-03-01'),
(1, 3, 'Análisis de requerimientos', 'Documento completo de requerimientos', 'alta', 'completada', '2026-02-15'),
(2, 1, 'API REST de usuarios', 'Desarrollar endpoints de autenticación', 'critica', 'en_progreso', '2026-05-01'),
(2, 4, 'Base de datos de la app', 'Diseñar esquema y migraciones', 'alta', 'completada', '2026-04-01'),
(2, 7, 'Pruebas unitarias backend', 'Tests con pytest para la API', 'media', 'pendiente', '2026-06-01'),
(3, 5, 'Diseño de interfaz educativa', 'Mockups de la plataforma de cursos', 'alta', 'completada', '2026-04-15'),
(3, 6, 'Modelado de datos educativos', 'Esquema de cursos, estudiantes y progreso', 'alta', 'en_progreso', '2026-05-15'),
(3, 8, 'Prototipo interactivo', 'Prototipo navegable en Figma', 'media', 'pendiente', '2026-06-30'),
(5, 4, 'Módulo de registro de pacientes', 'CRUD de pacientes', 'critica', 'en_progreso', '2026-04-15'),
(5, 7, 'Módulo de agenda', 'Sistema de turnos y agenda médica', 'alta', 'en_progreso', '2026-05-15'),
(7, 3, 'Análisis de procesos financieros', 'Documento de procesos actuales', 'alta', 'pendiente', '2026-06-15'),
(7, 6, 'Diseño de dashboard financiero', 'Mockups y prototipos', 'media', 'pendiente', '2026-07-01'),
(7, 8, 'UX Research', 'Entrevistas con usuarios', 'baja', 'pendiente', '2026-06-01');
