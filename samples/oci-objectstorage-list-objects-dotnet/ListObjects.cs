using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;

namespace ListObjects
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();
            string bucketName = input.bucketName;
            string namespaceName = input.namespaceName;
            ObjectStorageClient client = ObjectStorageClientHelper.GetObjectStorageClient();
            Task<List<ObjectSummary>> object_list = ListObjectHelper.GetObjectList(client, bucketName, namespaceName);

            foreach (ObjectSummary oss_object in object_list.Result)
            {
                var object_detail = new ObjectDetails();
                object_detail.name = oss_object.Name;
                object_details_list.Add(object_detail);
            }

            output.Add("results", object_details_list);
            return JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
