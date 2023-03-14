using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using MailKit.Net.Smtp;
using MailKit.Security;
using MailKit;
using MimeKit;

namespace SendEmail
{
    class Function
    {
        public Output function_handler(InputMessage input)
        {

            string smtp_password = Environment.GetEnvironmentVariable("smtp-password");
            string smtp_user_name = Environment.GetEnvironmentVariable("smtp-username");
            string smtp_endpoint = Environment.GetEnvironmentVariable("smtp-host");
            string smtp_port_str = Environment.GetEnvironmentVariable("smtp-port");
            int smtp_port = Int32.Parse(smtp_port_str);
            string from_email = input.sender_email;
            string from_name = input.sender_name;

            var message = new MimeMessage();
            message.From.Add(new MailboxAddress(from_name, from_email));
            message.To.Add(new MailboxAddress("Dear recipient", input.recipient));
            message.Subject = input.subject;

            message.Body = new TextPart("plain")
            {
                Text = @input.body
            };

            try
            {


                using (var client = new SmtpClient())
                {
                    client.Connect(smtp_endpoint, smtp_port, SecureSocketOptions.StartTls);
                    client.Authenticate(smtp_user_name, smtp_password);
                    client.Send(message);
                    client.Disconnect(true);
                }

                return new Output(string.Format(
                    "Mail Sent to  {0}!",
                    string.IsNullOrEmpty(input.recipient) ? "<invalid_email_id>" : input.recipient.Trim()));

            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
                return new Output(string.Format(ex.Message));

            }

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
