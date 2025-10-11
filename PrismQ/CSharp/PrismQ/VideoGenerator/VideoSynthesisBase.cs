using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace PrismQ.VideoGenerator
{
    /// <summary>
    /// Base class for video synthesis implementations providing common functionality
    /// </summary>
    public abstract class VideoSynthesisBase
    {
        protected readonly string PythonPath;
        
        protected VideoSynthesisBase(string pythonPath = "python")
        {
            PythonPath = pythonPath;
        }
        
        /// <summary>
        /// Execute Python script and return success status
        /// </summary>
        protected async Task<bool> ExecutePythonScriptAsync(
            string script,
            Action<string>? outputHandler = null,
            Action<string>? errorHandler = null)
        {
            // Save script to temporary file
            string tempScript = Path.Combine(
                Path.GetTempPath(),
                $"video_synthesis_{Guid.NewGuid()}.py");
            
            await File.WriteAllTextAsync(tempScript, script);
            
            try
            {
                var processInfo = new ProcessStartInfo
                {
                    FileName = PythonPath,
                    Arguments = tempScript,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                
                using var process = Process.Start(processInfo);
                if (process == null)
                {
                    Console.WriteLine("❌ Failed to start Python process");
                    return false;
                }
                
                // Read output asynchronously
                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();
                
                await process.WaitForExitAsync();
                
                string output = await outputTask;
                string error = await errorTask;
                
                // Handle output
                if (!string.IsNullOrEmpty(output))
                {
                    if (outputHandler != null)
                        outputHandler(output);
                    else
                        Console.WriteLine(output);
                }
                
                // Handle errors
                if (!string.IsNullOrEmpty(error))
                {
                    if (errorHandler != null)
                        errorHandler(error);
                    else if (process.ExitCode != 0)
                        Console.WriteLine($"Python stderr: {error}");
                }
                
                return process.ExitCode == 0;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error executing Python script: {ex.Message}");
                return false;
            }
            finally
            {
                // Cleanup temporary script
                if (File.Exists(tempScript))
                {
                    try { File.Delete(tempScript); }
                    catch { /* Ignore cleanup errors */ }
                }
            }
        }
        
        /// <summary>
        /// Validate that required files exist
        /// </summary>
        protected bool ValidateFile(string path, string description)
        {
            if (string.IsNullOrEmpty(path))
            {
                Console.WriteLine($"❌ {description} path is empty");
                return false;
            }
            
            if (!File.Exists(path))
            {
                Console.WriteLine($"❌ {description} not found: {path}");
                return false;
            }
            
            return true;
        }
        
        /// <summary>
        /// Validate output directory exists or create it
        /// </summary>
        protected bool EnsureOutputDirectory(string outputPath)
        {
            try
            {
                string? directory = Path.GetDirectoryName(outputPath);
                if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
                {
                    Directory.CreateDirectory(directory);
                }
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Failed to create output directory: {ex.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Escape string for use in Python script
        /// </summary>
        protected string EscapePythonString(string input)
        {
            if (string.IsNullOrEmpty(input))
                return string.Empty;
            
            return input
                .Replace("\\", "\\\\")
                .Replace("'", "\\'")
                .Replace("\"", "\\\"")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r");
        }
        
        /// <summary>
        /// Format path for cross-platform compatibility
        /// </summary>
        protected string NormalizePath(string path)
        {
            if (string.IsNullOrEmpty(path))
                return string.Empty;
            
            return Path.GetFullPath(path).Replace("\\", "/");
        }
    }
}
