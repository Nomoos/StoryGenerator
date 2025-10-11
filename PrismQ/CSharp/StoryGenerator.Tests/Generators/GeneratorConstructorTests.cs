using Xunit;
using PrismQ.IdeaScraper;
using PrismQ.StoryGenerator;
using PrismQ.SubtitleGenerator;
using PrismQ.VoiceOverGenerator;
using PrismQ.Shared.Interfaces;

namespace StoryGenerator.Tests.Generators;

/// <summary>
/// Basic tests to verify all generator implementations compile and have correct properties.
/// </summary>
public class GeneratorConstructorTests
{
    [Fact]
    public void IdeaGenerator_HasCorrectInterface()
    {
        // Verify IdeaGenerator implements IIdeaGenerator
        Assert.True(typeof(IIdeaGenerator).IsAssignableFrom(typeof(IdeaGenerator)));
        Assert.True(typeof(IGenerator).IsAssignableFrom(typeof(IdeaGenerator)));
    }

    [Fact]
    public void ScriptGenerator_HasCorrectInterface()
    {
        // Verify ScriptGenerator implements IScriptGenerator
        Assert.True(typeof(IScriptGenerator).IsAssignableFrom(typeof(ScriptGenerator)));
        Assert.True(typeof(IGenerator).IsAssignableFrom(typeof(ScriptGenerator)));
    }

    [Fact]
    public void RevisionGenerator_HasCorrectInterface()
    {
        // Verify RevisionGenerator implements IRevisionGenerator
        Assert.True(typeof(IRevisionGenerator).IsAssignableFrom(typeof(RevisionGenerator)));
        Assert.True(typeof(IGenerator).IsAssignableFrom(typeof(RevisionGenerator)));
    }

    [Fact]
    public void EnhancementGenerator_HasCorrectInterface()
    {
        // Verify EnhancementGenerator implements IEnhancementGenerator
        Assert.True(typeof(IEnhancementGenerator).IsAssignableFrom(typeof(EnhancementGenerator)));
        Assert.True(typeof(IGenerator).IsAssignableFrom(typeof(EnhancementGenerator)));
    }

    [Fact]
    public void VoiceGenerator_HasCorrectInterface()
    {
        // Verify VoiceGenerator implements IVoiceGenerator
        Assert.True(typeof(IVoiceGenerator).IsAssignableFrom(typeof(VoiceGenerator)));
        Assert.True(typeof(IGenerator).IsAssignableFrom(typeof(VoiceGenerator)));
    }

    [Fact]
    public void SubtitleGenerator_HasCorrectInterface()
    {
        // Verify SubtitleGenerator implements ISubtitleGenerator
        Assert.True(typeof(ISubtitleGenerator).IsAssignableFrom(typeof(SubtitleGenerator)));
        Assert.True(typeof(IGenerator).IsAssignableFrom(typeof(SubtitleGenerator)));
    }

    [Fact]
    public void AllGenerators_HaveRequiredInterfaces()
    {
        // Verify all generators implement IGenerator
        var generatorTypes = new[]
        {
            typeof(IdeaGenerator),
            typeof(ScriptGenerator),
            typeof(RevisionGenerator),
            typeof(EnhancementGenerator),
            typeof(VoiceGenerator),
            typeof(SubtitleGenerator)
        };

        foreach (var type in generatorTypes)
        {
            Assert.True(typeof(IGenerator).IsAssignableFrom(type), 
                $"{type.Name} should implement IGenerator");
        }
    }
}
