using Fnproject.Fn.Fdk;
using System.Runtime.CompilerServices;
using System.Collections.Generic;
using System.Collections;
using System.Collections.Specialized;
using System;
using System.IO;
using System.IO.Compression;
using System.Data;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.DatabaseService;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Oracle.ManagedDataAccess.Client;


namespace RunSQL
{
    class Function
    {

        public static String sqlDatoToJson(OracleDataReader dataReader)
        {
            var dataTable = new DataTable();
            dataTable.Load(dataReader);
            string JSONString = string.Empty;
            JSONString = JsonConvert.SerializeObject(dataTable);
            return JSONString;
        }

        public static string runsqlquery(string sql)
        {
            // var TNS_ADMIN = Environment.GetEnvironmentVariable("TNS_ADMIN");
            // var ADB_OCID = Environment.GetEnvironmentVariable("ADB_OCID");
            var DBUSER = Environment.GetEnvironmentVariable("DBUSER");
            var DBPWD_CYPHER = Environment.GetEnvironmentVariable("DBPWD_CYPHER");
            var DBSVC = Environment.GetEnvironmentVariable("DBSVC");

            string conString = "User Id=" + DBUSER + ";Password=" + DBPWD_CYPHER + ";Data Source=" + DBSVC + ";Connection Timeout=30;";
            using (OracleConnection con = new OracleConnection(conString))
            {

                using (OracleCommand cmd = con.CreateCommand())
                {
                    try
                    {
                        con.Open();
                        Console.WriteLine("Successfully connected to Oracle Autonomous Database");
                        Console.WriteLine();

                        cmd.CommandText = sql;
                        OracleDataReader reader = cmd.ExecuteReader();
                        string json_string = sqlDatoToJson(reader);
                        Console.WriteLine(json_string);
                        return json_string;
                    }
                    catch (Exception ex)
                    {

                        Console.WriteLine(ex.Message);
                        List<Dictionary<string, string>> rows = new List<Dictionary<string, string>>();
                        Dictionary<string, string> col = new Dictionary<string, string>();
                        col.Add("error", ex.Message);
                        rows.Add(col);
                        string JSONString = JsonConvert.SerializeObject(rows);
                        return JSONString;
                    }

                }
            }

        }
        public string function_handler(InputMessage input)
        {
            var TNS_ADMIN = Environment.GetEnvironmentVariable("TNS_ADMIN");
            var ADB_OCID = Environment.GetEnvironmentVariable("ADB_OCID");
            var DBUSER = Environment.GetEnvironmentVariable("DBUSER");
            var DBPWD_CYPHER = Environment.GetEnvironmentVariable("DBPWD_CYPHER");
            var DBSVC = Environment.GetEnvironmentVariable("DBSVC");

            _ = TNS_ADMIN ?? throw new ArgumentNullException(paramName: nameof(TNS_ADMIN), message: "TNS_ADMIN can't be null");
            _ = ADB_OCID ?? throw new ArgumentNullException(paramName: nameof(ADB_OCID), message: "Autonomous DB OCID can't be null");
            _ = DBUSER ?? throw new ArgumentNullException(paramName: nameof(DBUSER), message: "Autonomous DB DBUSER can't be null");
            _ = DBPWD_CYPHER ?? throw new ArgumentNullException(paramName: nameof(DBPWD_CYPHER), message: "Autonomous DB DBPWD_CYPHER can't be null");
            _ = DBSVC ?? throw new ArgumentNullException(paramName: nameof(DBSVC), message: "Autonomous DB DBSVC can't be null");

            DatabaseClient client = DBClientHelper.GetDBClient();
            Task<string> wallet_str = GenerateDBWalletHelper.GenWallet(client, ADB_OCID, TNS_ADMIN);
            Console.WriteLine("Result of Generate wallet  : {0}", wallet_str.Result);

            Dictionary<string, List<OutputDetails>> output = new Dictionary<string, List<OutputDetails>>();
            Dictionary<string, string> result = new Dictionary<string, string>();
            var query_result_list = new List<OutputDetails>();

            string sql = input.sql;
            string query_result = runsqlquery(sql);
            Console.WriteLine("Result of query  : {0}", query_result);
            JArray a = JArray.Parse(query_result);
            List<Dictionary<string, string>> rows = new List<Dictionary<string, string>>();

            foreach (JObject o in a.Children<JObject>())
            {
                Dictionary<string, string> col = new Dictionary<string, string>();
                foreach (JProperty p in o.Properties())
                {
                    string name = p.Name;
                    string value = (string)p.Value;
                    col.Add(name, value);

                }
                rows.Add(col);
            }

            var query_detail = new OutputDetails();
            query_detail.sql = sql;
            // query_detail.result = query_result;
            query_detail.result = rows;
            query_result_list.Add(query_detail);
            output.Add("output", query_result_list);
            // return query_result;
            // return System.Text.Json.JsonSerializer.Serialize(output);
            return JsonConvert.SerializeObject(output);


        }


        static void Main(string[] args)
        {

            Console.WriteLine("*******   HELLO FUNCTION   **************");

            var TNS_ADMIN = Environment.GetEnvironmentVariable("TNS_ADMIN");
            _ = TNS_ADMIN ?? throw new ArgumentNullException(paramName: nameof(TNS_ADMIN), message: "TNS_ADMIN can't be null");
            OracleConfiguration.TnsAdmin = TNS_ADMIN;
            OracleConfiguration.WalletLocation = OracleConfiguration.TnsAdmin;
            Fdk.Handle(args[0]);

        }



    }
}
