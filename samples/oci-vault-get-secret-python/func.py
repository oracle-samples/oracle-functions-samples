#
# oci-vault-get-secret-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import base64
import oci
import logging
import hashlib

from fdk import response

def get_text_secret(secret_ocid):
    #decrypted_secret_content = ""
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        client = oci.secrets.SecretsClient({}, signer=signer)
        secret_content = client.get_secret_bundle(secret_ocid).data.secret_bundle_content.content.encode('utf-8')
        decrypted_secret_content = base64.b64decode(secret_content).decode("utf-8")
    except Exception as ex:
        print("ERROR: failed to retrieve the secret content", ex, flush=True)
        raise
    return {"secret content": decrypted_secret_content}


def get_binary_secret_into_file(secret_ocid, filepath):
    #decrypted_secret_content = ""
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        client = oci.secrets.SecretsClient({}, signer=signer)
        secret_content = client.get_secret_bundle(secret_ocid).data.secret_bundle_content.content.encode('utf-8')
    except Exception as ex:
        print("ERROR: failed to retrieve the secret content", ex, flush=True)
        raise
    try:
        with open(filepath, 'wb') as secretfile:
            decrypted_secret_content = base64.decodebytes(secret_content)
            secretfile.write(decrypted_secret_content)
    except Exception as ex:
        print("ERROR: cannot write to file " + filepath, ex, flush=True)
        raise
    secret_md5 = hashlib.md5(decrypted_secret_content).hexdigest()
    return {"secret md5": secret_md5}


def handler(ctx, data: io.BytesIO=None):
    logging.getLogger().info("function start")

    secret_ocid = secret_type = resp = ""
    try:
        cfg = dict(ctx.Config())
        secret_ocid = cfg["secret_ocid"]
        logging.getLogger().info("Secret ocid = " + secret_ocid)
        secret_type = cfg["secret_type"]
        logging.getLogger().info("Secret type = " + secret_type)
    except Exception as e:
        print('ERROR: Missing configuration keys, secret ocid and secret_type', e, flush=True)
        raise

    if secret_type == "text":
        resp = get_text_secret(secret_ocid)
    elif secret_type == "binary":
        resp = get_binary_secret_into_file(secret_ocid, "/tmp/secret")
    else:
        raise ValueError('the value of the configuration parameter "secret_type" has to be either "text" or "binary"')

    logging.getLogger().info("function end")
    return response.Response(
        ctx, 
        response_data=resp,
        headers={"Content-Type": "application/json"}
    )
