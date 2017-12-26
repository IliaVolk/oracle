CREATE OR REPLACE TRIGGER meeting_delete
  INSTEAD OF DELETE ON "Meeting"
  FOR EACH ROW
  BEGIN
    UPDATE "Meeting" SET "deleted" = 1
      WHERE "id" = OLD."id";
  END;