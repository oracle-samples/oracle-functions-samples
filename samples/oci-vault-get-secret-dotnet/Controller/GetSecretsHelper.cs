
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using System.IO;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.SecretsService;
using Oci.SecretsService.Models;
using Oci.SecretsService.Requests;
using Oci.SecretsService.Responses;


namespace GetSecrets
{
    public class GetSecretsHelper
    {
        public static async Task<string> getSecretValue(SecretsClient client, string secret_ocid)

        {

            try
            {

                var getSecretBundleRequest = new Oci.SecretsService.Requests.GetSecretBundleRequest
                {
                    SecretId = secret_ocid,
                    Stage = Oci.SecretsService.Requests.GetSecretBundleRequest.StageEnum.Latest
                };


                var response = await client.GetSecretBundle(getSecretBundleRequest);
                Base64SecretBundleContentDetails b64_secret_contents = (Base64SecretBundleContentDetails)response.SecretBundle.SecretBundleContent;
                byte[] secretValueDecoded = Convert.FromBase64String(b64_secret_contents.Content);
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
