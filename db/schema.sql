use Crime;
-- 新聞
create table News (
    id bigint identity NOT null, -- 流水號
    title nvarchar(2048) NOT NULL, -- 文章標題
	link varchar(512) NOT NULL, -- 文章連結
    content nvarchar(MAX) NOT NULL, -- 文章內容
    criminal bit NOT NULL DEFAULT ((0)), -- 是否為犯罪新聞
    people  nvarchar(2048), -- 犯罪關係人(多個逗號分開)
    manual bit NOT NULL DEFAULT ((0)), -- 是否人工標註
	postdate varchar(256) NOT NULL, -- 文章發布日期
	updatetime datetime2, -- 文章更新日期
    primary key (id)
);