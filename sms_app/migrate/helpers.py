import logging

from django.db import connections

logger = logging.getLogger(__name__)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def selectRows(table_name, params, connection, debug=False):
    with connections[connection].cursor() as cursor:
        cursor.execute(
            "SELECT * FROM {} WHERE {}".format(
                table_name, " AND ".join(["{}=%s"]*len(params)).format(*params.keys())
            ),
            params.values()
        )
        return dictfetchall(cursor)
        
def insertOrUpdateRow(Object, table_name, fields, unique_keys, connection, debug=False):
    with connections[connection].cursor() as cursor:
        fields_for_update = fields.copy()
        for f in unique_keys:
            fields_for_update.remove(f)

        values_for_update = []
        for f in fields:
            values_for_update.append(Object[f])
        for f in fields_for_update:
            values_for_update.append(Object[f])

        sql = "INSERT INTO {} \n".format(table_name) + \
            "({}) VALUES \n".format(",".join(["`{}`".format(f) for f in fields])) + \
            "({}) \n".format(", ".join(["%s"]*len(fields))) + \
            "ON DUPLICATE KEY UPDATE \n" + \
            (",".join(["`{}`=%s"]*len(fields_for_update))).format(*fields_for_update)

        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: values={}".format(connection, values_for_update))

        cursor.execute(sql, values_for_update)

        cursor.execute(
            "SELECT id FROM {} WHERE {}".format(
                table_name, " AND ".join(["{}=%s"]*len(unique_keys)).format(*unique_keys)
            ),
            [Object[f] for f in unique_keys]
        )
        return cursor.fetchone()[0]

