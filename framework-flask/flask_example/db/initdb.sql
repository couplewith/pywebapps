drop table if exits user;
create table user(
   usre_id integer primary key autoincrement,
   user_name string not null,
   email  string not null,
   pw_hash string not null
);

drop table if exits follower;
create table follower(
   who_id integer,
   whom_from integer
);


drop table if exits message;
create table message(
   message_id integer primary key autoincrement,
   autor_id integer now null,
   text string not null,
   pub_date integer
);
