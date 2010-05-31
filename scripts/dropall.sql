BEGIN;
DROP TABLE "alerts_lamsonstate" CASCADE;
DROP TABLE "alerts_alert" CASCADE;
DROP TABLE "clients_client" CASCADE;
DROP TABLE "account_account" CASCADE;
DROP TABLE "blurb_blurb" CASCADE;
DROP TABLE "testing_confirmation" CASCADE;

COMMIT;