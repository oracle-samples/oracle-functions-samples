
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.IdentityService;
using Oci.IdentityService.Models;
using Oci.IdentityService.Requests;
using Oci.IdentityService.Responses;


namespace ListCompartment
{
    public class ListComparmentHelper
    {
        public static async Task<List<Compartment>> GetComparmentList(IdentityClient client, string parent_compartment_ocid)

        {
            string nextpage = "";
            List<Compartment> comp_list = new List<Compartment>();
            while (true)
            {
                try
                {

                    var listCompartmentsRequest = new Oci.IdentityService.Requests.ListCompartmentsRequest
                    {
                        CompartmentId = parent_compartment_ocid,
                        AccessLevel = Oci.IdentityService.Requests.ListCompartmentsRequest.AccessLevelEnum.Any,
                        CompartmentIdInSubtree = true,
                        Page = nextpage,
                        Limit = 1000,
                        SortBy = Oci.IdentityService.Requests.ListCompartmentsRequest.SortByEnum.Name,
                        SortOrder = Oci.IdentityService.Requests.ListCompartmentsRequest.SortOrderEnum.Asc,
                        LifecycleState = Oci.IdentityService.Models.Compartment.LifecycleStateEnum.Active
                    };

                    var response = await client.ListCompartments(listCompartmentsRequest);
                    nextpage = response.OpcNextPage;
                    comp_list.AddRange(response.Items);
                    if (string.IsNullOrEmpty(nextpage))
                    {
                        break;
                    }
                }

                catch (OciException ex)
                {
                    Console.WriteLine("Unable To Get Compartment List: {0}", ex.Message);
                    return new List<Compartment>();
                }
            }
            return comp_list;
        }


    }
}
