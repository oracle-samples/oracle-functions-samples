
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.ObjectstorageService;


namespace CreatePAR
{
    public class ObjectStorageClientHelper
    {
        public static ObjectStorageClient GetObjectStorageClient()
        {
            try
            {
                return new ObjectStorageClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new ObjectStorageClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration());
            }
        }

    }
}
