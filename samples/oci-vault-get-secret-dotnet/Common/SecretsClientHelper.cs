
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.SecretsService;


namespace GetSecrets
{
    public class SecretsClientHelper
    {
        public static SecretsClient GetSecretsClient()
        {
            try
            {
                return new SecretsClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new SecretsClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration());
            }
        }

    }
}
