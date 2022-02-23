PY=python3
CONFIG=migration_config.py
ENTRY_POINT=migrate.py

for line in $(cat configs/migrate_order);
do
	cp $line $CONFIG && echo ***Using config file $line;
	$PY $ENTRY_POINT && echo ***Migrated;
done
rm $CONFIG
