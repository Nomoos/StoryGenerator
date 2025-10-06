using System;
using System.IO;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Setup script to create the required folder structure for StoryGenerator.
    /// Creates folders for organizing artifacts and project outputs by gender and age buckets.
    /// </summary>
    public class SetupFolders
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
        /// Creates the complete folder structure for the StoryGenerator project.
        /// </summary>
        public static void CreateFolderStructure()
        {
            // Get the root directory (parent of CSharp folder)
            string rootDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", ".."));
            int createdCount = 0;

            Console.WriteLine("Creating simple folders...");
            foreach (var folder in SimpleFolders)
            {
                string folderPath = Path.Combine(rootDir, folder);
                Directory.CreateDirectory(folderPath);
                
                // Add .gitkeep to preserve empty directories
                string gitkeepPath = Path.Combine(folderPath, ".gitkeep");
                File.WriteAllText(gitkeepPath, "");
                
                Console.WriteLine($"  ✓ Created: {folder}/");
                createdCount++;
            }

            Console.WriteLine("\nCreating folders with gender and age bucket subdirectories...");
            foreach (var baseFolder in FoldersWithGenderAge)
            {
                foreach (var gender in Genders)
                {
                    foreach (var ageBucket in AgeBuckets)
                    {
                        string folderPath = Path.Combine(rootDir, baseFolder, gender, ageBucket);
                        Directory.CreateDirectory(folderPath);
                        
                        // Add .gitkeep to preserve empty directories
                        string gitkeepPath = Path.Combine(folderPath, ".gitkeep");
                        File.WriteAllText(gitkeepPath, "");
                        
                        Console.WriteLine($"  ✓ Created: {baseFolder}/{gender}/{ageBucket}/");
                        createdCount++;
                    }
                }
            }

            Console.WriteLine("\nCreating research folders...");
            foreach (var category in ResearchCategories)
            {
                string folderPath = Path.Combine(rootDir, "research", category);
                Directory.CreateDirectory(folderPath);
                
                // Add .gitkeep to preserve empty directories
                string gitkeepPath = Path.Combine(folderPath, ".gitkeep");
                File.WriteAllText(gitkeepPath, "");
                
                Console.WriteLine($"  ✓ Created: research/{category}/");
                createdCount++;
            }

            Console.WriteLine($"\n{new string('=', 60)}");
            Console.WriteLine($"✅ Successfully created {createdCount} folder structures!");
            Console.WriteLine($"{new string('=', 60)}");

            // Print summary
            Console.WriteLine("\n📊 Folder Structure Summary:");
            Console.WriteLine($"  - Simple folders: {SimpleFolders.Length}");
            Console.WriteLine($"  - Folders with gender/age buckets: {FoldersWithGenderAge.Length} × {Genders.Length} × {AgeBuckets.Length} = {FoldersWithGenderAge.Length * Genders.Length * AgeBuckets.Length}");
            Console.WriteLine($"  - Research folders: {ResearchCategories.Length}");
            Console.WriteLine($"  - Total: {createdCount} folders");
            Console.WriteLine($"\n📋 Age Buckets: {string.Join(", ", AgeBuckets)}");
        }

        public static void Main(string[] args)
        {
            Console.WriteLine(new string('=', 60));
            Console.WriteLine("StoryGenerator - Folder Structure Setup (C#)");
            Console.WriteLine(new string('=', 60));
            Console.WriteLine();

            try
            {
                CreateFolderStructure();
                Console.WriteLine("\n✨ Setup complete! All folders are ready for use.");
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
