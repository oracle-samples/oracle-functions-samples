
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.CoreService;


namespace ControlInstance
{
    public class ComputeClientHelper
    {
        public static ComputeClient GetComputeClient()
        {
            try{

                return new ComputeClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration());
            }
            catch(Exception ex) {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new ComputeClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration());
            }
        }

    }
}
