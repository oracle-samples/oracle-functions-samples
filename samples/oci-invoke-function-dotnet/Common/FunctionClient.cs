
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.FunctionsService;


namespace InvokeFn
{
    public class FunctionClientHelper
    {
        public static FunctionsInvokeClient GetFunctionClient(string function_endpoint)
        {
            try
            {
                return new FunctionsInvokeClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration(), function_endpoint);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider: {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new FunctionsInvokeClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration(), function_endpoint);
            }
        }

    }
}
