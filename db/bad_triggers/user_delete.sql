CREATE OR REPLACE TRIGGER user_delete
  INSTEAD OF DELETE ON "User"
  FOR EACH ROW
  BEGIN
    UPDATE "User" SET "deleted" = 1
    WHERE "email" = OLD."email";
  END;