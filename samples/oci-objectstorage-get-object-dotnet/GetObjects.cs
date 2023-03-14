using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;

namespace GetObjects
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
            ObjectStorageClient client = ObjectStorageClientHelper.GetObjectStorageClient();
            Task<string> object_str = GetObjectHelper.GetObject(client, bucketName, namespaceName, objectName);
            var object_detail = new ObjectDetails();
            if (object_str.Result != "object not found!")
            {
                byte[] data = Convert.FromBase64String(object_str.Result);
                string decodedString = Encoding.UTF8.GetString(data);
                object_detail.name = objectName;
                object_detail.content = decodedString;
                object_details_list.Add(object_detail);
            }

            output.Add("results", object_details_list);
            return JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
