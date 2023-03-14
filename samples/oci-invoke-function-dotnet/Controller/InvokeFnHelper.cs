
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using System.IO;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.FunctionsService;
using Oci.FunctionsService.Models;
using Oci.FunctionsService.Requests;
using Oci.FunctionsService.Responses;


namespace InvokeFn
{
    public class InvokeFnHelper
    {
        public static Stream GenerateStreamFromString(string s)
        {
            var stream = new MemoryStream();
            var writer = new StreamWriter(stream);
            writer.Write(s);
            writer.Flush();
            stream.Position = 0;
            return stream;
        }
        public static async Task<string> TriggerFunction(FunctionsInvokeClient client, string function_ocid, string function_endpoint, string function_body)

        {

            try
            {

                Console.WriteLine("Function endpoint : {0}", function_endpoint);
                var invokeFunctionRequest = new Oci.FunctionsService.Requests.InvokeFunctionRequest
                {
                    FunctionId = function_ocid,
                    InvokeFunctionBody = GenerateStreamFromString(function_body),
                };

                var response = await client.InvokeFunction(invokeFunctionRequest);
                byte[] bytes;
                using (var memoryStream = new MemoryStream())
                {
                    response.InputStream.CopyTo(memoryStream);
                    bytes = memoryStream.ToArray();
                }
                return Encoding.UTF8.GetString(bytes);

            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Invoke Function : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
