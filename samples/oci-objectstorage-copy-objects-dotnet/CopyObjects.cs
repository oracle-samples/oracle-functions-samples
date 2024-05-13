using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;

namespace CopyObjects
{
    class Function
    {
        public string function_handler(String input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();

            dynamic event_json = JsonConvert.DeserializeObject(input);

            string src_bucketName = event_json.data.additionalDetails["bucketName"];
            string dest_bucketName = event_json.data.additionalDetails["bucketName"] + "_IMMUTABLE";
            string namespaceName = event_json.data.additionalDetails["namespace"];
            string objectName = event_json.data.resourceName;

            ObjectStorageClient client = ObjectStorageClientHelper.GetObjectStorageClient();
            Task<string> object_str = CopyObjectsHelper.CopyObject(client, src_bucketName, dest_bucketName, namespaceName, objectName);
            var object_detail = new ObjectDetails();
            object_detail.result = object_str.Result;
            object_details_list.Add(object_detail);

            output.Add("results", object_details_list);
            return System.Text.Json.JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
