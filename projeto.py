from prettytable import PrettyTable
import mysql.connector

# ============================== CONEXÃO BANCO ==============================

def abrebanco():
    try:
        global conexao
        conexao = mysql.connector.connect(
            host='localhost',
            database='univap',
            user='root',
            password=''
        )
        if conexao.is_connected():
            print("Conexão realizada com sucesso!")
            global comandosql
            comandosql = conexao.cursor()
            return 1
        else:
            print("Falha na conexão com o banco.")
            return 0
    except Exception as erro:
        print(f"Erro: {erro}")
        return 0

# ============================== FUNÇÕES DISCIPLINAS ==============================

def mostrardisciplinas():
    grid = PrettyTable(["Código", "Nome"])
    comandosql.execute("SELECT * FROM disciplinas;")
    tabela = comandosql.fetchall()
    if tabela:
        for registro in tabela:
            grid.add_row([registro[0], registro[1]])
        print(grid)
    else:
        print("Nenhuma disciplina cadastrada!")

def cadastrardisciplina():
    try:
        try:
            cod = int(input("Código da disciplina: ").strip())
        except ValueError:
            print("Código deve ser numérico!")
            return

        nome = input("Nome da disciplina: ").strip()
        if nome == "":
            print("Nome não pode ser vazio!")
            return

        comandosql.execute("SELECT * FROM disciplinas WHERE codigodisc=%s;", (cod,))
        if comandosql.fetchone():
            print("Já existe uma disciplina com este código!")
            return

        comandosql.execute(
            "INSERT INTO disciplinas (codigodisc, nomedisc) VALUES (%s, %s);",
            (cod, nome)
        )
        conexao.commit()
        print("Disciplina cadastrada com sucesso!")
    except Exception as erro:
        print(f"Erro ao cadastrar disciplina: {erro}")

def alterardisciplina():
    mostrardisciplinas()
    try:
        cod = int(input("Informe o código da disciplina a alterar: ").strip())
    except ValueError:
        print("⚠ Código inválido!")
        return

    comandosql.execute("SELECT * FROM disciplinas WHERE codigodisc=%s;", (cod,))
    if not comandosql.fetchone():
        print("⚠ Disciplina não encontrada!")
        return

    nome = input("Novo nome da disciplina: ").strip()
    if nome == "":
        print("⚠ Nome não pode ser vazio!")
        return

    comandosql.execute(
        "UPDATE disciplinas SET nomedisc=%s WHERE codigodisc=%s;",
        (nome, cod)
    )
    conexao.commit()
    print("Disciplina alterada com sucesso!")

def excluirdisciplina():
    mostrardisciplinas()
    try:
        cod = int(input("Informe o código da disciplina a excluir: ").strip())
    except ValueError:
        print("⚠ Código inválido!")
        return

    comandosql.execute("SELECT * FROM disciplinas WHERE codigodisc=%s;", (cod,))
    if not comandosql.fetchone():
        print("⚠ Disciplina não encontrada!")
        return

    comandosql.execute("SELECT * FROM disciplinasxprofessores WHERE disciplinas_codigodisc=%s;", (cod,))
    if comandosql.fetchone():
        print("⚠ Não é possível excluir! Disciplina relacionada a algum professor.")
        return

    comandosql.execute("DELETE FROM disciplinas WHERE codigodisc=%s;", (cod,))
    conexao.commit()
    print("Disciplina excluída com sucesso!")

# ============================== FUNÇÕES PROFESSORES ==============================

def mostrartodosprofessores():
    grid = PrettyTable(["Registro", "Nome", "Telefone", "Idade", "Salário"])
    comandosql.execute("SELECT * FROM professores;")
    tabela = comandosql.fetchall()
    if tabela:
        for registro in tabela:
            grid.add_row([registro[0], registro[1], registro[2], registro[3], registro[4]])
        print(grid)
    else:
        print("Nenhum professor cadastrado!")

def cadastrarprofessor():
    try:
        nome = input("Nome do professor: ").strip()
        telefone = input("Telefone: ").strip()
        try:
            idade = int(input("Idade: ").strip())
        except ValueError:
            print("⚠ Idade deve ser numérica!")
            return
        try:
            salario = float(input("Salário: ").strip())
        except ValueError:
            print("⚠ Salário deve ser numérico!")
            return

        # verifica duplicidade no nome ou telefone
        comandosql.execute("SELECT * FROM professores WHERE nomeprof=%s OR telefoneprof=%s;", (nome, telefone))
        if comandosql.fetchone():
            print("⚠ Já existe um professor com este nome ou telefone!")
            return

        comandosql.execute(
            "INSERT INTO professores (nomeprof, telefoneprof, idadeprof, salarioprof) VALUES (%s, %s, %s, %s);",
            (nome, telefone, idade, salario)
        )
        conexao.commit()
        print("Professor cadastrado com sucesso!")
    except Exception as erro:
        print(f"Erro ao cadastrar professor: {erro}")

def alterarprofessor():
    mostrartodosprofessores()
    try:
        reg = int(input("Informe o registro do professor a alterar: ").strip())
    except ValueError:
        print("⚠ Registro inválido!")
        return

    comandosql.execute("SELECT * FROM professores WHERE registro=%s;", (reg,))
    prof = comandosql.fetchone()
    if not prof:
        print("⚠ Professor não encontrado!")
        return

    nome = input("Novo nome (enter para manter): ").strip()
    telefone = input("Novo telefone (enter para manter): ").strip()
    idade_str = input("Nova idade (enter para manter): ").strip()
    salario_str = input("Novo salário (enter para manter): ").strip()

    try:
        idade = int(idade_str) if idade_str else prof[3]
    except ValueError:
        idade = prof[3]
    try:
        salario = float(salario_str) if salario_str else prof[4]
    except ValueError:
        salario = prof[4]

    nome = nome if nome else prof[1]
    telefone = telefone if telefone else prof[2]

    # checa duplicidade de nome ou telefone (ignora o próprio professor)
    comandosql.execute(
        "SELECT * FROM professores WHERE (nomeprof=%s OR telefoneprof=%s) AND registro<>%s;",
        (nome, telefone, reg)
    )
    if comandosql.fetchone():
        print("⚠ Já existe outro professor com este nome ou telefone!")
        return

    comandosql.execute(
        "UPDATE professores SET nomeprof=%s, telefoneprof=%s, idadeprof=%s, salarioprof=%s WHERE registro=%s;",
        (nome, telefone, idade, salario, reg)
    )
    conexao.commit()
    print("Professor alterado com sucesso!")

def excluirprofessor():
    mostrartodosprofessores()
    try:
        reg = int(input("Informe o registro do professor a excluir: ").strip())
    except ValueError:
        print("⚠ Registro inválido!")
        return

    comandosql.execute("SELECT * FROM professores WHERE registro=%s;", (reg,))
    if not comandosql.fetchone():
        print("⚠ Professor não encontrado!")
        return

    comandosql.execute("SELECT * FROM disciplinasxprofessores WHERE professores_registro=%s;", (reg,))
    if comandosql.fetchone():
        print("⚠ Não é possível excluir! Professor está relacionado a alguma disciplina.")
        return

    comandosql.execute("DELETE FROM professores WHERE registro=%s;", (reg,))
    conexao.commit()
    print("Professor excluído com sucesso!")

# ============================== FUNÇÕES RELAÇÕES ==============================

def mostrarrelacoes():
    grid = PrettyTable(["ID", "Disciplina", "Professor", "Curso", "Carga Horária", "Ano Letivo"])
    comandosql.execute("""
        SELECT r.id, d.nomedisc, p.nomeprof, r.curso, r.cargahoraria, r.anoletivo
        FROM disciplinasxprofessores r
        JOIN disciplinas d ON r.disciplinas_codigodisc = d.codigodisc
        JOIN professores p ON r.professores_registro = p.registro;
    """)
    tabela = comandosql.fetchall()
    if tabela:
        for registro in tabela:
            grid.add_row(registro)
        print(grid)
    else:
        print("Nenhuma relação cadastrada!")

def cadastrarelacao():
    print("=== Disciplinas ===")
    mostrardisciplinas()
    try:
        cod_disc = int(input("Informe o código da disciplina: ").strip())
    except ValueError:
        print("⚠ Código inválido!")
        return

    comandosql.execute("SELECT * FROM disciplinas WHERE codigodisc=%s;", (cod_disc,))
    if not comandosql.fetchone():
        print("⚠ Disciplina não encontrada!")
        return

    print("=== Professores ===")
    mostrartodosprofessores()
    try:
        reg_prof = int(input("Informe o registro do professor: ").strip())
    except ValueError:
        print("⚠ Registro inválido!")
        return

    comandosql.execute("SELECT * FROM professores WHERE registro=%s;", (reg_prof,))
    if not comandosql.fetchone():
        print("⚠ Professor não encontrado!")
        return

    try:
        curso = int(input("Curso: ").strip())
        cargahoraria = int(input("Carga horária: ").strip())
        anoletivo = int(input("Ano letivo: ").strip())
    except ValueError:
        print("⚠ Curso, carga horária e ano letivo devem ser numéricos!")
        return

    comandosql.execute("""
        INSERT INTO disciplinasxprofessores 
        (disciplinas_codigodisc, professores_registro, curso, cargahoraria, anoletivo)
        VALUES (%s, %s, %s, %s, %s);
    """, (cod_disc, reg_prof, curso, cargahoraria, anoletivo))
    conexao.commit()
    print("Relação cadastrada com sucesso!")

def alterarelacao():
    mostrarrelacoes()
    try:
        id_rel = int(input("Informe o ID da relação a alterar: ").strip())
    except ValueError:
        print("⚠ ID inválido!")
        return

    comandosql.execute("SELECT * FROM disciplinasxprofessores WHERE id=%s;", (id_rel,))
    if not comandosql.fetchone():
        print("⚠ Relação não encontrada!")
        return

    print("=== Disciplinas ===")
    mostrardisciplinas()
    try:
        cod_disc = int(input("Novo código da disciplina: ").strip())
    except ValueError:
        print("⚠ Código inválido!")
        return

    comandosql.execute("SELECT * FROM disciplinas WHERE codigodisc=%s;", (cod_disc,))
    if not comandosql.fetchone():
        print("⚠ Disciplina não encontrada!")
        return

    print("=== Professores ===")
    mostrartodosprofessores()
    try:
        reg_prof = int(input("Novo registro do professor: ").strip())
    except ValueError:
        print("⚠ Registro inválido!")
        return

    comandosql.execute("SELECT * FROM professores WHERE registro=%s;", (reg_prof,))
    if not comandosql.fetchone():
        print("⚠ Professor não encontrado!")
        return

    try:
        curso = int(input("Curso: ").strip())
        cargahoraria = int(input("Carga horária: ").strip())
        anoletivo = int(input("Ano letivo: ").strip())
    except ValueError:
        print("⚠ Curso, carga horária e ano letivo devem ser numéricos!")
        return

    comandosql.execute("""
        UPDATE disciplinasxprofessores
        SET disciplinas_codigodisc=%s, professores_registro=%s, curso=%s, cargahoraria=%s, anoletivo=%s
        WHERE id=%s;
    """, (cod_disc, reg_prof, curso, cargahoraria, anoletivo, id_rel))
    conexao.commit()
    print("Relação alterada com sucesso!")

def excluirelacao():
    mostrarrelacoes()
    try:
        id_rel = int(input("Informe o ID da relação a excluir: ").strip())
    except ValueError:
        print("⚠ ID inválido!")
        return

    comandosql.execute("SELECT * FROM disciplinasxprofessores WHERE id=%s;", (id_rel,))
    if not comandosql.fetchone():
        print("⚠ Relação não encontrada!")
        return

    comandosql.execute("DELETE FROM disciplinasxprofessores WHERE id=%s;", (id_rel,))
    conexao.commit()
    print("Relação excluída com sucesso!")


# ============================== MENU PRINCIPAL ==============================

if abrebanco() == 1:
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Menu Disciplinas")
        print("2 - Menu Professores")
        print("3 - Menu Relações")
        print("0 - Sair")
        opc = input("Escolha: ")

        # ---------------- MENU DISCIPLINAS ----------------
        if opc == '1':
            while True:
                print("\n=== MENU DISCIPLINAS ===")
                print("1 - Mostrar disciplinas")
                print("2 - Cadastrar disciplina")
                print("3 - Alterar disciplina")
                print("4 - Excluir disciplina")
                print("0 - Voltar")
                sub = input("Escolha: ")
                if sub == '1':
                    mostrardisciplinas()
                elif sub == '2':
                    cadastrardisciplina()
                elif sub == '3':
                    alterardisciplina()
                elif sub == '4':
                    excluirdisciplina()
                elif sub == '0':
                    break
                else:
                    print("Opção inválida!")

        # ---------------- MENU PROFESSORES ----------------
        elif opc == '2':
            while True:
                print("\n=== MENU PROFESSORES ===")
                print("1 - Mostrar professores")
                print("2 - Cadastrar professor")
                print("3 - Alterar professor")
                print("4 - Excluir professor")
                print("0 - Voltar")
                sub = input("Escolha: ")
                if sub == '1':
                    mostrartodosprofessores()
                elif sub == '2':
                    cadastrarprofessor()
                elif sub == '3':
                    alterarprofessor()
                elif sub == '4':
                    excluirprofessor()
                elif sub == '0':
                    break
                else:
                    print("Opção inválida!")

        # ---------------- MENU RELAÇÕES ----------------
        elif opc == '3':
            while True:
                print("\n=== MENU RELAÇÕES ===")
                print("1 - Mostrar relações")
                print("2 - Cadastrar relação")
                print("3 - Alterar relação")
                print("4 - Excluir relação")
                print("0 - Voltar")
                sub = input("Escolha: ")
                if sub == '1':
                    mostrarrelacoes()
                elif sub == '2':
                    cadastrarelacao()
                elif sub == '3':
                    alterarelacao()
                elif sub == '4':
                    excluirelacao()
                elif sub == '0':
                    break
                else:
                    print("Opção inválida!")

        elif opc == '0':
            break
        else:
            print("Opção inválida!")

    comandosql.close()
    conexao.close()
    print("Programa encerrado.")
