#
# oci-ons-compute-shape-increase-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

def list_vm_shapes(compute_client, compartment_id, availability_domain):
    list_shapes_response = oci.pagination.list_call_get_all_results(
            compute_client.list_shapes,
            compartment_id,
            availability_domain=availability_domain
        )
    vm_shapes_only = list(filter(lambda shape: shape.shape.startswith("VM"), list_shapes_response.data))
    available_shapes = list(map(lambda shape: shape.shape, vm_shapes_only))
    return available_shapes

    #available_shapes = list_vm_shapes(compute_client, compartment_id, availability_domain)
    #print("available shapes: ", available_shapes, flush=True)