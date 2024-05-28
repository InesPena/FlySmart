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

namespace Company.Function2
{
    public static class CosmosTrigger2
    {
        private const string iotConnectionString = "HostName=iothub-deusto.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=JFIJGmHCl+c6YkyQQcPJts0j0ZQRLon07AIoTGzJ8ek=";
        private const string targetDevice = "smartmeter1";

        [FunctionName("CosmosTrigger2")]
        public static async Task Run([CosmosDBTrigger(
            databaseName: "alarms",
            containerName: "fridge",
            Connection = "comosiot_DOCUMENTDB",
            LeaseContainerName = "leases",
            CreateLeaseContainerIfNotExists = true)]IReadOnlyList<MyDocument2> input,
            ILogger log)
        {
            if (input != null && input.Count > 0)
            {
                log.LogInformation("Documents modified " + input.Count);

                foreach (var doc in input) {
                    log.LogInformation($"Processing new document Id: {doc.id}");
                    await SendCloudToDeviceMessageAsync(doc.averageConsumption);
                }
            }  
        }

        //Mandar comandos
        private async static Task SendCloudToDeviceMessageAsync(float averageConsumption)
        {
            ServiceClient serviceClient = ServiceClient.CreateFromConnectionString(iotConnectionString);

            var commandData = new
            {
                averageConsumption = averageConsumption
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
    public class MyDocument2
    {
        public string id { get; set; }
        public float averageConsumption { get; set; }
    }
}
