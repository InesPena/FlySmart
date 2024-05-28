using System;
using System.Collections.Generic;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Devices;
using Newtonsoft.Json;
using System.Text;
using System.Threading.Tasks;

namespace Company.Function1
{
    public static class CosmosTrigger1
    {
        private const string iotConnectionString = "HostName=iothub-deusto.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=JFIJGmHCl+c6YkyQQcPJts0j0ZQRLon07AIoTGzJ8ek=";
        private const string targetDevice = "smartmeter1";

        [FunctionName("CosmosTrigger1")]
        public static async Task Run([CosmosDBTrigger(
            databaseName: "alarms",
            containerName: "temperature",
            Connection = "comosiot_DOCUMENTDB",
            LeaseContainerName = "leases",
            CreateLeaseContainerIfNotExists = true)]IReadOnlyList<MyDocument1> input,
            ILogger log)
        {
            if (input != null && input.Count > 0)
            {
                log.LogInformation("Documents modified " + input.Count);

                foreach (var doc in input) {
                    log.LogInformation($"Processing new document Id: {doc.id}");
                    await SendCloudToDeviceMessageAsync(doc.typeAlarm, doc.furnace1Fixed, doc.furnace2Fixed);
                }
            }  
        }

        //Mandar comandos
        private async static Task SendCloudToDeviceMessageAsync(string typeAlarm, float furnace1Fixed, float furnace2Fixed)
        {
            ServiceClient serviceClient = ServiceClient.CreateFromConnectionString(iotConnectionString);

            var commandData = new
            {
                typeAlarm = typeAlarm,
                furnace1Fixed = furnace1Fixed,
                furnace2Fixed = furnace2Fixed
            };

            string jsonMessage = JsonConvert.SerializeObject(commandData);

            var commandMessage = new Message(Encoding.UTF8.GetBytes(jsonMessage))
            {
            ContentType = "application/json", 
            ContentEncoding = "utf-8" 
            };

            await serviceClient.SendAsync(targetDevice, commandMessage);
        }
    }

    // Customize the model with your own desired properties
    public class MyDocument1
    {
        public string id { get; set; }
        public float temperature { get; set; }
        public string typeAlarm { get; set; }
        public float furnace1Fixed { get; set; }
        public float furnace2Fixed { get; set; }
    }
}
