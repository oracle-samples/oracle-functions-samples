using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.ObjectstorageService;
using Oci.ObjectstorageService.Models;

namespace CreatePAR
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();
            string parName = input.PARName;
            string bucketName = Environment.GetEnvironmentVariable("BUCKET_NAME");
            string namespaceName = Environment.GetEnvironmentVariable("NAMESPACE");
            int lifetime = Int32.Parse(Environment.GetEnvironmentVariable("LIFETIME"));
            string region = Environment.GetEnvironmentVariable("REGION");
            ObjectStorageClient client = ObjectStorageClientHelper.GetObjectStorageClient();
            Task<string> object_str = CreatePARHelper.CreatePAR(client, bucketName, namespaceName, parName, lifetime, region);
            var object_detail = new ObjectDetails();
            object_detail.parname = parName;
            object_detail.bucketname = bucketName;
            object_detail.parurl = object_str.Result;
            object_details_list.Add(object_detail);

            output.Add("results", object_details_list);
            return JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
