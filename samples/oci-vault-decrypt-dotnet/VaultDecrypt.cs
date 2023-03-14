using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.KeymanagementService;
using Oci.KeymanagementService.Models;

namespace VaultDecrypt
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<SecretContent>> output = new Dictionary<string, List<SecretContent>>();
            var secret_details_list = new List<SecretContent>();

            string cipher = input.cipher;
            string vault_key_ocid = Environment.GetEnvironmentVariable("key_ocid");
            string crypto_endpoint = Environment.GetEnvironmentVariable("cryptographic_endpoint");


            KmsCryptoClient client = KmsCryptoClientHelper.GetVaultDecryptClient(crypto_endpoint);

            Task<string> secret_value = GetSecretsHelper.getSecretValue(client, vault_key_ocid, cipher);

            var secret_detail = new SecretContent();
            secret_detail.secret_content = secret_value.Result;
            secret_details_list.Add(secret_detail);

            output.Add("secret_content", secret_details_list);
            return System.Text.Json.JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
