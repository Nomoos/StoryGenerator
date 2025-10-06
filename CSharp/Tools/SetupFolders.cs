using System;
using System.IO;
using System.Collections.Generic;
using System.Text.Json;
using System.Linq;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Audience configuration model
    /// </summary>
    public class AudienceConfig
    {
        public class GenderPreference
        {
            public string name { get; set; }
            public int preference_percentage { get; set; }
        }

        public class CountryPreference
        {
            public string name { get; set; }
            public int preference_percentage { get; set; }
        }

        public class AgeGroupPreference
        {
            public string range { get; set; }
            public double preference_percentage { get; set; }
        }

        public class AudienceData
        {
            public List<GenderPreference> genders { get; set; }
            public List<CountryPreference> countries { get; set; }
            public List<AgeGroupPreference> age_groups { get; set; }
        }

        public class FolderStructureData
        {
            public List<string> content_folders { get; set; }
            public List<string> script_folders { get; set; }
            public List<string> voice_folders { get; set; }
            public List<string> audio_folders { get; set; }
            public List<string> subtitle_folders { get; set; }
            public List<string> scene_folders { get; set; }
            public List<string> image_folders { get; set; }
            public List<string> video_folders { get; set; }
            public List<string> final_folders { get; set; }
            public List<string> research_folders { get; set; }
            public List<string> simple_folders { get; set; }
        }

        public AudienceData audience { get; set; }
        public FolderStructureData folder_structure { get; set; }
    }

    /// <summary>
    /// Setup script to create the required folder structure for StoryGenerator.
    /// Creates folders for organizing artifacts and project outputs based on configuration.
    /// Supports configurable audience demographics (gender, age, country) with preference percentages.
    /// </summary>
    public class SetupFolders
    {
        /// <summary>
        /// Load audience configuration from JSON file
        /// </summary>
        /// <param name="configPath">Path to configuration file. If null, uses default.</param>
        /// <returns>Parsed configuration</returns>
        public static AudienceConfig LoadConfig(string configPath = null)
        {
            if (configPath == null)
            {
                // Default config path
                string rootDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", ".."));
                configPath = Path.Combine(rootDir, "config", "audience_config.json");
            }

            try
            {
                string jsonContent = File.ReadAllText(configPath);
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                return JsonSerializer.Deserialize<AudienceConfig>(jsonContent, options);
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine($"❌ Config file not found: {configPath}");
                Console.WriteLine("Creating default configuration...");
                return CreateDefaultConfig();
            }
            catch (JsonException ex)
            {
                Console.WriteLine($"❌ Error parsing config file: {ex.Message}");
                Environment.Exit(1);
                return null;
            }
        }

        /// <summary>
        /// Create a default configuration if none exists
        /// </summary>
        private static AudienceConfig CreateDefaultConfig()
        {
            return new AudienceConfig
            {
                audience = new AudienceConfig.AudienceData
                {
                    genders = new List<AudienceConfig.GenderPreference>
                    {
                        new AudienceConfig.GenderPreference { name = "men", preference_percentage = 50 },
                        new AudienceConfig.GenderPreference { name = "women", preference_percentage = 50 }
                    },
                    countries = new List<AudienceConfig.CountryPreference>
                    {
                        new AudienceConfig.CountryPreference { name = "US", preference_percentage = 100 }
                    },
                    age_groups = new List<AudienceConfig.AgeGroupPreference>
                    {
                        new AudienceConfig.AgeGroupPreference { range = "10-14", preference_percentage = 10 },
                        new AudienceConfig.AgeGroupPreference { range = "15-19", preference_percentage = 20 },
                        new AudienceConfig.AgeGroupPreference { range = "20-24", preference_percentage = 30 },
                        new AudienceConfig.AgeGroupPreference { range = "25-29", preference_percentage = 25 },
                        new AudienceConfig.AgeGroupPreference { range = "30-34", preference_percentage = 15 }
                    }
                },
                folder_structure = new AudienceConfig.FolderStructureData
                {
                    content_folders = new List<string> { "ideas", "topics", "titles", "scores" },
                    script_folders = new List<string> { "scripts/raw_local" },
                    simple_folders = new List<string> { "config" }
                }
            };
        }

        /// <summary>
        /// Creates the complete folder structure for the StoryGenerator project based on configuration.
        /// </summary>
        /// <param name="configPath">Optional path to configuration JSON file</param>
        public static void CreateFolderStructure(string configPath = null)
        {
            // Load configuration
            var config = LoadConfig(configPath);

            // Get the root directory (parent of CSharp folder)
            string rootDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", ".."));
            int createdCount = 0;

            // Extract audience configuration
            var genders = config.audience.genders.Select(g => g.name).ToList();
            var ageGroups = config.audience.age_groups.Select(a => a.range).ToList();
            var countries = config.audience.countries.Select(c => c.name).ToList();

            // Extract folder structure configuration
            var foldersWithGenderAge = new List<string>();
            if (config.folder_structure.content_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.content_folders);
            if (config.folder_structure.script_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.script_folders);
            if (config.folder_structure.voice_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.voice_folders);
            if (config.folder_structure.audio_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.audio_folders);
            if (config.folder_structure.subtitle_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.subtitle_folders);
            if (config.folder_structure.scene_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.scene_folders);
            if (config.folder_structure.image_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.image_folders);
            if (config.folder_structure.video_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.video_folders);
            if (config.folder_structure.final_folders != null)
                foldersWithGenderAge.AddRange(config.folder_structure.final_folders);

            var researchFolders = config.folder_structure.research_folders ?? new List<string>();
            var simpleFolders = config.folder_structure.simple_folders ?? new List<string>();

            Console.WriteLine("Creating simple folders...");
            foreach (var folder in simpleFolders)
            {
                string folderPath = Path.Combine(rootDir, folder);
                Directory.CreateDirectory(folderPath);

                // Add .gitkeep to preserve empty directories
                string gitkeepPath = Path.Combine(folderPath, ".gitkeep");
                File.WriteAllText(gitkeepPath, "");

                Console.WriteLine($"  ✓ Created: {folder}/");
                createdCount++;
            }

            Console.WriteLine("\nCreating folders with gender and age group subdirectories...");
            foreach (var baseFolder in foldersWithGenderAge)
            {
                foreach (var gender in genders)
                {
                    foreach (var ageGroup in ageGroups)
                    {
                        string folderPath = Path.Combine(rootDir, baseFolder, gender, ageGroup);
                        Directory.CreateDirectory(folderPath);

                        // Add .gitkeep to preserve empty directories
                        string gitkeepPath = Path.Combine(folderPath, ".gitkeep");
                        File.WriteAllText(gitkeepPath, "");

                        Console.WriteLine($"  ✓ Created: {baseFolder}/{gender}/{ageGroup}/");
                        createdCount++;
                    }
                }
            }

            Console.WriteLine("\nCreating research folders...");
            foreach (var researchFolder in researchFolders)
            {
                string folderPath = Path.Combine(rootDir, researchFolder);
                Directory.CreateDirectory(folderPath);

                // Add .gitkeep to preserve empty directories
                string gitkeepPath = Path.Combine(folderPath, ".gitkeep");
                File.WriteAllText(gitkeepPath, "");

                Console.WriteLine($"  ✓ Created: {researchFolder}/");
                createdCount++;
            }

            Console.WriteLine($"\n{new string('=', 60)}");
            Console.WriteLine($"✅ Successfully created {createdCount} folder structures!");
            Console.WriteLine($"{new string('=', 60)}");

            // Print summary
            Console.WriteLine("\n📊 Folder Structure Summary:");
            Console.WriteLine($"  - Simple folders: {simpleFolders.Count}");
            Console.WriteLine($"  - Folders with gender/age structure: {foldersWithGenderAge.Count} × {genders.Count} × {ageGroups.Count} = {foldersWithGenderAge.Count * genders.Count * ageGroups.Count}");
            Console.WriteLine($"  - Research folders: {researchFolders.Count}");
            Console.WriteLine($"  - Total: {createdCount} folders");
            Console.WriteLine($"\n📋 Configuration:");
            Console.WriteLine($"  - Genders: {string.Join(", ", genders)}");
            Console.WriteLine($"  - Age Groups: {string.Join(", ", ageGroups)}");
            Console.WriteLine($"  - Countries: {string.Join(", ", countries)}");
        }

        public static void Main(string[] args)
        {
            Console.WriteLine(new string('=', 60));
            Console.WriteLine("StoryGenerator - Folder Structure Setup (C#)");
            Console.WriteLine(new string('=', 60));
            Console.WriteLine();

            try
            {
                // Check for config file argument
                string configPath = null;
                if (args.Length > 0)
                {
                    configPath = args[0];
                    Console.WriteLine($"Using config file: {configPath}\n");
                }

                CreateFolderStructure(configPath);
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
