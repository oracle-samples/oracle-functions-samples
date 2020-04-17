#
# oci-kms-decrypt-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import base64
import oci
from oci.key_management.models import DecryptDataDetails

from fdk import response

def decrypt(key_ocid, cryptographic_endpoint, cipher):
    decryptedtext = ""
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        client = oci.key_management.KmsCryptoClient({}, cryptographic_endpoint, signer=signer)
        secret = client.decrypt(DecryptDataDetails(key_id=key_ocid, ciphertext=cipher)).data.plaintext
        decryptedtext = base64.b64decode(secret).decode("utf-8")
    except Exception as ex:
        print("ERROR: Decryption failed", ex, flush=True)
        raise
    return decryptedtext

def handler(ctx, data: io.BytesIO=None):
    
    key_ocid = cryptographic_endpoint = cipher = decryptedtext = ""
    try:
        # Retrieve key OCID and cryptographic endpoint
        cfg = ctx.Config()
        key_ocid = cfg["key_ocid"]
        cryptographic_endpoint = cfg["cryptographic_endpoint"]
    except Exception as ex:
        print('ERROR: Missing configuration key', ex, flush=True)
        raise
    try:
        # Retrieve Cipher text to decrypt
        payload_bytes = data.getvalue()
        if payload_bytes==b'':
            raise KeyError('No keys in payload')
        payload = json.loads(payload_bytes)
        cipher = payload["cipher"]
    except Exception as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise

    decryptedtext = decrypt(key_ocid, cryptographic_endpoint, cipher)

    return response.Response(
        ctx, 
        response_data=json.dumps(
            {"decrypted_text": decryptedtext}),
        headers={"Content-Type": "application/json"}
    )
