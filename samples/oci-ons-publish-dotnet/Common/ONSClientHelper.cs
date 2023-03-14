
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.OnsService;


namespace PublishONS
{
    public class ONSClientHelper
    {
        public static NotificationDataPlaneClient GetONSClient()
        {
            try
            {
                return new NotificationDataPlaneClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new NotificationDataPlaneClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration());
            }
        }

    }
}
