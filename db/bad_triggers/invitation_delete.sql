CREATE OR REPLACE TRIGGER invitation_delete
 INSTEAD OF DELETE ON "Invitation"
  FOR EACH ROW
  BEGIN
    UPDATE "Invitation" SET "deleted" = 1
    WHERE "id" = OLD."id" AND "email" = OLD."email";
  END;