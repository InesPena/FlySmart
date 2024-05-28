// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

// This application uses the Azure IoT Hub device SDK for .NET
// For samples see: https://github.com/Azure/azure-iot-sdk-csharp/tree/master/iothub/device/samples

using System;
using Microsoft.Azure.Devices.Client;
using Newtonsoft.Json;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.IO;
using Microsoft.Azure.Devices.Shared;
using Newtonsoft.Json.Linq;
using System.Linq;

namespace simulatedDevice
{
    class SimulatedDevice
    {
        private static DeviceClient s_deviceClient;

        // The device connection string to authenticate the device with your IoT hub.
        private const string s_connectionString = "HostName=iothub-deusto.azure-devices.net;DeviceId=dev-group-1;SharedAccessKey=fws5qMb9nde69WKr6wOuAO3eGMIEZ4zSG3xQ39LCHCs=";
        
        private static async void ReceiveC2dAsync()
        {
            Console.WriteLine("\nReceiving cloud to device messages from service");
            while (true)
            {
                Twin twin = await s_deviceClient.GetTwinAsync().ConfigureAwait(false);
                var jsonContent = twin.ToJson();
                List<string> desiredProperties = ReadDesiredVariablesFromJson(jsonContent);

                Message receivedMessage = await s_deviceClient.ReceiveAsync();
                if (receivedMessage == null) continue;
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("Received message: {0}",
                Encoding.ASCII.GetString(receivedMessage.GetBytes()));
                Console.ResetColor();

                await s_deviceClient.CompleteAsync(receivedMessage);
            }
        }
        static List<string> ReadDesiredVariablesFromJson(string jsonContent)
        {
            try
            {
                List<string> desiredVariables = new List<string>();
                // Parsear el JSON
                JObject jsonObject = JObject.Parse(jsonContent);
                dynamic jsonObj = JsonConvert.DeserializeObject(jsonObject.ToString());
                var desiredProperties = jsonObj["properties"]["desired"];
                Console.WriteLine(desiredProperties["frecuency"]);
                if (desiredProperties["frecuency"] != null) {
                    desiredVariables.Add(desiredProperties.GetValue("frecuency").ToString());
                } else {
                    Console.WriteLine("la propiedad frecuency no existe");
                }
                if (desiredProperties["reducir_consumo"] != null) {
                    desiredVariables.Add(desiredProperties.GetValue("reducir_consumo").ToString());
                } else {
                    Console.WriteLine("la propiedad reducir_consumo no existe");
                }
                for (int i = 0; i < desiredVariables.Count(); i++) {
                    Console.WriteLine(desiredVariables[i]);
                }

                // Crear un array para almacenar las variables deseadas

                return desiredVariables;
            }
            catch (Exception ex)
            {
                // Manejar cualquier error que pueda ocurrir al leer el archivo
                Console.WriteLine($"Error al leer el archivo JSON: {ex.Message}");
                return null;
            }
        }
        static void UpdateTwin(string jsonContent, List<string> desiredProperties) {
            JObject jsonObject = JObject.Parse(jsonContent);
            dynamic jsonObj = JsonConvert.DeserializeObject(jsonObject.ToString());
            jsonObj["properties"]["desired"].put("frecuency", desiredProperties[0]);
            jsonObj["properties"]["desired"].put("reducir_consumo", desiredProperties[1]);
            TwinCollection updatedTwin = new TwinCollection(jsonObj);
            s_deviceClient.UpdateReportedPropertiesAsync(updatedTwin);
        }

        private static void Main()
        {
            Console.WriteLine("IoT Hub Quickstarts - Simulated device. Ctrl-C to exit.\n");

            // Connect to the IoT hub using the MQTT protocol
            s_deviceClient = DeviceClient.CreateFromConnectionString(s_connectionString, TransportType.Mqtt);
            ReceiveC2dAsync();
            Console.ReadLine();
        }
    }
}
