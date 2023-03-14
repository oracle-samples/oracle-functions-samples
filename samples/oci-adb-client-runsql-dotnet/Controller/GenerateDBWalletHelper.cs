
using System;
using System.Linq;
using System.Threading.Tasks;
using System.Text;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using Oci.Common.Model;
using Oci.Common;
using Oci.Common.Auth;
using Oci.DatabaseService;
using Oci.DatabaseService.Models;
using Oci.DatabaseService.Requests;
using Oci.DatabaseService.Responses;


namespace RunSQL
{
    public class GenerateDBWalletHelper
    {

        public static string RandomString(int length)
        {
            const string pool = "abcdefghijklmnopqrstuvwxyz0123456789#%^$@";
            Random random = new Random();
            var chars = Enumerable.Range(0, length)
                .Select(x => pool[random.Next(0, pool.Length)]);
            return new string(chars.ToArray());
        }

        public static string GenerateWalletPassword(int length)
        {
            Random ran = new Random();
            String b = "abcdefghijklmnopqrstuvwxyz0123456789";
            String sc = "!@#$%^&*~";
            String random = "";
            for (int i = 0; i < length; i++)
            {
                int a = ran.Next(b.Length);
                random = random + b.ElementAt(a);
            }
            for (int j = 0; j < 2; j++)
            {
                int sz = ran.Next(sc.Length);
                random = random + sc.ElementAt(sz);
            }
            return random;
        }
        public static async Task<string> GenWallet(DatabaseClient client, string adb_ocid, string extractPath)

        {

            try
            {
                var wallet_password = GenerateWalletPassword(10);

                Console.WriteLine("Inside GenWallet Method");
                var generateAutonomousDatabaseWalletDetails = new Oci.DatabaseService.Models.GenerateAutonomousDatabaseWalletDetails
                {
                    GenerateType = Oci.DatabaseService.Models.GenerateAutonomousDatabaseWalletDetails.GenerateTypeEnum.Single,
                    Password = wallet_password
                };

                var generateAutonomousDatabaseWalletRequest = new Oci.DatabaseService.Requests.GenerateAutonomousDatabaseWalletRequest
                {
                    AutonomousDatabaseId = adb_ocid,
                    GenerateAutonomousDatabaseWalletDetails = generateAutonomousDatabaseWalletDetails,
                };

                var response = await client.GenerateAutonomousDatabaseWallet(generateAutonomousDatabaseWalletRequest);

                using (var memoryStream = new MemoryStream())
                {

                    response.InputStream.CopyTo(memoryStream);
                    Console.WriteLine("Generating zip file...");
                    var fileName = $"gen_wallet.zip";
                    string zipPath = Path.Combine(extractPath + "/" + fileName);
                    Console.WriteLine("Wallet location  : {0}", zipPath);
                    using (var fs = new FileStream(zipPath, FileMode.Create, FileAccess.Write))
                    {
                        memoryStream.WriteTo(fs);
                    }
                    Console.WriteLine("extracting : {0} to {1}", zipPath, extractPath);

                    using (ZipArchive source = ZipFile.Open(zipPath, ZipArchiveMode.Read, null))
                    {
                        foreach (ZipArchiveEntry entry in source.Entries)
                        {
                            string fullPath = Path.GetFullPath(Path.Combine(extractPath, entry.FullName));

                            if (Path.GetFileName(fullPath).Length != 0)
                            {
                                entry.ExtractToFile(fullPath, true);
                            }
                        }
                    }

                }
                return "success";


            }

            catch (OciException ex)
            {
                Console.WriteLine("Unable To Generate wallet  : {0}", ex.Message);
                return "Failed " + ex.Message;
            }

        }


    }
}
