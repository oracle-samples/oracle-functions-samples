
using System;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using System.IO;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.OnsService;
using Oci.OnsService.Models;
using Oci.OnsService.Requests;
using Oci.OnsService.Responses;


namespace PublishONS
{
    public class InvokeONSHelper
    {
        public static async Task<string> SendMessage(NotificationDataPlaneClient client, string topic_id, string msg_title, string msg_body)

        {

            try
            {

                // Create a request and dependent object(s).
                var messageDetails = new Oci.OnsService.Models.MessageDetails
                {
                    Title = msg_title,
                    Body = msg_body
                };
                var publishMessageRequest = new Oci.OnsService.Requests.PublishMessageRequest
                {
                    TopicId = topic_id,
                    MessageDetails = messageDetails,
                    MessageType = Oci.OnsService.Requests.PublishMessageRequest.MessageTypeEnum.RawText
                };

                var response = await client.PublishMessage(publishMessageRequest);
                var messageIdValue = response.PublishResult.MessageId;
                return messageIdValue;

            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Send Message to ONS : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
