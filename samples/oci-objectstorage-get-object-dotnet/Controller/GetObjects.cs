
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using System.IO;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;
using Oci.ObjectstorageService.Requests;
using Oci.ObjectstorageService.Responses;


namespace GetObjects
{
    public class GetObjectHelper
    {
        public static async Task<string> GetObject(ObjectStorageClient client, string bucketName, string namespaceName, string objectName)

        {

            try
            {

                var getObjectRequest = new Oci.ObjectstorageService.Requests.GetObjectRequest
                {
                    NamespaceName = namespaceName,
                    BucketName = bucketName,
                    ObjectName = objectName,
                };

                var response = await client.GetObject(getObjectRequest);
                byte[] bytes;
                using (var memoryStream = new MemoryStream())
                {
                    response.InputStream.CopyTo(memoryStream);
                    bytes = memoryStream.ToArray();
                }

                return Convert.ToBase64String(bytes);
            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Get Object : {0}", ex.Message);
                return "object not found!";
            }

        }


    }
}
