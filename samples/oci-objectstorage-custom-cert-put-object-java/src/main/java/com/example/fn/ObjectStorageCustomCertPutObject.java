/*
** ObjectStorageCustomCertPutObject version 1.0.
**
** Copyright (c) 2021 Oracle, Inc.
** Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.fn;

import com.oracle.bmc.auth.ResourcePrincipalAuthenticationDetailsProvider;
import com.oracle.bmc.objectstorage.ObjectStorage;
import com.oracle.bmc.objectstorage.ObjectStorageClient;
import com.oracle.bmc.objectstorage.requests.GetNamespaceRequest;
import com.oracle.bmc.objectstorage.requests.PutObjectRequest;
import com.oracle.bmc.objectstorage.responses.PutObjectResponse;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.io.File;

import java.security.KeyStore;
import java.security.cert.CertificateFactory;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.Key;
import java.io.IOException;
import java.io.InputStream;
import java.io.DataInputStream;
import java.security.cert.Certificate;
import java.util.Collection;
import org.apache.commons.lang3.RandomStringUtils;

public class ObjectStorageCustomCertPutObject {

    static String keyStorePassword = RandomStringUtils.randomAlphanumeric(10);
    private ObjectStorage objStoreClient = null;
    final ResourcePrincipalAuthenticationDetailsProvider provider
            = ResourcePrincipalAuthenticationDetailsProvider.builder().build();

    public ObjectStorageCustomCertPutObject() {
        try {
            //print env vars in Functions container
            System.err.println("OCI_RESOURCE_PRINCIPAL_VERSION " + System.getenv("OCI_RESOURCE_PRINCIPAL_VERSION"));
            System.err.println("OCI_RESOURCE_PRINCIPAL_REGION " + System.getenv("OCI_RESOURCE_PRINCIPAL_REGION"));
            System.err.println("OCI_RESOURCE_PRINCIPAL_RPST " + System.getenv("OCI_RESOURCE_PRINCIPAL_RPST"));
            System.err.println("OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM " + System.getenv("OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM"));

            // Adding certificates to trust store
            // Adding certificates to trust store
            String certificate_file_path = "/etc/oci-pki/customer/customer-cert.pem";
            String trust_store_path = "/tmp/keystore.jks";
            File cacertFile = new File(certificate_file_path);
            if (cacertFile.exists()) {
                createKeystoreWithCaBundle(certificate_file_path, trust_store_path);
                System.setProperty("javax.net.ssl.trustStore", trust_store_path);
            }
            objStoreClient = new ObjectStorageClient(provider);
        } catch (Throwable ex) {
            System.err.println("Failed to instantiate ObjectStorage client - " + ex.getMessage());
        }
    }

    private static void createKeystoreWithCaBundle(String caBundlePath, String trustStorePath) throws Exception {
        KeyStore ks = KeyStore.getInstance("JKS");
        ks.load(null, null);

        // Now load our cert and add it to the keystore
        CertificateFactory cf = CertificateFactory.getInstance("X.509");

        try (FileInputStream inputStream = new FileInputStream(caBundlePath)) {
            Collection<? extends Certificate> caCollection = cf.generateCertificates(inputStream);
            int i = 0;
            for (Certificate ca : caCollection) {
                ks.setCertificateEntry("Trusted Cert " + i++, ca);
            }

            FileOutputStream fos = new FileOutputStream(trustStorePath);
            ks.store(fos, keyStorePassword.toCharArray());
        }
    }

    public static class ObjectInfo {

        private String name;
        private String bucketName;
        private String content;

        public String getBucketName() {
            return bucketName;
        }

        public void setBucketName(String bucketName) {
            this.bucketName = bucketName;
        }

        public ObjectInfo() {
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getContent() {
            return content;
        }

        public void setContent(String content) {
            this.content = content;
        }

    }

    public String handle(ObjectInfo objectInfo) {
        String result = "FAILED";

        if (objStoreClient == null) {
            System.err.println("There was a problem creating the ObjectStorage Client object. Please check logs");
            return result;
        }
        try {
            GetNamespaceRequest request = GetNamespaceRequest.builder().build();
            String nameSpace = objStoreClient.getNamespace(request).getValue();
            String name = "cert_test";
            String content = "This is sample content";
            PutObjectRequest por = PutObjectRequest.builder()
                    .namespaceName(nameSpace)
                    .bucketName(objectInfo.bucketName)
                    .objectName(name)
                    .putObjectBody(new ByteArrayInputStream(content.getBytes(StandardCharsets.UTF_8)))
                    .build();

            PutObjectResponse poResp = objStoreClient.putObject(por);
            result = "Successfully submitted Put request for object " + name + " in bucket " + objectInfo.bucketName + ". OPC reuquest ID is " + poResp.getOpcRequestId();
            System.err.println(result);

        } catch (Throwable e) {
            System.err.println("Error storing object in bucket " + e.getMessage());
            result = "Error storing object in bucket " + e.getMessage();
        }

        return result;
    }
}
