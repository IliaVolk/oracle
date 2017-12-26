CREATE OR REPLACE TRIGGER invitation_update
  BEFORE UPDATE ON "Invitation"
  FOR EACH ROW
declare
  ex_custom EXCEPTION;
  PRAGMA EXCEPTION_INIT( ex_custom, -20001 );
BEGIN
  IF :NEW."id" <> :OLD."id" OR
     :NEW."email" <> :OLD."email" THEN
    RAISE_APPLICATION_ERROR(-20001, 'ACCESS DENIED');
  END IF;
END;
