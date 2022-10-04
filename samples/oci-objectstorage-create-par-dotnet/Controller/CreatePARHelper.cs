
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


namespace CreatePAR
{
    public class CreatePARHelper
    {

        public static async Task<string> CreatePAR(ObjectStorageClient client, string bucketName, string namespaceName, string parName, int lifetime, string region)

        {

            try
            {
                DateTime currentTime = DateTime.Now;
                DateTime parexpiry = currentTime.AddMinutes(lifetime);
                string object_storage_endpoint = "https://objectstorage." + region + ".oraclecloud.com";
                var createPreauthenticatedRequestDetails = new Oci.ObjectstorageService.Models.CreatePreauthenticatedRequestDetails
                {
                    Name = parName,
                    BucketListingAction = Oci.ObjectstorageService.Models.PreauthenticatedRequest.BucketListingActionEnum.ListObjects,
                    AccessType = Oci.ObjectstorageService.Models.CreatePreauthenticatedRequestDetails.AccessTypeEnum.AnyObjectWrite,
                    TimeExpires = parexpiry
                };
                var createPreauthenticatedRequestRequest = new Oci.ObjectstorageService.Requests.CreatePreauthenticatedRequestRequest
                {
                    NamespaceName = namespaceName,
                    BucketName = bucketName,
                    CreatePreauthenticatedRequestDetails = createPreauthenticatedRequestDetails,
                };

                var response = await client.CreatePreauthenticatedRequest(createPreauthenticatedRequestRequest);
                return object_storage_endpoint + response.PreauthenticatedRequest.AccessUri;


            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Put Object : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
