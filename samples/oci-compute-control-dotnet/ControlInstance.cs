using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.CoreService;

namespace ControlInstance
{
    class Function
    {
        public string function_handler(InputMessage input)
        {
            string command;
            string instance_ocid;
            Dictionary<string, string> output = new Dictionary<string, string>();
            try{
                command=input.command.ToLower();
                instance_ocid=input.instance_ocid;
                ComputeClient client = ComputeClientHelper.GetComputeClient();
                if (command=="status")
                {
                    Task<string> instance_state = ComputeController.GetComputeStatus(client,instance_ocid);
                    output.Add("result", instance_state.Result);
                }
                else if (command=="start")
                {   
                    Task<string> instance_state = ComputeController.StartCompute(client,instance_ocid);
                    output.Add("result", instance_state.Result);
                }
                else if (command=="stop")
                {   
                    Task<string> instance_state = ComputeController.StopCompute(client,instance_ocid);
                    output.Add("result", instance_state.Result);
                }
                else 
                {
                    output.Add("result", "Invalid Command");
                }

                return JsonSerializer.Serialize(output); 

            }
            catch(Exception ex){
                Console.WriteLine($"Invalid Payload: {ex.Message}"); 
                output.Add("result", "Invalid Payload");
                return JsonSerializer.Serialize(output); 
            }
        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
