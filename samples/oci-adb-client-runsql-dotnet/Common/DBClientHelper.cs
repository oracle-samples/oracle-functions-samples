
using System;
using System.Threading.Tasks;
using System.Text;

using Oci.Common;
using Oci.Common.Auth;
using Oci.DatabaseService;

namespace RunSQL
{
    public class DBClientHelper
    {
        public static DatabaseClient GetDBClient()
        {
            try
            {
                return new DatabaseClient(ResourcePrincipalAuthenticationDetailsProvider.GetProvider(), new ClientConfiguration());
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unable To Create Resource Principal Provider : {0}", ex.Message);
                Console.WriteLine("Defaulting to Instance Provider");
                return new DatabaseClient(new InstancePrincipalsAuthenticationDetailsProvider(), new ClientConfiguration());
            }
        }

    }
}
