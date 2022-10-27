using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.OnsService;
using Oci.OnsService.Models;

namespace PublishONS
{
    class Function
    {
        public string function_handler(InputMessage input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();
            string topic_id = input.topic_id;
            string msg_title = input.msg_title;
            string msg_body = input.msg_body;

            NotificationDataPlaneClient client = ONSClientHelper.GetONSClient();
            Task<string> messageIdValue = InvokeONSHelper.SendMessage(client, topic_id, msg_title, msg_body);

            var object_detail = new ObjectDetails();
            object_detail.result = messageIdValue.Result;
            object_details_list.Add(object_detail);

            output.Add("results", object_details_list);
            return System.Text.Json.JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
