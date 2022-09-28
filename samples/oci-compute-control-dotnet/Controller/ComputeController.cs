
using System;
using System.Threading.Tasks;
using System.Text;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.CoreService;
using Oci.CoreService.Models;
using Oci.CoreService.Requests;
using Oci.CoreService.Responses;

namespace ControlInstance
{
    public class ComputeController
    {
        public static async Task<string> GetComputeStatus(ComputeClient client,string instance_ocid)
        {
            try
            {
                var getInstanceRequest = new Oci.CoreService.Requests.GetInstanceRequest
                {
                    InstanceId = instance_ocid
                };

                var getInstancesResponse = await client.GetInstance(getInstanceRequest);
                return getInstancesResponse.Instance.LifecycleState.ToString();
            }
            catch (OciException  ex)
            {
                return ex.ServiceCode;
            }
        }

        public static async Task<string> StartCompute(ComputeClient client,string instance_ocid)
        {
            Console.WriteLine($"Starting Instance Id: {instance_ocid}"); 
            try
            {
                if (GetComputeStatus(client,instance_ocid).Result == "Stopped" )
                {
                    var instanceActionRequest = new Oci.CoreService.Requests.InstanceActionRequest
                    {
                        InstanceId = instance_ocid,
                        Action = "START",
                    };

                    var getInstancesResponse = await client.InstanceAction(instanceActionRequest);
                    Console.WriteLine($"Start Response Code : {getInstancesResponse.Instance.LifecycleState.ToString()}"); 
                    return GetComputeStatus(client,instance_ocid).Result;
                }
                else
                {
                    Console.WriteLine($"Instance Is Already Running");
                    return "Instance Is Already Running";
                }
            }
            catch (OciException ex)
            {
                return ex.Message;
            }
        }

        public static async Task<string> StopCompute(ComputeClient client,string instance_ocid)
        {
            Console.WriteLine($"Stopping Instance Id: {instance_ocid}"); 
            try
            {
                if (GetComputeStatus(client,instance_ocid).Result == "Running" )
                {
                    var instanceActionRequest = new Oci.CoreService.Requests.InstanceActionRequest
                    {
                        InstanceId = instance_ocid,
                        Action = "STOP",
                    };

                    var getInstancesResponse = await client.InstanceAction(instanceActionRequest);
                    Console.WriteLine($"Stop Response Code : {getInstancesResponse.Instance.LifecycleState.ToString()}"); 
                    return GetComputeStatus(client,instance_ocid).Result;
                }
                else
                {
                    Console.WriteLine($"Instance Is Already Stopped");
                    return "Instance Is Already Stopped";
                }
            }
            catch (OciException ex)
            {
                return ex.Message;
            }
        }

    }
}
