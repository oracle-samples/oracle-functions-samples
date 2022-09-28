
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


namespace PutObjects
{
    public class PutObjectsHelper
    {
        private static Stream GenerateStreamFromString(string inputString)
        {
            var stream = new MemoryStream();
            var writer = new StreamWriter(stream);
            writer.Write(inputString);
            writer.Flush();
            stream.Position = 0;
            return stream;
        }
        public static async Task<string> PutObject(ObjectStorageClient client, string bucketName, string namespaceName, string objectName, string content)

        {

            try
            {

                var putObjectRequest = new Oci.ObjectstorageService.Requests.PutObjectRequest
                {
                    NamespaceName = namespaceName,
                    BucketName = bucketName,
                    ObjectName = objectName,
                    PutObjectBody = GenerateStreamFromString(content),
                };

                var response = await client.PutObject(putObjectRequest);
                var hasValueValue = response.LastModified.HasValue;

                return "Success!";

            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Put Object : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
