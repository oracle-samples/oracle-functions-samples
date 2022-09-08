using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

using Oci.Common;
using Oci.Common.Auth;
using Oci.CoreService;

using Oci.CoreService.Models;
using Oci.CoreService.Requests;
using Oci.CoreService.Responses;

namespace ListInstance
{
    class Function
    {
        public string function_handler(string compartment_id)
        {
            Task<List<Instance>> inst_list = list_instances(compartment_id);
            var instance_details_list = new List<InstanceDetails>();
            Dictionary<string, List<InstanceDetails>> output = new Dictionary<string, List<InstanceDetails>>();

            foreach (Instance inst in inst_list.Result)
            {
                var instance_detail = new InstanceDetails();
                instance_detail.name = inst.DisplayName;
                instance_detail.ocid = inst.Id;
                instance_detail.state = inst.LifecycleState.ToString();
                instance_details_list.Add(instance_detail);
            }
            output.Add("instances", instance_details_list);
            return JsonSerializer.Serialize(output);
        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

        public async Task<List<Instance>> list_instances(string comp_id)
        {

            var provider = ResourcePrincipalAuthenticationDetailsProvider.GetProvider();
            var listInstancesRequest = new Oci.CoreService.Requests.ListInstancesRequest
            {
                CompartmentId = comp_id
            };
            // Create a service client and send the request.
            using (var client = new ComputeClient(provider, new ClientConfiguration()))
            {
                var listInstancesResponse = await client.ListInstances(listInstancesRequest);
                return listInstancesResponse.Items;
            }


        }
    }
}
