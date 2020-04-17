/*
** ObjectStorageListObjects version 1.0.
**
** Copyright (c) 2020 Oracle, Inc.
** Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.fn;

import com.oracle.bmc.auth.ResourcePrincipalAuthenticationDetailsProvider;
import com.oracle.bmc.objectstorage.ObjectStorage;
import com.oracle.bmc.objectstorage.ObjectStorageClient;
import com.oracle.bmc.objectstorage.requests.ListObjectsRequest;
import com.oracle.bmc.objectstorage.responses.ListObjectsResponse;

import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class ObjectStorageListObjects {

    private ObjectStorage objStoreClient = null;

    final ResourcePrincipalAuthenticationDetailsProvider provider
            = ResourcePrincipalAuthenticationDetailsProvider.builder().build();

    public ObjectStorageListObjects() {
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

    public List<String> handleRequest(String bucketName) {

        if (objStoreClient == null) {
            System.err.println("There was a problem creating the ObjectStorage Client object. Please check logs");
            return Collections.emptyList();
        }

        List<String> objNames = null;
        try {
            String nameSpace = System.getenv().get("NAMESPACE");

            ListObjectsRequest lor = ListObjectsRequest.builder()
                    .namespaceName(nameSpace)
                    .bucketName(bucketName)
                    .build();

            System.err.println("Listing objects from bucket " + bucketName);

            ListObjectsResponse response = objStoreClient.listObjects(lor);

            objNames = response.getListObjects().getObjects().stream()
                    .map((objSummary) -> objSummary.getName())
                    .collect(Collectors.toList());

            System.err.println("Got " + objNames.size() + " objects in bucket " + bucketName);

        } catch (Throwable e) {
            System.err.println("Error fetching object list from bucket " + e.getMessage());
        }

        return objNames;
    }
}
