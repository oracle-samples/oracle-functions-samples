using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.IdentityService;
using Oci.IdentityService.Models;

namespace ListCompartment
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<CompartmentDetails>> output = new Dictionary<string, List<CompartmentDetails>>();
            var compartment_details_list = new List<CompartmentDetails>();
            string parent_compartment_ocid;
            parent_compartment_ocid = input.compartment_ocid;
            Console.WriteLine($"Getting Compartment tree for parent ocid : {parent_compartment_ocid}");
            IdentityClient client = IdentityClientHelper.GetIdentityClient();
            Task<List<Compartment>> compartment_list = ListComparmentHelper.GetComparmentList(client, parent_compartment_ocid);

            foreach (Compartment comp in compartment_list.Result)
            {
                var compartment_detail = new CompartmentDetails();
                compartment_detail.name = comp.Name;
                compartment_detail.ocid = comp.Id;
                compartment_details_list.Add(compartment_detail);
            }

            output.Add("results", compartment_details_list);
            return JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
