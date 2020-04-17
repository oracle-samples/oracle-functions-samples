/*
** ObjectStorageGetObject version 1.0.
**
** Copyright (c) 2020 Oracle, Inc.
** Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.fn;

import com.oracle.bmc.auth.ResourcePrincipalAuthenticationDetailsProvider;
import com.oracle.bmc.objectstorage.ObjectStorage;
import com.oracle.bmc.objectstorage.ObjectStorageClient;
import com.oracle.bmc.objectstorage.requests.GetObjectRequest;
import com.oracle.bmc.objectstorage.responses.GetObjectResponse;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

public class ObjectStorageGetObject {

    private ObjectStorage objStoreClient = null;
    final ResourcePrincipalAuthenticationDetailsProvider provider
            = ResourcePrincipalAuthenticationDetailsProvider.builder().build();

    public ObjectStorageGetObject() {

        try {
            //print env vars in Functions container
            System.err.println("OCI_RESOURCE_PRINCIPAL_VERSION " + System.getenv("OCI_RESOURCE_PRINCIPAL_VERSION"));
            System.err.println("OCI_RESOURCE_PRINCIPAL_REGION " + System.getenv("OCI_RESOURCE_PRINCIPAL_REGION"));
            System.err.println("OCI_RESOURCE_PRINCIPAL_RPST " + System.getenv("OCI_RESOURCE_PRINCIPAL_RPST"));
            System.err.println("OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM " + System.getenv("OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM"));

            objStoreClient = new ObjectStorageClient(provider);

        } catch (Throwable ex) {
            System.err.println("Failed to instantiate ObjectStorage client - " + ex.getMessage());
        }
    }

    public static class GetObjectInfo {

        private String bucketName;
        private String name;

        public String getBucketName() {
            return bucketName;
        }

        public void setBucketName(String bucketName) {
            this.bucketName = bucketName;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

    }

    public String handle(GetObjectInfo objectInfo) {

        String result = "FAILED";

        if (objStoreClient == null) {
            System.err.println("There was a problem creating the ObjectStorage Client object. Please check logs");
            return result;
        }
        try {

            String nameSpace = System.getenv().get("NAMESPACE");

            GetObjectRequest gor = GetObjectRequest.builder()
                    .namespaceName(nameSpace)
                    .bucketName(objectInfo.getBucketName())
                    .objectName(objectInfo.getName())
                    .build();
            System.err.println("Getting content for object " + objectInfo.getName() + " from bucket " + objectInfo.getBucketName());

            GetObjectResponse response = objStoreClient.getObject(gor);
            result = new BufferedReader(new InputStreamReader(response.getInputStream()))
                    .lines().collect(Collectors.joining("\n"));

            System.err.println("Finished reading content for object " + objectInfo.getName());

        } catch (Throwable e) {
            System.err.println("Error fetching object " + e.getMessage());
            result = "Error fetching object " + e.getMessage();
        }

        return result;
    }
}
