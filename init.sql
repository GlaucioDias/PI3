-- Criação do banco de dados pi3
USE pi3;

ALTER USER 'flask'@'%' IDENTIFIED WITH mysql_native_password BY 'flask123';
FLUSH PRIVILEGES;

-- Tabela de cidades
CREATE TABLE IF NOT EXISTS cidades (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de eventos
CREATE TABLE IF NOT EXISTS eventos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  descricao TEXT,
  cidade_id INT,
  data DATE NOT NULL,
  horario TIME NOT NULL,
  endereco VARCHAR(255),
  imagem VARCHAR(255),
  usuario_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (cidade_id) REFERENCES cidades(id),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserir cidades padrão
INSERT INTO cidades (nome) VALUES 
('São Paulo'),
('Rio de Janeiro'),
('Belo Horizonte'),
('Brasília'),
('Salvador'),
('Fortaleza'),
('Manaus'),
('Recife'),
('Curitiba'),
('Porto Alegre')
ON DUPLICATE KEY UPDATE nome=VALUES(nome);
