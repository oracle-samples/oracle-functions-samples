using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.SecretsService;
using Oci.SecretsService.Models;

namespace GetSecrets
{
    class Function
    {
        public string function_handler()
        {

            Dictionary<string, List<SecretContent>> output = new Dictionary<string, List<SecretContent>>();
            var secret_details_list = new List<SecretContent>();

            string secret_ocid = Environment.GetEnvironmentVariable("secret_ocid");

            SecretsClient client = SecretsClientHelper.GetSecretsClient();

            Task<string> secret_value = GetSecretsHelper.getSecretValue(client, secret_ocid);

            var secret_detail = new SecretContent();
            secret_detail.secret_content = secret_value.Result;
            secret_details_list.Add(secret_detail);

            output.Add("secret_content", secret_details_list);
            return System.Text.Json.JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
