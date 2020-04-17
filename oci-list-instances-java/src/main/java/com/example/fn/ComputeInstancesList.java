/*
** ComputeInstancesList version 1.0.
**
** Copyright (c) 2020 Oracle, Inc.
** Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
*/

package com.example.fn;

import com.oracle.bmc.auth.ResourcePrincipalAuthenticationDetailsProvider;
import com.oracle.bmc.core.ComputeClient;
import com.oracle.bmc.core.model.Instance;
import com.oracle.bmc.core.requests.ListInstancesRequest;
import com.oracle.bmc.core.responses.ListInstancesResponse;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ComputeInstancesList {

    private ComputeClient computeClient = null;
    final ResourcePrincipalAuthenticationDetailsProvider provider
            = ResourcePrincipalAuthenticationDetailsProvider.builder().build();

    public ComputeInstancesList() {

        //print env vars in Functions container
        System.err.println("OCI_RESOURCE_PRINCIPAL_VERSION " + System.getenv("OCI_RESOURCE_PRINCIPAL_VERSION"));
        System.err.println("OCI_RESOURCE_PRINCIPAL_REGION " + System.getenv("OCI_RESOURCE_PRINCIPAL_REGION"));
        System.err.println("OCI_RESOURCE_PRINCIPAL_RPST " + System.getenv("OCI_RESOURCE_PRINCIPAL_RPST"));
        System.err.println("OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM " + System.getenv("OCI_RESOURCE_PRINCIPAL_PRIVATE_PEM"));

        try {

            computeClient = new ComputeClient(provider);

        } catch (Throwable ex) {
            System.err.println("Failed to instantiate ComputeClient - " + ex.getMessage());
            ex.printStackTrace();
        }
    }

    public Map<String, String> handle(String compID) {

        Map<String, String> names = Collections.emptyMap();

        if (computeClient == null) {
            System.err.println("There was a problem creating the ComputeClient object. Please check logs...");
            return names;
        }

        try {
            System.err.println("Searching for compute instances in compartment " + compID);

            ListInstancesRequest request = ListInstancesRequest.builder().compartmentId(compID).build();
            System.err.println("ListInstancesRequest " + request);

            ListInstancesResponse instances = computeClient.listInstances(request);
            System.err.println("ListInstancesResponse " + instances);

            List<Instance> instanceList = instances.getItems();
            System.err.println("No. of compute instances found in compartment " + instanceList.size());

             names = instanceList.stream()
//                     .collect(Collectors.toMap((instance) -> instance.getId(), (instance) -> instance.toString()));
                     .collect(Collectors.toMap(Instance::getId, Instance::toString));

            System.err.println("Compute instances " + names);

        } catch (Throwable e) {
            System.err.println("ERROR searching for compute instances in compartment " + compID);
            System.err.println("e.getMessage() " + e.getMessage());
            e.printStackTrace();
        }

        return names;
    }
}
