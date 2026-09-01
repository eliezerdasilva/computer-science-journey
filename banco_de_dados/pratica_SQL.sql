create databese if not exists crlv;
use crlv;

create table crlv.Carro(
id_carro integer PRIMARY KEY AUTO_INCREMENT,
modelo VARCHAR(100),
placa CHAR(7),
id_proprietario integer,
FOREIGN key (id_proprietario) REFERENCES Pessoa(id_pessoa) 
)
create table if not exists crlv.Pessoa(
id_pessoa integer Primary key AUTO_increment,
nome VARCHAR(100),
email VARCHAR(100)
)

INSERT INTO crlv.Pessoa (nome,email) VALUES
	 ('Maria','maria@gmail.com'),
	 ('Tiago','tiago@gmail.com'),
	 ('Paulo','paulo@gmail.com'),
	 ('Teresa','teresa@gmail.com');


INSERT INTO crlv.Carro (modelo,placa,id_proprietario) VALUES
	 ('Fox','ZAZ1234',1),
	 ('Ka','ABC4321',2),
	 ('Fusca','AAA1111',3),
	 ('Kombi','ZZZ9999',2),
	 ('Gol','GHG3344',NULL),
('Golf','ABA1212',3);

--- Qual é o comando SQL que retorna apenas as placas e modelos de carros que não possuem proprietário?
SELECT Carro.placa, Carro.modelo FROM Carro WHERE Carro.id_proprietario IS NULL;

--- Qual é o comando SQL que retorna apenas os nomes das pessoas que possuem Fusca ou Kombi?
SELECT Pessoa.nome from Pessoa inner join Carro on Carro.id_proprietario = Pessoa.id_pessoa WHERE Carro.modelo IN ('fusca', 'Kombi')
--- Qual é o comando SQL que retorna apenas os nomes das pessoas e os modelos de carros que cada pessoa possui? No seguinte formato:
SELECT Pessoa.nome, Carro.modelo from Pessoa inner join Carro on Carro.id_proprietario = Pessoa.id_pessoa;

-- Qual é o comando SQL que insere um carro que pertence a Paulo?
INSERT INTO Carro (modelo, placa, id_proprietario)
VALUES (
    'Camaro', 
    'ZQL5841', 
    (SELECT id_proprietario FROM Pessoa WHERE nome = 'Paulo')
);
-- Qual é o comando SQL que retorna os carros em ordem alfabética crescente de placa?
select placa from Carro 
order by placa;
--Qual é o comando SQL que retorna os carros que não possuem dono?
select * from Carro 
where id_proprietario is null;
--Qual é o comando SQL que retorna os carros de Tiago?
select * from Carro 
inner join Pessoa on Pessoa.id_pessoa=Carro.id_proprietario
where Pessoa.nome like ('Tiago')

-- Segunda atividade
CREATE TABLE receita.Pessoa (
id_pessoa INTEGER PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
telefone VARCHAR(100) NOT NULL
);

CREATE TABLE receita.Categoria (
id_categoria INTEGER PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100) UNIQUE NOT NULL,
descricao VARCHAR(100) NOT NULL
);

CREATE TABLE receita.Receita (
id_receita INTEGER PRIMARY KEY AUTO_INCREMENT,
titulo VARCHAR(100) NOT NULL,
descricao VARCHAR(100) NOT NULL,
modo_preparo VARCHAR(100) NOT NULL,
tempo_preparo INTEGER,
rendimento VARCHAR(100) NOT NULL,
autor INTEGER NOT NULL REFERENCES Pessoa (id_pessoa) ON DELETE CASCADE,
categoria INTEGER REFERENCES Categoria (id_categoria) ON DELETE SET NULL
);

CREATE TABLE receita.Ingrediente (
id_ingrediente INTEGER PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100) UNIQUE NOT NULL,
unidade_padrao VARCHAR(100) NOT NULL
);

CREATE TABLE receita.Comentario (
id_comentario INTEGER PRIMARY KEY AUTO_INCREMENT,
pessoa INTEGER NOT NULL REFERENCES Pessoa (id_pessoa) ON DELETE CASCADE,
receita INTEGER NOT NULL REFERENCES Receita (id_receita) ON DELETE CASCADE,
texto VARCHAR(100) NOT NULL,
data VARCHAR(100) NOT NULL,
nota INTEGER
);



CREATE TABLE receita.ItemIngrediente (
id_itemIngrediente INTEGER PRIMARY KEY AUTO_INCREMENT,
receita INTEGER NOT NULL REFERENCES Receita (id) ON DELETE CASCADE,
ingrediente INTEGER NOT NULL REFERENCES Ingrediente (id_ingrediente) ON DELETE CASCADE,
quantidade REAL NOT NULL,
unidade VARCHAR(100) NOT NULL
);

Use receita
INSERT INTO Categoria (nome,descricao) VALUES
	 ('Sobremesa','Doces e sobremesas'),
	 ('Pizza','Pizzas de diversos sabores'),
('Salgadinho','Salgadinhos para festas');


INSERT INTO Pessoa (nome,email,telefone) VALUES
	 ('João Silva','joao@email.com',''),
('Maria Souza','masouza@gmail.com','');


INSERT INTO Ingrediente (nome,unidade_padrao) VALUES
	 ('Leite','ml'),
	 ('Leite Condensado','lata'),
	 ('Calabresa','g'),
	 ('Cebola','unidade'),
	 ('Molho de Tomate','ml'),
	 ('Queijo Mussarela','g'),
	 ('Farinha de Trigo','g'),
	 ('Fermento Biológico','g'),
	 ('Água','ml'),
('Azeite','ml');


INSERT INTO Receita (titulo,descricao,modo_preparo,tempo_preparo,rendimento,autor,categoria) VALUES ('Pudim de Leite Condensado','Clássico pudim brasileiro','Bata tudo, asse em banho-maria por 1 hora.',60,'8 porções',1,1), ('Pizza de Calabresa','Pizza sabor calabresa com cebola','Prepare a massa, adicione molho, calabresa e cebola. Asse por 20 minutos.',90,'1 pizza grande',2,2), ('Coxinha de Frango','Coxinha crocante recheada com frango desfiado','Prepare a massa, recheie com frango, modele em forma de coxinha e frite.',120,'20 unidades',1,3);


INSERT INTO Comentario (pessoa,receita,texto,data,nota) VALUES
	 (1,1,'Ficou ótimo!','2025-10-07',5),
	 (2,1,'Muito fácil de fazer.','2025-10-08',4),
	 (2,2,'Deliciosa!','2025-10-09',5),
	 (1,2,'Use calabrasa não muito picante!','2025-10-10',3),
	 (1,3,'Perfeita para festas!','2025-10-11',5),
	 (2,3,'Sugiro usar menos óleo','2025-10-12',4);





INSERT INTO Ingrediente (nome,unidade_padrao) VALUES
	 ('Farinha de Rosca','g'),
	 ('Alho','dente'),
('Salsa','g');

INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (1,1,500.0,''),
	 (1,2,1.0,''),
	 (2,3,200.0,''),
	 (2,4,1.0,''),
	 (2,5,150.0,''),
	 (2,6,200.0,''),
	 (2,7,300.0,''),
	 (2,8,10.0,''),
	 (2,9,180.0,''),
	 (2,10,20.0,'');
INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (2,11,5.0,''),
	 (2,12,5.0,''),
	 (3,13,300.0,''),
	 (3,14,100.0,''),
	 (3,15,10.0,''),
	 (3,16,50.0,''),
	 (3,17,2.0,''),
	 (3,18,200.0,''),
	 (3,7,100.0,''),
	 (3,1,300.0,'');
INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (3,19,2.0,''),
	 (3,20,1000.0,''),
	 (3,21,150.0,''),
	 (3,4,1.0,''),
	 (3,22,2.0,''),
	 (3,23,10.0,''),
	 (3,10,20.0,''),
	 (3,11,5.0,''),
	 (3,12,5.0,''),
	 (3,8,10.0,'');

INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (3,9,200.0,''),
(3,6,100.0,'');


Use receita
INSERT INTO Categoria (nome,descricao) VALUES
	 ('Sobremesa','Doces e sobremesas'),
	 ('Pizza','Pizzas de diversos sabores'),
('Salgadinho','Salgadinhos para festas');


INSERT INTO Pessoa (nome,email,telefone) VALUES
	 ('João Silva','joao@email.com',''),
('Maria Souza','masouza@gmail.com','');


INSERT INTO Ingrediente (nome,unidade_padrao) VALUES
	 ('Leite','ml'),
	 ('Leite Condensado','lata'),
	 ('Calabresa','g'),
	 ('Cebola','unidade'),
	 ('Molho de Tomate','ml'),
	 ('Queijo Mussarela','g'),
	 ('Farinha de Trigo','g'),
	 ('Fermento Biológico','g'),
	 ('Água','ml'),
('Azeite','ml');


INSERT INTO Receita (titulo,descricao,modo_preparo,tempo_preparo,rendimento,autor,categoria) VALUES ('Pudim de Leite Condensado','Clássico pudim brasileiro','Bata tudo, asse em banho-maria por 1 hora.',60,'8 porções',1,1), ('Pizza de Calabresa','Pizza sabor calabresa com cebola','Prepare a massa, adicione molho, calabresa e cebola. Asse por 20 minutos.',90,'1 pizza grande',2,2), ('Coxinha de Frango','Coxinha crocante recheada com frango desfiado','Prepare a massa, recheie com frango, modele em forma de coxinha e frite.',120,'20 unidades',1,3);


INSERT INTO Comentario (pessoa,receita,texto,data,nota) VALUES
	 (1,1,'Ficou ótimo!','2025-10-07',5),
	 (2,1,'Muito fácil de fazer.','2025-10-08',4),
	 (2,2,'Deliciosa!','2025-10-09',5),
	 (1,2,'Use calabrasa não muito picante!','2025-10-10',3),
	 (1,3,'Perfeita para festas!','2025-10-11',5),
	 (2,3,'Sugiro usar menos óleo','2025-10-12',4);





INSERT INTO Ingrediente (nome,unidade_padrao) VALUES
	 ('Farinha de Rosca','g'),
	 ('Alho','dente'),
('Salsa','g');

INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (1,1,500.0,''),
	 (1,2,1.0,''),
	 (2,3,200.0,''),
	 (2,4,1.0,''),
	 (2,5,150.0,''),
	 (2,6,200.0,''),
	 (2,7,300.0,''),
	 (2,8,10.0,''),
	 (2,9,180.0,''),
	 (2,10,20.0,'');
INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (2,11,5.0,''),
	 (2,12,5.0,''),
	 (3,13,300.0,''),
	 (3,14,100.0,''),
	 (3,15,10.0,''),
	 (3,16,50.0,''),
	 (3,17,2.0,''),
	 (3,18,200.0,''),
	 (3,7,100.0,''),
	 (3,1,300.0,'');
INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (3,19,2.0,''),
	 (3,20,1000.0,''),
	 (3,21,150.0,''),
	 (3,4,1.0,''),
	 (3,22,2.0,''),
	 (3,23,10.0,''),
	 (3,10,20.0,''),
	 (3,11,5.0,''),
	 (3,12,5.0,''),
	 (3,8,10.0,'');

INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (3,9,200.0,''),
(3,6,100.0,'');



Use receita
INSERT INTO Categoria (nome,descricao) VALUES
	 ('Sobremesa','Doces e sobremesas'),
	 ('Pizza','Pizzas de diversos sabores'),
('Salgadinho','Salgadinhos para festas');


INSERT INTO Pessoa (nome,email,telefone) VALUES
	 ('João Silva','joao@email.com',''),
('Maria Souza','masouza@gmail.com','');


INSERT INTO Ingrediente (nome,unidade_padrao) VALUES
	 ('Leite','ml'),
	 ('Leite Condensado','lata'),
	 ('Calabresa','g'),
	 ('Cebola','unidade'),
	 ('Molho de Tomate','ml'),
	 ('Queijo Mussarela','g'),
	 ('Farinha de Trigo','g'),
	 ('Fermento Biológico','g'),
	 ('Água','ml'),
('Azeite','ml');


INSERT INTO Receita (titulo,descricao,modo_preparo,tempo_preparo,rendimento,autor,categoria) VALUES ('Pudim de Leite Condensado','Clássico pudim brasileiro','Bata tudo, asse em banho-maria por 1 hora.',60,'8 porções',1,1), ('Pizza de Calabresa','Pizza sabor calabresa com cebola','Prepare a massa, adicione molho, calabresa e cebola. Asse por 20 minutos.',90,'1 pizza grande',2,2), ('Coxinha de Frango','Coxinha crocante recheada com frango desfiado','Prepare a massa, recheie com frango, modele em forma de coxinha e frite.',120,'20 unidades',1,3);


INSERT INTO Comentario (pessoa,receita,texto,data,nota) VALUES
	 (1,1,'Ficou ótimo!','2025-10-07',5),
	 (2,1,'Muito fácil de fazer.','2025-10-08',4),
	 (2,2,'Deliciosa!','2025-10-09',5),
	 (1,2,'Use calabrasa não muito picante!','2025-10-10',3),
	 (1,3,'Perfeita para festas!','2025-10-11',5),
	 (2,3,'Sugiro usar menos óleo','2025-10-12',4);





INSERT INTO Ingrediente (nome,unidade_padrao) VALUES
	 ('Farinha de Rosca','g'),
	 ('Alho','dente'),
('Salsa','g');

INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (1,1,500.0,''),
	 (1,2,1.0,''),
	 (2,3,200.0,''),
	 (2,4,1.0,''),
	 (2,5,150.0,''),
	 (2,6,200.0,''),
	 (2,7,300.0,''),
	 (2,8,10.0,''),
	 (2,9,180.0,''),
	 (2,10,20.0,'');
INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (2,11,5.0,''),
	 (2,12,5.0,''),
	 (3,13,300.0,''),
	 (3,14,100.0,''),
	 (3,15,10.0,''),
	 (3,16,50.0,''),
	 (3,17,2.0,''),
	 (3,18,200.0,''),
	 (3,7,100.0,''),
	 (3,1,300.0,'');
INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (3,19,2.0,''),
	 (3,20,1000.0,''),
	 (3,21,150.0,''),
	 (3,4,1.0,''),
	 (3,22,2.0,''),
	 (3,23,10.0,''),
	 (3,10,20.0,''),
	 (3,11,5.0,''),
	 (3,12,5.0,''),
	 (3,8,10.0,'');

INSERT INTO ItemIngrediente (receita,ingrediente,quantidade,unidade) VALUES
	 (3,9,200.0,''),
(3,6,100.0,'');


-- Em quantas receitas cada ingrediente foi usado?
Select Ingrediente.nome, count(ItemIngrediente.receita) AS total_receitas from Ingrediente
LEFT JOIN ItemIngrediente on ItemIngrediente.ingrediente = Ingrediente.id_ingrediente
GROUP by Ingrediente.id_ingrediente
ORDER BY total_receitas DESC;

-- Qual é a nota média por receita?
SELEct Receita.titulo, AVG(Comentario.nota) from Receita
Inner join Comentario on Comentario.receita= Receita.id_receita
GROUP by titulo
-- Listar Receitas por ordem de tempo de preparo
SELEct Receita.titulo, tempo_preparo from Receita
order by tempo_preparo asc
-- Retornar receitas e quantidade de ingredientes em cada receita
SELEct Receita.titulo, count(ItemIngrediente.quantidade) as quantidade from Receita
inner join ItemIngrediente on ItemIngrediente.receita = Receita.id_receita
group by titulo
-- Listar “o quanto” de cada ingrediente é preciso para fazer cada receita
SELEct Receita.titulo, Ingrediente.nome, ItemIngrediente.quantidade from Receita
join ItemIngrediente on ItemIngrediente.receita = Receita.id_receita
join Ingrediente on Ingrediente.id_ingrediente = ItemIngrediente.ingrediente


-- Listar comentários e receitas
SELECT Comentario.texto as comentarios, Receita.titulo as receitas from Comentario
join Receita on Comentario.receita = Receita.id_receita

-- Quais são as receitas mais demoradas
SELEct Receita.titulo, tempo_preparo from Receita
order by tempo_preparo desc
-- Listar receitas nas quais um ingrediente está em maior quantidade do que na outra

-- Trazer os comentários das pessoas, usando junção natural
SELECT Pessoa.nome as Usuario,Comentario.texto as comentarios, Receita.titulo as receitas from Comentario
join Receita on Comentario.receita = Receita.id_receita
join Pessoa on Pessoa.id_pessoa= Comentario.pessoa












