using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;

namespace PutObjects
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();
            string bucketName = input.bucketName;
            string objectName = input.objectName;
            string namespaceName = input.namespaceName;
            string content = input.content;
            ObjectStorageClient client = ObjectStorageClientHelper.GetObjectStorageClient();
            Task<string> object_str = PutObjectsHelper.PutObject(client, bucketName, namespaceName, objectName, content);
            var object_detail = new ObjectDetails();
            object_detail.name = objectName;
            object_detail.bucketname = bucketName;
            object_detail.result = object_str.Result;
            object_details_list.Add(object_detail);

            output.Add("results", object_details_list);
            return JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
