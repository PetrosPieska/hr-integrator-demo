using System;
using System.IO;
using System.Text.Json;
using System.Threading;

class Program
{
    static void Main(string[] args)
    {
        string baseDir = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));
        string sftpDir = Path.Combine(baseDir, "sftp");
        Directory.CreateDirectory(sftpDir);

        string csvPath = Path.Combine(sftpDir, "employees.csv");
        string responsePath = csvPath + ".response.json";

        Console.WriteLine("[Bridge] Writing CSV to: " + csvPath);

        // Kirjoita testidata
        File.WriteAllText(csvPath,
@"id,name,status
1,Matti Meikäläinen,new
2,Maija Mallikas,new");

        Console.WriteLine("[Bridge] CSV written. Waiting for HR B response...");

        // Odota vastausta (max 10 sekuntia)
        int waited = 0;
        while (waited < 10000)
        {
            if (File.Exists(responsePath))
            {
                string json = File.ReadAllText(responsePath);
                Console.WriteLine("[Bridge] Got response:");
                Console.WriteLine(json);
                return;
            }

            Thread.Sleep(1000);
            waited += 1000;
            Console.WriteLine($"[Bridge] Still waiting... {waited / 1000}s");
        }

        Console.WriteLine("[Bridge] Timeout. No response.json found.");
    }
}
