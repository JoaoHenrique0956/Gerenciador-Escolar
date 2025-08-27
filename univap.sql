-- Criando o banco de dados
CREATE DATABASE univap;
USE univap;

-- Tabela de professores
CREATE TABLE professores (
    registro INT(11) PRIMARY KEY auto_increment,
    nomeprof VARCHAR(50),
    telefoneprof VARCHAR(30),
    idadeprof INT(11),
    salarioprof FLOAT
);


CREATE TABLE disciplinas (
    codigodisc INT(11) PRIMARY KEY,
    nomedisc VARCHAR(50)
);


CREATE TABLE disciplinasxprofessores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disciplinas_codigodisc INT NOT NULL,
    professores_registro INT NOT NULL,
    curso INT(11),
    cargahoraria INT(11),
    anoletivo INT(11),
    FOREIGN KEY (disciplinas_codigodisc) REFERENCES disciplinas(codigodisc),
    FOREIGN KEY (professores_registro) REFERENCES professores(registro)
);

