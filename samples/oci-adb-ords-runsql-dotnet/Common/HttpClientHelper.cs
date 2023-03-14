
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.Common.Http.Signing;
using System.Net.Http;


namespace RunSQL
{
    public class HttpClientHelper
    {
        public static HttpClient GetHttpClient()
        {
            try
            {
                // return new KmsCryptoClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration(), crypto_endpoint);
                return new HttpClient(OciHttpClientHandler.FromAuthProvider(ResourcePrincipalAuthenticationDetailsProvider.GetProvider()));
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new HttpClient(OciHttpClientHandler.FromAuthProvider(new InstancePrincipalsAuthenticationDetailsProvider()));
            }
        }

    }
}
