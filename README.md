# tcc-capm
TCC - Uma análise estatística da bolsa de valores

"""
Script ciração do BD
create table acao (
	cod  varchar(10) primary key,
	nome varchar(50) not null
);

create table preco (
	id serial primary key,
	cod_acao varchar(10) not null,
	dia date not null,
	preco decimal(10,2) not null,
	foreign key (cod_acao) references acao (cod)
);
"""
