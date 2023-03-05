insert into person (name, email, password, enabled, change_password, created_at)
values
    (
     'Frodo Baggins',
     'frodo@theshire',
     'pbkdf2:sha512:260000$CEaxpBEBYeiOJf2R$177d50d301956c469f7c5f9cc054316391ce2cdf4edc4f663b26998fdf10787a97ab23268c7be86fce7258e92eaf65f9f9b4bcb996209286978d4068fa266f1b',
     1, 0,
     CURRENT_TIMESTAMP
    );

insert into role (name, description, created_at)
values ('SYSTEM_ADMIN', 'Has unrestricted access', CURRENT_TIMESTAMP);

insert into role (name, description, created_at)
values ('PERSON_ADMIN', 'Manages user accounts', CURRENT_TIMESTAMP);

insert into person_role (person_id, role_id) values (1, 1);
