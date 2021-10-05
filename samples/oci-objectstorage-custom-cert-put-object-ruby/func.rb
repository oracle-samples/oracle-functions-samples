#
# oci-objectstorage-onsr-put-object-ruby version 1.0.
#
# Copyright (c) 2021 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

require 'fdk'

# Certs location
$cert_file_path = '/etc/oci-pki/customer/customer-cert.pem'
# file to upload
$file_to_upload = "cert_test"
$file_to_upload_content = "This is test file for ONSR test"

def put_object(bucket)
  FDK.log(entry: "put_object: enter")
  require 'oci'
  principal_signer =  OCI::Auth::Signers.resource_principals_signer
  object_storage_client = OCI::ObjectStorage::ObjectStorageClient.new(signer: principal_signer)
  namespace = object_storage_client.get_namespace.data

  if(File.exist?($cert_file_path))
    object_storage_client.api_client.request_option_overrides = {
      ca_file: $cert_file_path
    }
  end
  get_object_response = object_storage_client.put_object(namespace, bucket, $file_to_upload, $file_to_upload_content)
  FDK.log(entry: "put_object: exit")
end

def myfunction(context:, input:)
  bucket = input.respond_to?(:fetch) ? input.fetch('bucketName') : input
  put_object(bucket)
  { message: "Completed Successfully!!!" }
end

FDK.handle(target: :myfunction)
