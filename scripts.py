#runs all the scripts
import sys

usage = "Usage:\npython scripts.py (option)\n\nOptions:\n  pull_new_users: "\
        + "pull new users from newrelic\n  configure_db: creates table,"\
        + "configures dbwith initial values"

if len(sys.argv) > 1:
    if sys.argv[1] == "pull_new_users":
        import scripts.pull_new_user
    elif sys.argv[1] == "configure_db":
        import scripts.db_init
    else:
        print usage
else:
    print usage
