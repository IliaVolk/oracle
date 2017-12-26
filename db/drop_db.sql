alter table "Invitation"
   drop constraint FK_INVITATI_CONFIRMAT_MEETING;

alter table "Invitation"
   drop constraint FK_INVITATI_NOTIFICAT_USER;

alter table "Meeting"
   drop constraint FK_MEETING_OWNERSHIP_USER;

drop index "Confirmation of participation_";

drop table "Invitation" cascade constraints;


drop table "Meeting" cascade constraints;

drop table "User" cascade constraints;

DROP SEQUENCE meeting_seq;