-- ============================================
-- AGENCIACODE STUDIO - SCHEMA DE BASE DE DATOS
-- ============================================

CREATE DATABASE IF NOT EXISTS agenciacode_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agenciacode_db;

-- 1. TABLA USUARIOS (Autenticación)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA CLIENTES
CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    sector VARCHAR(100),
    email VARCHAR(120) UNIQUE,
    phone VARCHAR(15),
    contact_person VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sector (sector)
);

-- 3. TABLA COLABORADORES
CREATE TABLE collaborators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role ENUM('desarrollador', 'diseniador', 'analista') NOT NULL,
    status ENUM('activo', 'inactivo') DEFAULT 'activo',
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(15),
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_role (role),
    INDEX idx_status (status)
);

-- 4. TABLA PROYECTOS
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    client_id INT NOT NULL,
    status ENUM('planificacion', 'activo', 'pausado', 'finalizado', 'cancelado') DEFAULT 'planificacion',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_dates (start_date, end_date),
    CONSTRAINT chk_dates CHECK (start_date < end_date)
);

-- 5. TABLA TAREAS
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    collaborator_id INT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    priority ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    status ENUM('pendiente', 'en_progreso', 'en_revision', 'completada', 'cancelada') DEFAULT 'pendiente',
    due_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (collaborator_id) REFERENCES collaborators(id) ON SET NULL,
    INDEX idx_project (project_id),
    INDEX idx_collaborator (collaborator_id),
    INDEX idx_status (status)
);

-- 6. TABLA INTERMEDIA: COLABORADORES - PROYECTOS
CREATE TABLE collaborator_project (
    id INT AUTO_INCREMENT PRIMARY KEY,
    collaborator_id INT NOT NULL,
    project_id INT NOT NULL,
    assigned_date DATE DEFAULT CURDATE(),
    removed_date DATE,
    FOREIGN KEY (collaborator_id) REFERENCES collaborators(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_assignment (collaborator_id, project_id, removed_date),
    INDEX idx_collaborator (collaborator_id),
    INDEX idx_project (project_id)
);

-- VISTAS ÚTILES PARA REPORTES
CREATE VIEW vw_projects_summary AS
SELECT
    p.id,
    p.name AS project_name,
    c.name AS client_name,
    p.status,
    p.start_date,
    p.end_date,
    COUNT(t.id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completada' THEN 1 ELSE 0 END) AS completed_tasks
FROM projects p
JOIN clients c ON p.client_id = c.id
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id;

CREATE VIEW vw_collaborator_workload AS
SELECT
    col.id,
    col.name,
    col.role,
    COUNT(DISTINCT cp.project_id) AS active_projects,
    COUNT(DISTINCT t.id) AS assigned_tasks,
    SUM(CASE WHEN t.status = 'en_progreso' THEN 1 ELSE 0 END) AS tasks_in_progress
FROM collaborators col
LEFT JOIN collaborator_project cp ON col.id = cp.collaborator_id AND cp.removed_date IS NULL
LEFT JOIN tasks t ON col.id = t.collaborator_id AND t.status != 'cancelada'
GROUP BY col.id;

-- ÍNDICES ADICIONALES
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX idx_tasks_collaborator_status ON tasks(collaborator_id, status);

-- TRIGGER: Prevenir asignación a más de 3 proyectos activos
DELIMITER $$
CREATE TRIGGER tr_check_max_projects
BEFORE INSERT ON collaborator_project
FOR EACH ROW
BEGIN
    DECLARE active_count INT;
    SELECT COUNT(*) INTO active_count
    FROM collaborator_project cp
    JOIN projects p ON cp.project_id = p.id
    WHERE cp.collaborator_id = NEW.collaborator_id
      AND p.status = 'activo'
      AND cp.removed_date IS NULL;
    IF active_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Colaborador ya tiene 3 proyectos activos';
    END IF;
END$$
DELIMITER ;

-- TRIGGER: Prevenir tareas en proyectos finalizados/cancelados
DELIMITER $$
CREATE TRIGGER tr_check_project_status
BEFORE INSERT ON tasks
FOR EACH ROW
BEGIN
    DECLARE proj_status VARCHAR(50);
    SELECT status INTO proj_status FROM projects WHERE id = NEW.project_id;
    IF proj_status IN ('finalizado', 'cancelado') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se pueden crear tareas en proyectos finalizados o cancelados';
    END IF;
END$$
DELIMITER ;
