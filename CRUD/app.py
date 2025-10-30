import os
from typing import Optional, Tuple, List
from prettytable import PrettyTable
from db import Database

def table_print(headers: List[str], rows: List[Tuple]):
    t = PrettyTable()
    t.field_names = headers
    for r in rows:
        t.add_row(r)
    print(t)

def pause():
    input("\nPressione ENTER para continuar...")

# ########## CRUD: AUTORES ##########

def autores_listar(db: Database):
    rows = db.query("SELECT id, nome, nacionalidade FROM autores ORDER BY id")
    table_print(["ID", "Nome", "Nacionalidade"], rows)

def autores_inserir(db: Database):
    nome = input("Nome do autor: ").strip()
    nacionalidade = input("Nacionalidade (opcional): ").strip() or None
    with db.transaction():
        db.execute("INSERT INTO autores (nome, nacionalidade) VALUES (%s, %s)", (nome, nacionalidade))
    print("Autor inserido com sucesso.")

def autores_atualizar(db: Database):
    id_ = int(input("ID do autor a atualizar: "))
    nome = input("Novo nome: ").strip()
    nacionalidade = input("Nova nacionalidade (opcional): ").strip() or None
    with db.transaction():
        n = db.execute("UPDATE autores SET nome=%s, nacionalidade=%s WHERE id=%s", (nome, nacionalidade, id_))
    print(f"{n} registro(s) atualizado(s).")

def autores_excluir(db: Database):
    id_ = int(input("ID do autor a excluir: "))
    with db.transaction():
        n = db.execute("DELETE FROM autores WHERE id=%s", (id_,))
    print(f"{n} registro(s) excluído(s).")

# ########## CRUD: LIVROS ##########

def livros_listar(db: Database):
    sql = """
    SELECT l.id, l.titulo, l.ano_publicacao, l.isbn,
           GROUP_CONCAT(a.nome ORDER BY a.nome SEPARATOR ', ') AS autores
      FROM livros l
 LEFT JOIN livros_autores la ON la.livro_id = l.id
 LEFT JOIN autores a ON a.id = la.autor_id
  GROUP BY l.id, l.titulo, l.ano_publicacao, l.isbn
  ORDER BY l.id
    """
    rows = db.query(sql)
    table_print(["ID", "Título", "Ano", "ISBN", "Autor(es)"], rows)

def livros_inserir(db: Database):
    titulo = input("Título: ").strip()
    ano = input("Ano de publicação (opcional): ").strip()
    ano_int = int(ano) if ano else None
    isbn = input("ISBN (opcional): ").strip() or None

    print("Informe IDs de autores separados por vírgula (deixe vazio para nenhum):")
    autores_ids_str = input("Autor IDs: ").strip()
    autor_ids = []
    if autores_ids_str:
        autor_ids = [int(x) for x in autores_ids_str.split(",") if x.strip().isdigit()]

    with db.transaction():
        db.execute("INSERT INTO livros (titulo, ano_publicacao, isbn) VALUES (%s, %s, %s)",
                   (titulo, ano_int, isbn))
        livro_id = db.lastrowid()
        if autor_ids:
            values = [(livro_id, a_id) for a_id in autor_ids]
            db.executemany("INSERT INTO livros_autores (livro_id, autor_id) VALUES (%s, %s)", values)

    print("Livro inserido com sucesso.")

def livros_atualizar(db: Database):
    id_ = int(input("ID do livro a atualizar: "))
    titulo = input("Novo título: ").strip()
    ano = input("Novo ano (opcional): ").strip()
    ano_int = int(ano) if ano else None
    isbn = input("Novo ISBN (opcional): ").strip() or None

    with db.transaction():
        n = db.execute("UPDATE livros SET titulo=%s, ano_publicacao=%s, isbn=%s WHERE id=%s",
                       (titulo, ano_int, isbn, id_))
    print(f"{n} registro(s) atualizado(s).")

def livros_excluir(db: Database):
    id_ = int(input("ID do livro a excluir: "))
    with db.transaction():
        n = db.execute("DELETE FROM livros WHERE id=%s", (id_,))
    print(f"{n} registro(s) excluído(s).")

# ########## Menus ##########

def menu_autores(db: Database):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("==== AUTORES ====")
        print("1) Listar")
        print("2) Inserir")
        print("3) Atualizar")
        print("4) Excluir")
        print("0) Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            autores_listar(db); pause()
        elif op == "2":
            autores_inserir(db); pause()
        elif op == "3":
            autores_atualizar(db); pause()
        elif op == "4":
            autores_excluir(db); pause()
        elif op == "0":
            break

def menu_livros(db: Database):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("==== LIVROS ====")
        print("1) Listar")
        print("2) Inserir")
        print("3) Atualizar")
        print("4) Excluir")
        print("0) Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            livros_listar(db); pause()
        elif op == "2":
            livros_inserir(db); pause()
        elif op == "3":
            livros_atualizar(db); pause()
        elif op == "4":
            livros_excluir(db); pause()
        elif op == "0":
            break

def main():
    db = Database()
    try:
        db.connect()
    except Exception as e:
        print("Falha ao conectar no MySQL. Verifique .env e se o schema existe (rode schema.sql).")
        print("Erro:", e)
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("==== Biblioteca CRUD (MySQL + Python) ====")
        print("1) Autores")
        print("2) Livros")
        print("9) Rodar teste rápido (CRUD completo)")
        print("0) Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            menu_autores(db)
        elif op == "2":
            menu_livros(db)
        elif op == "9":
            quick_test(db); pause()
        elif op == "0":
            break

    db.disconnect()

# ########## Teste & Validação ##########

def quick_test(db: Database):
    print("Iniciando teste CRUD de autores...")
    with db.transaction():
        db.execute("INSERT INTO autores (nome, nacionalidade) VALUES (%s,%s)", ("Autor Teste", "BR"))
    novo_id = db.lastrowid()
    rows = db.query("SELECT id, nome FROM autores WHERE id=%s", (novo_id,))
    table_print(["ID","Nome"], rows)

    with db.transaction():
        db.execute("UPDATE autores SET nome=%s WHERE id=%s", ("Autor Teste Atualizado", novo_id))
    rows = db.query("SELECT id, nome FROM autores WHERE id=%s", (novo_id,))
    table_print(["ID","Nome"], rows)

    with db.transaction():
        db.execute("DELETE FROM autores WHERE id=%s", (novo_id,))
    rows = db.query("SELECT id, nome FROM autores WHERE id=%s", (novo_id,))
    print("Após delete, resultado deve ser vazio:")
    table_print(["ID","Nome"], rows)

if __name__ == "__main__":
    main()
