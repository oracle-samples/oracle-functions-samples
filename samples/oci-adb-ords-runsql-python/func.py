#
# oci-adb-ords-runsql-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import requests

from fdk import response

def ords_run_sql(ordsbaseurl, dbschema, dbpwd, sql):
    dbsqlurl = ordsbaseurl + dbschema + '/_/sql'
    headers = {"Content-Type": "application/sql"}
    auth=(dbschema, dbpwd)
    r = requests.post(dbsqlurl, auth=auth, headers=headers, data=sql)
    result = {}
    try:
        r_json = json.loads(r.text)
        for item in r_json["items"]:
            result["sql_statement"] = item["statementText"]
            if "errorDetails" in item:
                result["error"] = item["errorDetails"]
            elif "resultSet" in item:
                result["results"] = item["resultSet"]["items"]
            else:
                raise ValueError("No Error nor results found.")
    except ValueError:
        print(r.text, flush=True)
        raise
    return result

def handler(ctx, data: io.BytesIO=None):
    ordsbaseurl = dbuser = dbpwdcypher = dbpwd = sql = ""
    try:
        cfg = ctx.Config()
        ordsbaseurl = cfg["ords-base-url"]
        dbschema = cfg["db-schema"]
        dbpwdcypher = cfg["db-pwd-cypher"]
        dbpwd = dbpwdcypher  # The decryption of the db password using OCI KMS would have to be done, however it is addressed here
    except Exception:
        print('Missing function parameters: ords-base-url, db-user and db-pwd', flush=True)
        raise
    try:
        body = json.loads(data.getvalue())
        sql = body["sql"]
    except Exception:
        print('The data to pass to this function is a JSON object with the format: \'{"sql": "<SQL statement>"}\' ', flush=True)
        raise
    result = ords_run_sql(ordsbaseurl, dbschema, dbpwd, sql)

    return response.Response(
        ctx, 
        response_data=json.dumps(result),
        headers={"Content-Type": "application/json"}
    )
