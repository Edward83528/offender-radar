
create table News (
    id bigint identity not null,
    title nvarchar(2048) NOT NULL,
	link varchar(512) NOT NULL,
    content nvarchar(MAX) NOT NULL,
	postdate varchar(256) NOT NULL,
	updatetime datetime2,
    primary key (id)
);