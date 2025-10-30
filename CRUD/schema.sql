DROP DATABASE IF EXISTS biblioteca;
CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE biblioteca;

-- Tabela de autores
CREATE TABLE autores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  nacionalidade VARCHAR(80)
);

-- Tabela de livros
CREATE TABLE livros (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  ano_publicacao INT,
  isbn VARCHAR(20) UNIQUE
);

CREATE TABLE livros_autores (
  livro_id INT NOT NULL,
  autor_id INT NOT NULL,
  PRIMARY KEY (livro_id, autor_id),
  CONSTRAINT fk_livros_autores_livro FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE,
  CONSTRAINT fk_livros_autores_autor FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE
);

CREATE TABLE tomadores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE,
  telefone VARCHAR(30)
);

CREATE TABLE emprestimos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  livro_id INT NOT NULL,
  tomador_id INT NOT NULL,
  data_emprestimo DATE NOT NULL,
  data_devolucao DATE,
  CONSTRAINT fk_emp_livro FOREIGN KEY (livro_id) REFERENCES livros(id),
  CONSTRAINT fk_emp_tomador FOREIGN KEY (tomador_id) REFERENCES tomadores(id)
);

-- Dados mínimos para testes
INSERT INTO autores (nome, nacionalidade) VALUES
  ('Machado de Assis', 'Brasil'),
  ('José de Alencar', 'Brasil'),
  ('Clarice Lispector', 'Brasil');

INSERT INTO livros (titulo, ano_publicacao, isbn) VALUES
  ('Dom Casmurro', 1899, '978-85-359-0277-7'),
  ('O Guarani', 1857, '978-85-359-0350-7'),
  ('A Hora da Estrela', 1977, '978-85-359-0433-7');

INSERT INTO livros_autores (livro_id, autor_id) VALUES
  (1, 1),
  (2, 2),
  (3, 3);

INSERT INTO tomadores (nome, email, telefone) VALUES
  ('Ana Souza', 'ana@email.com.br', '(11) 99999-0001'),
  ('Bruno Lima', 'bruno@email.com.br', '(11) 99999-0002');

INSERT INTO emprestimos (livro_id, tomador_id, data_emprestimo) VALUES
  (1, 1, '2025-10-01'),
  (3, 2, '2025-10-15');
