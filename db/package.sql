CREATE OR REPLACE PACKAGE ilya_package AS
   TYPE STRING_LIST IS TABLE OF "User"."email"%TYPE INDEX BY PLS_INTEGER;
   TYPE T_EMAIL IS TABLE OF "User"."email"%TYPE;
   TYPE USER_TABLE_RECORD IS RECORD (
      email "User"."email"%TYPE,
      name "User"."name"%TYPE
   );
   TYPE USER_TABLE IS TABLE OF USER_TABLE_RECORD;
   TYPE EMAIL_RECORD IS RECORD (
      email "User"."email"%TYPE
   );
   TYPE EMAIL_TABLE IS TABLE OF EMAIL_RECORD;
   TYPE MEETING_TABLE_RECORD IS RECORD (
      id "Meeting"."id"%TYPE,
      email "Meeting"."email"%TYPE,
      title "Meeting"."title"%TYPE,
      address "Meeting"."address"%TYPE,
      a_date "Meeting"."date"%TYPE,
      description "Meeting"."description"%TYPE,
      invited_name "User"."name"%TYPE,
      invited_email "User"."email"%TYPE,
      invited_status "Invitation"."status"%TYPE
   );
   TYPE MEETING_TABLE IS TABLE OF MEETING_TABLE_RECORD;
   TYPE INVITATION_TABLE_RECORD IS RECORD  (
      id "Meeting"."id"%TYPE,
      title "Meeting"."title"%TYPE,
      address "Meeting"."address"%TYPE,
      a_date "Meeting"."date"%TYPE,
      email "Invitation"."email"%TYPE,
      name "User"."name"%TYPE
   );
   TYPE INVITATION_TABLE IS TABLE OF INVITATION_TABLE_RECORD;
   PROCEDURE create_meeting(-- rc
      title "Meeting"."title"%TYPE,
      address "Meeting"."address"%TYPE,
      a_date "Meeting"."date"%TYPE,
      email "Meeting"."email"%TYPE,
      invited STRING_LIST,
      description "Meeting"."description"%TYPE
   );
   FUNCTION autocomplete_emails(
      owner_email "User"."email"%TYPE
   ) RETURN EMAIL_TABLE PIPELINED;
   FUNCTION get_meetings_list(
      email "User"."email"%TYPE,
      id "Meeting"."id"%TYPE
   ) RETURN MEETING_TABLE PIPELINED;
   PROCEDURE update_meeting(--ser
      id "Meeting"."id"%TYPE,
      title "Meeting"."title"%TYPE,
      address "Meeting"."address"%TYPE,
      a_date "Meeting"."date"%TYPE,
      invited STRING_LIST,
      description "Meeting"."description"%TYPE
   );
   FUNCTION get_user(
      email "User"."email"%TYPE
   ) RETURN USER_TABLE PIPELINED;
   PROCEDURE create_user(--rc
      email "User"."email"%TYPE,
      username "User"."name"%TYPE
   );
   FUNCTION get_invitations(
      email "User"."email"%TYPE
   ) RETURN INVITATION_TABLE PIPELINED;
   PROCEDURE accept_invitation(--rc
      id "Invitation"."id"%TYPE,
      email "Invitation"."email"%TYPE
   );
   PROCEDURE discard_invitation(--rc
      id "Invitation"."id"%TYPE,
      email "Invitation"."email"%TYPE
   );
   PROCEDURE delete_meeting(
      id "Meeting"."id"%TYPE
   );
END ilya_package;
