CREATE OR REPLACE TRIGGER invitation_insert
  BEFORE INSERT ON "Invitation"
  FOR EACH ROW
  DECLARE
  meeting_email "Meeting"."email"%TYPE;
  BEGIN
    SELECT "email" INTO meeting_email
      FROM "Meeting"
      WHERE "id" = :NEW."id";
    IF meeting_email = :NEW."email" THEN
      RAISE_APPLICATION_ERROR(-20001, 'Can not invite meeting owner');
    END IF;
  END;