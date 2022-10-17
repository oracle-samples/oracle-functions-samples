
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using System.IO;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.KeymanagementService;
using Oci.KeymanagementService.Models;
using Oci.KeymanagementService.Requests;
using Oci.KeymanagementService.Responses;


namespace VaultDecrypt
{
    public class GetSecretsHelper
    {
        public static async Task<string> getSecretValue(KmsCryptoClient client, string vault_key_ocid, string cipher)

        {

            try
            {


                // Create a request and dependent object(s).
                var decryptDataDetails = new Oci.KeymanagementService.Models.DecryptDataDetails
                {
                    Ciphertext = cipher,
                    KeyId = vault_key_ocid,
                };

                var decryptRequest = new Oci.KeymanagementService.Requests.DecryptRequest
                {
                    DecryptDataDetails = decryptDataDetails,
                };


                var response = await client.Decrypt(decryptRequest);
                var value_b64 = response.DecryptedData.Plaintext;
                byte[] secretValueDecoded = Convert.FromBase64String(value_b64);
                string secretIdValue = Encoding.Default.GetString(secretValueDecoded);
                return secretIdValue;

            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Get Secret : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
