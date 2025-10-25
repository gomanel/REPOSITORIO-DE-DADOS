CREATE DATABASE IF NOT EXISTS biblioteca
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE biblioteca;

CREATE TABLE autor (
  autorId INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE livro (
  livroId INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  isbn VARCHAR(20) UNIQUE,
  anoPublicacao INT,
  totalCopias INT NOT NULL DEFAULT 1,
  copiasDisponiveis INT NOT NULL DEFAULT 1,
  CONSTRAINT chk_copias CHECK (totalCopias >= 0 AND copiasDisponiveis >= 0 AND totalCopias >= copiasDisponiveis)
) ENGINE=InnoDB;

CREATE TABLE livroAutor (
  livroId INT NOT NULL,
  autorId INT NOT NULL,
  PRIMARY KEY (livroId, autorId),
  CONSTRAINT fk_la_livro FOREIGN KEY (livroId) REFERENCES livro(livroId) ON DELETE CASCADE,
  CONSTRAINT fk_la_autor FOREIGN KEY (autorId) REFERENCES autor(autorId) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE tomador (
  tomadorId INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  email VARCHAR(150) UNIQUE,
  dataCadastro DATE NOT NULL DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB;

CREATE TABLE emprestimo (
  emprestimoId INT AUTO_INCREMENT PRIMARY KEY,
  tomadorId INT NOT NULL,
  criadoEm DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  previstoDevolucao DATETIME NULL,
  CONSTRAINT fk_emp_tomador FOREIGN KEY (tomadorId) REFERENCES tomador(tomadorId)
) ENGINE=InnoDB;

CREATE TABLE emprestimolivro (
  itemId INT AUTO_INCREMENT PRIMARY KEY,
  emprestimoId INT NOT NULL,
  livroId INT NOT NULL,
  devolvidoEm DATETIME NULL,
  CONSTRAINT fk_item_emp FOREIGN KEY (emprestimoId) REFERENCES emprestimo(emprestimoId) ON DELETE CASCADE,
  CONSTRAINT fk_item_livro FOREIGN KEY (livroId) REFERENCES livro(livroId)
) ENGINE=InnoDB;

CREATE INDEX idx_livro_titulo ON livro (titulo);
CREATE INDEX idx_autor_nome ON autor (nome);
CREATE INDEX idx_tomador_nome ON tomador (nome);
CREATE INDEX idx_item_livro ON emprestimoLivro (livroId);
CREATE INDEX idx_item_devolvido ON emprestimoLivro (devolvidoEm);

DELIMITER $$

CREATE TRIGGER trg_item_insert_decrement
AFTER INSERT ON emprestimolivro
FOR EACH ROW
BEGIN
  UPDATE livro
    SET copiasDisponiveis = copiasDisponiveis - 1
  WHERE livroId = NEW.livroId;
END$$

CREATE TRIGGER trg_item_update_increment
AFTER UPDATE ON emprestimolivro
FOR EACH ROW
BEGIN
  IF OLD.devolvidoEm IS NULL AND NEW.devolvidoEm IS NOT NULL THEN
    UPDATE livro
      SET copiasDisponiveis = copiasDisponiveis + 1
    WHERE livroId = NEW.livroId;
  END IF;
END$$

DELIMITER ;

INSERT INTO autor (nome) VALUES
('J. K. Rowling'), ('J. R. R. Tolkien'), ('George R. R. Martin'),
('Machado de Assis'), ('Clarice Lispector'), ('Neil Gaiman'),
('Isaac Asimov'), ('Arthur C. Clarke'), ('Agatha Christie'),
('Haruki Murakami'), ('Gabriel García Márquez'), ('José Saramago');

INSERT INTO livro (titulo, isbn, anoPublicacao, totalCopias, copiasDisponiveis) VALUES
('Harry Potter e a Pedra Filosofal', '9780747532699', 1997, 5, 5),
('O Senhor dos Anéis: A Sociedade do Anel', '9780261102354', 1954, 3, 3),
('A Game of Thrones', '9780553103540', 1996, 4, 4),
('Dom Casmurro', '9788520935110', 1899, 2, 2),
('A Hora da Estrela', '9788520933253', 1977, 2, 2),
('American Gods', '9780380973651', 2001, 3, 3),
('Fundação', '9780553803716', 1951, 4, 4),
('2001: Uma Odisseia no Espaço', '9780451457998', 1968, 2, 2),
('Assassinato no Expresso do Oriente', '9780007119318', 1934, 3, 3),
('Kafka à Beira-Mar', '9780307277671', 2002, 2, 2),
('Cem Anos de Solidão', '9780060883287', 1967, 3, 3),
('Ensaio sobre a Cegueira', '9789721040061', 1995, 2, 2);

INSERT INTO tomador (nome, email) VALUES
('Ana Souza', 'ana@example.com'),
('Bruno Lima', 'bruno@example.com'),
('Carla Menezes', 'carla@example.com'),
('Manoel Júnior', 'manoeljr@example.com');

INSERT INTO biblioteca.livroautor (livroId,autorId) VALUES
	 (1,1),
	 (2,2),
	 (3,3),
	 (4,4),
	 (5,5),
	 (6,6),
	 (7,7),
	 (8,8),
	 (9,9),
	 (10,10),
	 (11,11),
	 (12,12);

DELIMITER $$

CREATE PROCEDURE registrarEmprestimo(
  IN p_tomadorId INT,
  IN p_previstoDias INT
)
BEGIN
  INSERT INTO emprestimo (tomadorId, previstoDevolucao)
  VALUES (p_tomadorId, DATE_ADD(NOW(), INTERVAL p_previstoDias DAY));
  SELECT LAST_INSERT_ID() AS novoEmprestimoId;
END$$

CREATE PROCEDURE adicionarLivroEmprestimo(
  IN p_emprestimoId INT,
  IN p_livroId INT
)
BEGIN
  DECLARE v_disp INT;
  SELECT copiasDisponiveis INTO v_disp FROM livro WHERE livroId = p_livroId FOR UPDATE;
  IF v_disp IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Livro inexistente.';
  END IF;
  IF v_disp <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sem cópias disponíveis para este livro.';
  END IF;
  INSERT INTO emprestimolivro (emprestimoId, livroId) VALUES (p_emprestimoId, p_livroId);
END$$

CREATE PROCEDURE devolverLivroEmprestimo(
  IN p_itemId INT
)
BEGIN
  UPDATE emprestimolivro
    SET devolvidoEm = NOW()
  WHERE itemId = p_itemId AND devolvidoEm IS NULL;
  IF ROW_COUNT() = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Item já devolvido ou inexistente.';
  END IF;
END$$

DELIMITER ;

SELECT livroId, titulo, isbn, anoPublicacao, copiasDisponiveis, totalCopias
FROM livro
WHERE copiasDisponiveis > 0
ORDER BY titulo;

SELECT l.livroId, l.titulo, l.isbn, l.anoPublicacao
FROM livro l
JOIN livroAutor la ON la.livroId = l.livroId
JOIN autor a ON a.autorId = la.autorId
WHERE a.nome LIKE '%Isaac Asimov%'
ORDER BY l.titulo;

-- Criar um empréstimo
CALL registrarEmprestimo(1, 7);
SET @empId = LAST_INSERT_ID();

-- Adicionar 2 livros ao empréstimo
set @livroId = (SELECT livroId FROM livro WHERE titulo='Fundação' LIMIT 1);
CALL adicionarLivroEmprestimo(@empId, @livroId);
set @livroId = (SELECT livroId FROM livro WHERE titulo='Dom Casmurro' LIMIT 1);
CALL adicionarLivroEmprestimo(@empId, @livroId);

-- Conferir disponibilidade após o empréstimo
SELECT titulo, copiasDisponiveis FROM livro WHERE titulo IN ('Fundação','Dom Casmurro');

-- Listar livros do empréstimo
SELECT ei.itemId, l.titulo, ei.devolvidoEm
FROM emprestimolivro ei
JOIN livro l ON l.livroId = ei.livroId
WHERE ei.emprestimoId = @empId;

-- Devolver um item
SET @itemId := (SELECT itemId FROM emprestimolivro WHERE emprestimoId=@empId LIMIT 1);
CALL devolverLivroEmprestimo(@itemId);

-- Verificar disponibilidade pós-devolução
SELECT titulo, copiasDisponiveis FROM livro WHERE titulo IN ('Fundação','Dom Casmurro');

-- Verificar data de devolução do item
SELECT * from emprestimolivro e 

DELIMITER ;

-- Insert de um id inexistente para verificação das chaves estrangeiras
-- insert into biblioteca.livroautor values (1, 22);


