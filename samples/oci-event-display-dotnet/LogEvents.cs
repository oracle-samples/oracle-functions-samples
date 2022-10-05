using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Newtonsoft.Json;


namespace LogEvents
{
    class Function
    {
        public string function_handler(String input)
        {

            Dictionary<string, List<ObjectDetails>> output = new Dictionary<string, List<ObjectDetails>>();
            var object_details_list = new List<ObjectDetails>();
            dynamic event_json = JsonConvert.DeserializeObject(input);
            var event_str = Newtonsoft.Json.JsonConvert.SerializeObject(event_json, Newtonsoft.Json.Formatting.Indented);
            Console.WriteLine("event type: {0} ", event_json.eventType);
            Console.WriteLine("compartment name: {0} ", event_json.data.compartmentName);
            Console.WriteLine("Full Cloud event json data:");
            Console.WriteLine(event_str);
            var object_detail = new ObjectDetails();

            object_detail.result = event_str;

            output.Add("results", object_details_list);
            return System.Text.Json.JsonSerializer.Serialize(output);

        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

    }
}
