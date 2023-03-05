drop table if exists login;
drop table if exists person_role;
drop table if exists role;
drop table if exists person;

create table person (
    id integer not null
        constraint person_pk primary key,
    name text not null,
    email text not null
        constraint person_email_uk unique,
    password text not null,
    mobile text null,
    enabled integer not null,
    change_password integer not null,
    created_at text not null,
    updated_at text null,
    deleted_at text null
);

create table role (
    id integer not null
        constraint role_pk primary key,
    name text not null
        constraint role_name_uk unique,
    description text null,
    created_at text not null,
    updated_at text null
);

create table person_role (
    person_id integer not null
        constraint person_role_person_fk references person (id)
            on delete no action
            on update no action,
    role_id integer not null
        constraint person_role_role_fk references role (id)
            on delete no action
            on update no action,
    constraint person_role_pk primary key (person_id, role_id)
);

create table login (
    id integer not null
        constraint login_pk primary key,
    person_id integer not null
        constraint login_person_fk references person (id)
            on delete no action
            on update no action,
    action text not null,
    ip_address text null,
    user_agent text null,
    created_at text not null
);
