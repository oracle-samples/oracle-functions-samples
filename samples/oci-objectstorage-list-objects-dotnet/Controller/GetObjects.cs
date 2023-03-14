
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;
using Oci.ObjectstorageService.Requests;
using Oci.ObjectstorageService.Responses;


namespace ListObjects
{
    public class ListObjectHelper
    {
        public static async Task<List<ObjectSummary>> GetObjectList(ObjectStorageClient client, string bucketName, string namespaceName)

        {
            string nextpage = "";
            List<ObjectSummary> object_list = new List<ObjectSummary>();
            while (true)
            {
                try
                {

                    var listObjectsRequest = new Oci.ObjectstorageService.Requests.ListObjectsRequest
                    {
                        NamespaceName = namespaceName,
                        BucketName = bucketName,
                        Limit = 1000,
                        Start = nextpage,
                    };

                    var response = await client.ListObjects(listObjectsRequest);
                    nextpage = response.ListObjects.NextStartWith;
                    object_list.AddRange(response.ListObjects.Objects);
                    if (string.IsNullOrEmpty(nextpage))
                    {
                        break;
                    }
                }

                catch (OciException ex)
                {
                    Console.WriteLine("Unable To Get Object List: {0}", ex.Message);
                    return new List<ObjectSummary>();
                }
            }
            return object_list;
        }


    }
}
