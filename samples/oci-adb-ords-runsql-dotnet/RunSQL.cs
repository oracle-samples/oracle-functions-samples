using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System.Collections;
using System.Collections.Specialized;
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.Common.Http.Signing;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


namespace RunSQL
{
    class Function
    {
        public string function_handler(InputMessage input)
        {


            Dictionary<string, List<OutputDetails>> output = new Dictionary<string, List<OutputDetails>>();
            Dictionary<string, string> result = new Dictionary<string, string>();
            var query_result_list = new List<OutputDetails>();

            var ords_base_url = Environment.GetEnvironmentVariable("ords_base_url");
            var db_schema = Environment.GetEnvironmentVariable("db_schema");
            var db_pwd_cypher = Environment.GetEnvironmentVariable("db_pwd_cypher");


            string sql = input.sql;

            string dbsqlurl = ords_base_url + db_schema + "/_/sql";
            string auth_str = db_schema + ":" + db_pwd_cypher;
            string authString = Convert.ToBase64String(Encoding.UTF8.GetBytes(auth_str));

            HttpClient client = HttpClientHelper.GetHttpClient();
            HttpClient client1 = new HttpClient();

            Task<string> response_value = InvokeHttpCall(client1, dbsqlurl, authString, sql);
            string response_str = response_value.Result;
            JObject json = JObject.Parse(response_str);
            var query_detail = new OutputDetails();
            foreach (JToken item in json.SelectToken("items"))
            {

                Console.WriteLine(item.SelectToken("statementText"));
                query_detail.sql = item.SelectToken("statementText").ToString();
                if (item.SelectToken("resultSet.items") != null)
                {
                    query_detail.result = item.SelectToken("resultSet.items").ToObject<List<Dictionary<string, string>>>();
                    query_detail.error = new List<string>();
                    Console.WriteLine(item.SelectToken("resultSet.items").ToString(Newtonsoft.Json.Formatting.Indented));
                }
                else if (item.SelectToken("errorDetails") != null)
                {
                    query_detail.result = new List<Dictionary<string, string>>();
                    string error = item.SelectToken("errorDetails").ToString();
                    query_detail.error = new List<string>();
                    query_detail.error.Add(error);
                }
                query_result_list.Add(query_detail);


            }
            output.Add("output", query_result_list);
            return System.Text.Json.JsonSerializer.Serialize(output);
        }

        static void Main(string[] args) { Fdk.Handle(args[0]); }

        public static async Task<string> InvokeHttpCall(HttpClient client, string dbsqlurl, string authString, string sql)
        {
            try
            {

                HttpRequestMessage request = new HttpRequestMessage
                {
                    Method = HttpMethod.Post,
                    RequestUri = new Uri(dbsqlurl),
                    Content = new StringContent(sql, Encoding.UTF8, "application/sql"),
                };

                client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", authString);

                var response = await client.SendAsync(request);

                Console.WriteLine("Is rest call successful: {0}", response.IsSuccessStatusCode);
                var responseJson = await response.Content.ReadAsStringAsync();
                Console.WriteLine("Parsed Response: {0}", responseJson);

                return responseJson;
            }
            catch (OciException ex)
            {
                Console.WriteLine("Unable To Invoke HTTP : {0}", ex.Message);
                return "Failed " + ex.Message;
            }
        }

    }
}
