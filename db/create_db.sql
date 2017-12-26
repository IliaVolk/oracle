create table "Invitation"
(
   "id"                 NUMBER,
   "email"              VARCHAR2(320),
   "status"             VARCHAR2(7) NOT NULL,
   constraint PK_INVITATION primary key ("id", "email")
);


create index "Confirmation of participation_" on "Invitation" (
   "id" ASC
);

create table "Meeting"
(
   "title"              VARCHAR2(256)            not null,
   "address"            VARCHAR2(256)            not null,
   "date"               TIMESTAMP                not null,
   "id"                 NUMBER                   NOT NULL ,
   "email"              VARCHAR2(320)            not null,
   "description"        VARCHAR2(256)            NULL,
   constraint PK_MEETING primary key ("id")
);

CREATE SEQUENCE meeting_seq START WITH 1;

create table "User"
(
   "email"              VARCHAR2(320)            not null,
   "name"               VARCHAR2(32),
   constraint PK_USER primary key ("email")
);

alter table "Invitation"
   add constraint FK_INVITATI_CONFIRMAT_MEETING foreign key ("id")
      references "Meeting" ("id");

alter table "Invitation"
   add constraint FK_INVITATI_NOTIFICAT_USER foreign key ("email")
      references "User" ("email");

alter table "Invitation"
   add constraint status_check
   check ("status" in ('accept', 'pending'));

alter table "Meeting"
   add constraint FK_MEETING_OWNERSHIP_USER foreign key ("email")
      references "User" ("email");

alter table "Meeting"
   add constraint MEETING_UNIQUENESS UNIQUE ("email", "title", "address", "date");


alter table "Meeting"
   add constraint check_title
   check ( LENGTHB("title") > 2);

ALTER TABLE "Meeting"
   ADD CONSTRAINT check_description
   CHECK ( LENGTHB("description") > 2);

alter table "Meeting"
   add constraint check_address
   check ( LENGTHB("address") > 2);

ALTER TABLE "User"
   ADD CONSTRAINT check_email
   CHECK ( REGEXP_LIKE ("email", '[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,4}'));

ALTER TABLE "User"
   ADD CONSTRAINT check_name
   CHECK (LENGTHB("name") > 2);

