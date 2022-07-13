import logging
import subprocess

from django.db import connections

logger = logging.getLogger(__name__)

APP_ENVS = [
    'staging',
    'campus'
]
DESTINATIONS = {
    'staging': [
        'university'
    ],
    'campus': [
        'sms',
        'zhaw',
        'ffhs',
        'unili',
        'ethz',
        'epfl',
        'unige',
        'tdr',
    ]
}

CONNECTION_SOURCE = 'edxapp_readonly'
CONNECTION_ID = 'edxapp_id'

def set_max_allowed_packet(connection):
    with connections[connection].cursor() as cursor:
        cursor.execute("SET max_allowed_packet=1073741824")

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def selectRows(table_name, params, connection, debug=False):
    with connections[connection].cursor() as cursor:
        sql = "SELECT * FROM {} WHERE {}".format(
            table_name, " AND ".join(["{}=%s"]*len(params)).format(*params.keys())
        )
        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: params={}".format(connection, params.values()))
        cursor.execute(sql, params.values())
        return dictfetchall(cursor)

def selectRowsIn(table_name, param, values, connection, debug=False):
    if not values: return []
    with connections[connection].cursor() as cursor:
        sql = "SELECT * FROM {} WHERE {} IN ({})".format(
            table_name, param, ", ".join(["%s"]*len(values))
        )
        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: params={}".format(connection, values))
        cursor.execute(sql, values)
        return dictfetchall(cursor)

def selectField(table_name, field, params, connection, debug=False):
    with connections[connection].cursor() as cursor:
        sql = "SELECT {} FROM {} WHERE {}".format(
            field, table_name, " AND ".join(["{}=%s"]*len(params)).format(*params.keys())
        )
        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: params={}".format(connection, params.values()))
        cursor.execute(sql, params.values())
        return set([row[field] for row in dictfetchall(cursor)])

def selectFieldIn(table_name, field, param, values, connection, debug=False):
    if not values: return []
    with connections[connection].cursor() as cursor:
        sql = "SELECT {} FROM {} WHERE {} IN ({})".format(
            field, table_name, param, ", ".join(["%s"]*len(values))
        )
        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: params={}".format(connection, values))
        cursor.execute(sql, values)
        return set([row[field] for row in dictfetchall(cursor)])

def tableStruct(table_name, connection):
    with connections[connection].cursor() as cursor:
        cursor.execute("DESCRIBE {}".format(table_name))
        return cursor.fetchall();

def copyTable(table_name, src, dst, debug=False):
    struct = tableStruct(table_name, src)
    # (('id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'), ('content_hash', 'varchar(40)', 'NO', 'UNI', None, ''), ('structure_hash', 'varchar(40)', 'NO', 'MUL', None, ''))
    fields = [f[0] for f in struct]
    for row in selectRows(table_name, {1:1}, src, debug):
        insertOrUpdateRow(row, table_name, fields, ['id'], dst, debug)

def insertOrUpdateRow(Object, table_name, fields, unique_keys, connection, debug=False):
    # do nothing id there isn't Object to copy
    if not Object: return

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

def cmd(cmd, debug=False):
    if debug:
        logger.info("RUN CMD={}".format(cmd))

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    return_code = process.returncode

    if debug:
        logger.info("CMD CODE={}, STDOUT={}, STDERR={}".format(return_code, stdout, stderr))

    return return_code, stdout, stderr

def deleteRows(table_name, params, connection, debug=False):
    with connections[connection].cursor() as cursor:
        sql = "DELETE FROM {} WHERE {}".format(
            table_name, " AND ".join(["{}=%s"]*len(params)).format(*params.keys())
        )
        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: params={}".format(connection, params.values()))
        cursor.execute(sql, params.values())

def deleteRowsIn(table_name, param, values, connection, debug=False):
    if not values: return []
    with connections[connection].cursor() as cursor:
        sql = "DELETE FROM {} WHERE {} IN ({})".format(
            table_name, param, ", ".join(["%s"]*len(values))
        )
        if debug:
            logger.info("{}: SQL={}".format(connection, sql))
            logger.info("{}: params={}".format(connection, values))
        cursor.execute(sql, values)
