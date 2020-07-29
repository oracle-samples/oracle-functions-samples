#
# oci-adb-client-runsql-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import cx_Oracle
import oci
import os
from zipfile import ZipFile
import string
import random
from timeit import default_timer as timer

from fdk import response


def get_dbwallet_from_bucket():
    signer = oci.auth.signers.get_resource_principals_signer()  # authentication based on instance principal
    object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    obj = object_storage_client.get_object(object_storage_client.get_namespace().data, dbwallet_bucket, dbwallet_object)
    with open(dbwalletzip_location, 'w+b') as f:
        for chunk in obj.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    with ZipFile(dbwalletzip_location, 'r') as zipObj:
        zipObj.extractall(dbwallet_dir)

def get_dbwallet_from_autonomousdb():
    signer = oci.auth.signers.get_resource_principals_signer()   # authentication based on instance principal
    atp_client = oci.database.DatabaseClient(config={}, signer=signer)
    atp_wallet_pwd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)) # random string
    # the wallet password is only used for creation of the Java jks files, which aren't used by cx_Oracle so the value is not important
    atp_wallet_details = oci.database.models.GenerateAutonomousDatabaseWalletDetails(password=atp_wallet_pwd)
    print(atp_wallet_details, flush=True)
    obj = atp_client.generate_autonomous_database_wallet(adb_ocid, atp_wallet_details)
    with open(dbwalletzip_location, 'w+b') as f:
        for chunk in obj.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    with ZipFile(dbwalletzip_location, 'r') as zipObj:
            zipObj.extractall(dbwallet_dir)

#
# Instantiation code: executed once when the function container is initialized
#
if os.getenv("DBUSER") != None:
    dbuser = os.getenv("DBUSER")
else:
    raise ValueError("ERROR: Missing configuration key DBUSER")
if os.getenv("DBPWD_CYPHER") != None:
    dbpwd_cypher = dbpwd = os.getenv("DBPWD_CYPHER") # The decryption of the db password using OCI KMS would have to be done, however it is not addressed here
else:
    raise ValueError("ERROR: Missing configuration key DBPWD_CYPHER")
if os.getenv("DBSVC") != None:
    dbsvc = os.getenv("DBSVC")
else:
    raise ValueError("ERROR: Missing configuration key DBSVC")
if os.getenv("DBWALLET_BUCKET") != None and os.getenv("DBWALLET_OBJECT") != None:
    dbwallet_bucket = os.getenv("DBWALLET_BUCKET")
    dbwallet_object = os.getenv("DBWALLET_OBJECT")
    wallet_from_bucket = True
    print("INFO: DB wallet has to be retrived from bucket ", dbwallet_bucket, flush=True)
elif os.getenv("ADB_OCID") != None:
    adb_ocid = os.getenv("ADB_OCID")
    wallet_from_adb = True
    print("INFO: DB wallet has to be generated from ADB ", adb_ocid, flush=True)
else:
    raise ValueError("ERROR: Missing configuration key DBWALLET_BUCKET with DBWALLET_OBJECT, or ADB_OCID")
# Download the DB Wallet
dbwalletzip_location = "/tmp/dbwallet.zip"
dbwallet_dir = os.getenv('TNS_ADMIN')
if wallet_from_bucket:
    start_wallet = timer()
    get_dbwallet_from_bucket()
    end_wallet = timer()
    print('INFO: DB wallet downloaded from bucket in {} sec'.format(end_wallet - start_wallet), flush=True)
elif wallet_from_adb:
    start_wallet = timer()
    get_dbwallet_from_autonomousdb()
    end_wallet = timer()
    print('INFO: DB wallet downloaded from Autonomous DB in {} sec'.format(end_wallet - start_wallet), flush=True)
print('INFO: DB wallet dir content =', os.listdir(dbwallet_dir), flush=True)
# Update SQLNET.ORA
with open(dbwallet_dir + '/sqlnet.ora') as orig_sqlnetora:
    newText=orig_sqlnetora.read().replace('DIRECTORY=\"?/network/admin\"', 'DIRECTORY=\"{}\"'.format(dbwallet_dir))
with open(dbwallet_dir + '/sqlnet.ora', "w") as new_sqlnetora:
    new_sqlnetora.write(newText)
# Create the DB Session Pool
start_pool = timer()
dbpool = cx_Oracle.SessionPool(dbuser, dbpwd, dbsvc, min=1, max=1, encoding="UTF-8", nencoding="UTF-8")
end_pool = timer()
print("INFO: DB pool created in {} sec".format(end_pool - start_pool), flush=True)

#
# Function Handler: executed every time the function is invoked
#
def handler(ctx, data: io.BytesIO = None):
    try:
        payload_bytes = data.getvalue()
        if payload_bytes==b'':
            raise KeyError('No keys in payload')
        payload = json.loads(payload_bytes)
        sql_statement = payload["sql_statement"]
    except Exception as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise

    start_acquire = timer()
    with dbpool.acquire() as dbconnection:
        end_acquire = timer()
        print("INFO: DB connection acquired in {} sec".format(end_acquire - start_acquire), flush=True)
        start_cursor = timer()
        with dbconnection.cursor() as dbcursor:
            end_cursor = timer()
            print("INFO: DB cursor created in {} sec".format(end_cursor - start_cursor), flush=True)
            start_query = timer()
            result = dbcursor.execute(sql_statement)
            dbcursor.rowfactory = lambda *args: dict(zip([d[0] for d in dbcursor.description], args))
            result = dbcursor.fetchall()
            end_query = timer()
            print(result, flush=True)
            print("INFO: DB query executed in {} sec".format(end_query - start_query), flush=True)

    return response.Response(
        ctx,
        response_data=json.dumps(
            {"sql_statement": "{}".format(sql_statement), "result": "{}".format(result)}),
        headers={"Content-Type": "application/json"}
    )