using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.FunctionsService;
using Oci.FunctionsService.Models;

namespace InvokeFn
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();
            string function_ocid = input.function_ocid;
            string function_endpoint = input.function_endpoint;
            string function_body = input.function_body;

            FunctionsInvokeClient client = FunctionClientHelper.GetFunctionClient(function_endpoint);
            Task<string> object_str = InvokeFnHelper.TriggerFunction(client, function_ocid, function_endpoint, function_body);
            var object_detail = new ObjectDetails();
            object_detail.result = object_str.Result;
            object_details_list.Add(object_detail);

            output.Add("results", object_details_list);
            return System.Text.Json.JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
