
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


namespace CopyObjects
{
    public class CopyObjectsHelper
    {
        public static async Task<string> CopyObject(ObjectStorageClient client, string src_bucketName, string dest_bucketName, string namespaceName, string objectName)

        {

            try
            {

                var copyObjectDetails = new Oci.ObjectstorageService.Models.CopyObjectDetails
                {
                    DestinationBucket = dest_bucketName,
                    DestinationNamespace = namespaceName,
                    SourceObjectName = objectName,
                    DestinationObjectName = objectName,
                    DestinationRegion = Environment.GetEnvironmentVariable("REGION"),
                };

                var copyObjectRequest = new Oci.ObjectstorageService.Requests.CopyObjectRequest
                {
                    NamespaceName = namespaceName,
                    BucketName = src_bucketName,
                    CopyObjectDetails = copyObjectDetails,
                };

                var response = await client.CopyObject(copyObjectRequest);
                var opcWorkRequestIdValue = response.OpcWorkRequestId;

                return opcWorkRequestIdValue;

            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Put Object : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
