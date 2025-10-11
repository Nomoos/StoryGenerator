namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Checkpoint for pipeline state management
/// Allows resuming pipeline from last successful step
/// </summary>
public class PipelineCheckpoint
{
    public Dictionary<string, bool> CompletedSteps { get; set; } = new();
    public Dictionary<string, string> StepData { get; set; } = new();
    public DateTime LastUpdated { get; set; } = DateTime.Now;

    public bool IsStepComplete(string stepName)
    {
        if (string.IsNullOrWhiteSpace(stepName))
        {
            throw new ArgumentException("Step name cannot be empty", nameof(stepName));
        }

        return CompletedSteps.ContainsKey(stepName) && CompletedSteps[stepName];
    }

    public void CompleteStep(string stepName, string? data = null)
    {
        if (string.IsNullOrWhiteSpace(stepName))
        {
            throw new ArgumentException("Step name cannot be empty", nameof(stepName));
        }

        CompletedSteps[stepName] = true;
        if (data != null)
        {
            StepData[stepName] = data;
        }
        LastUpdated = DateTime.Now;
    }

    public string? GetStepData(string stepName)
    {
        if (string.IsNullOrWhiteSpace(stepName))
        {
            throw new ArgumentException("Step name cannot be empty", nameof(stepName));
        }

        return StepData.ContainsKey(stepName) ? StepData[stepName] : null;
    }
}
