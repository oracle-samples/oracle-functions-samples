
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.KeymanagementService;


namespace VaultDecrypt
{
    public class KmsCryptoClientHelper
    {
        public static KmsCryptoClient GetVaultDecryptClient(string crypto_endpoint)
        {
            try
            {
                return new KmsCryptoClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration(), crypto_endpoint);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new KmsCryptoClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration(), crypto_endpoint);
            }
        }

    }
}
