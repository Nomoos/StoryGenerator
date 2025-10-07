using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Verification script to ensure all required folders exist.
    /// </summary>
    public class VerifyFolders
    {
        private static readonly string[] Genders = { "women", "men" };
        private static readonly string[] AgeBuckets = { "10-13", "14-17", "18-23", "24-30" };
        private static readonly string[] ResearchCategories = { "python", "csharp" };

        private static readonly string[] FoldersWithGenderAge = 
        {
            "ideas",
            "topics",
            "titles",
            "scores",
            "scripts/raw_local",
            "scripts/iter_local",
            "scripts/gpt_improved",
            "voices/choice",
            "audio/tts",
            "audio/normalized",
            "subtitles/srt",
            "subtitles/timed",
            "scenes/json",
            "images/keyframes_v1",
            "images/keyframes_v2",
            "videos/ltx",
            "videos/interp",
            "final"
        };

        private static readonly string[] SimpleFolders = { "config" };

        /// <summary>
        /// Verify that all required folders exist.
        /// </summary>
        public static bool VerifyFolderStructure()
        {
            // Get the root directory (parent of CSharp folder)
            string rootDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", ".."));
            
            var missing = new List<string>();
            int found = 0;

            // Check simple folders
            foreach (var folder in SimpleFolders)
            {
                string folderPath = Path.Combine(rootDir, folder);
                if (Directory.Exists(folderPath))
                {
                    found++;
                }
                else
                {
                    missing.Add(folderPath);
                }
            }

            // Check folders with gender and age buckets
            foreach (var baseFolder in FoldersWithGenderAge)
            {
                foreach (var gender in Genders)
                {
                    foreach (var ageBucket in AgeBuckets)
                    {
                        string folderPath = Path.Combine(rootDir, baseFolder, gender, ageBucket);
                        if (Directory.Exists(folderPath))
                        {
                            found++;
                        }
                        else
                        {
                            missing.Add(folderPath);
                        }
                    }
                }
            }

            // Check research folders
            foreach (var category in ResearchCategories)
            {
                string folderPath = Path.Combine(rootDir, "research", category);
                if (Directory.Exists(folderPath))
                {
                    found++;
                }
                else
                {
                    missing.Add(folderPath);
                }
            }

            // Report results
            int total = SimpleFolders.Length + 
                       (FoldersWithGenderAge.Length * Genders.Length * AgeBuckets.Length) + 
                       ResearchCategories.Length;

            Console.WriteLine("Folder Structure Verification");
            Console.WriteLine(new string('=', 60));
            Console.WriteLine($"Expected folders: {total}");
            Console.WriteLine($"Found folders: {found}");
            Console.WriteLine($"Missing folders: {missing.Count}");
            Console.WriteLine();

            if (missing.Any())
            {
                Console.WriteLine("❌ Missing folders:");
                foreach (var folder in missing)
                {
                    Console.WriteLine($"  - {folder}");
                }
                return false;
            }
            else
            {
                Console.WriteLine("✅ All required folders exist!");
                return true;
            }
        }

        public static void Main(string[] args)
        {
            try
            {
                bool success = VerifyFolderStructure();
                Environment.Exit(success ? 0 : 1);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n❌ Error: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
                Environment.Exit(1);
            }
        }
    }
}
