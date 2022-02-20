DROP TABLE IF EXISTS kids;
DROP TABLE IF EXISTS parties;

CREATE TABLE kids (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first TEXT NOT NULL,
  last TEXT NOT NULL,
  age INTEGER NOT NULL
);

CREATE TABLE parties (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kid_list TEXT,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  description TEXT NOT NULL,
  invitation TEXT NOT NULL
);

CREATE TRIGGER before_delete_kids BEFORE DELETE ON kids
BEGIN
select case when 1=1 then RAISE(ABORT,'Deletions not allowed on kids table')
END;
END;

CREATE TRIGGER before_delete_parties BEFORE DELETE ON parties
BEGIN
select case when 1=1 then RAISE(ABORT,'Deletions not allowed on parties table')
END;
END;

