from Generators.GStoryIdeas import StoryIdeasGenerator

generator = StoryIdeasGenerator()

refined_story_topics = [
    "pretending you're okay with casual when you're secretly catching feelings",
    "falling for someone who gives mixed signals you keep trying to decode",
    "finding out your friend group had a secret chat — without you",
    "falling in love with a story that mirrors something you haven’t told anyone",
    "crying over a book that feels like your real life",
    "pretending to be someone else just to fit in",
    "trying to live a perfect lifestyle until it doesn’t feel like you anymore",
    "learning the difference between attraction and connection — the hard way",
    "realizing beauty doesn’t always mean confidence",
    "watching your opinion go viral — and not knowing how to feel about it",
    "living like it’s 2005 and discovering who you really are",
    "being intimate for the first time — and not knowing what you're supposed to feel",
    "spending your savings trying to look like an influencer",
    "turning your routine into a performance without meaning to",
    "falling in love with books that change how you see yourself",
    "wondering if the aesthetic you're chasing is really your own",
    "using fashion to express who you really are",
    "debating adults online and finding your own voice",
    "chasing beauty trends that weren’t made for people your age",
    "learning your favorite creator wasn’t who you thought — and neither were you",
    "getting noticed for asking the questions no one else does",
    "realizing your first serious relationship doesn't feel like love anymore",
    "creating your identity from thrift finds and eyeliner",
    "feeling like you stand out just by showing up as yourself",
    "dressing like a kid to feel like yourself again",
    "letting go of the perfection you thought would make you happy",
    "being underestimated because you look too soft to be strong",
    "finding a clever loophole that lets you bend the rules",
    "giving up your smartphone to feel more like yourself",
    "using outdated trends to stand out in a modern world"
]

viral_mixed_tones_us_teens = [
    "witty, chaotic, emotional",             # highest relatability, meme-friendly, and emotionally charged
    "awkward, romantic, relatable",          # teen crush energy + vulnerability = viral gold
    "relatable, awkward, heartwarming",      # cringe + sweet = very shareable and duet-able
    "dramatic, aesthetic, cinematic",        # popular for storytime edits and dreamy monologues
    "soft, dreamy, empowering"               # emotionally rich but slightly lower engagement velocity
]

viral_story_themes_us_teens = [
    "secret crushes, awkward moments, unexpected confessions",     # highly relatable, perfect for POVs and skits
    "mixed signals, dreamy moments, when everything changed",      # emotional romance confusion = high engagement
    "feeling left out, friendship drama, finding your real people",# universal pain + redemption arc
    "first love, quiet sadness, learning to let go",               # soft heartbreak + coming-of-age tension
    "real life vs online filters, breaking free from perfection",  # deep + trending in aesthetic-focused formats
    "double lives, secret accounts, who you are online vs IRL",    # identity and duality = very Gen Z/Alpha
    "quiet pressure, feeling overwhelmed, finding balance again",  # mental health angle, platform-safe
    "friendship tests, choosing kindness, staying true to yourself",# betrayal without toxicity = safe + emotional
    "new confidence, small wins, telling your side of the story",  # glow-up with quiet payoff
    "shy girls, big thoughts, speaking up when it matters"         # empowering but slightly slower viral pickup
]


for tone in viral_mixed_tones_us_teens:
    for theme in viral_story_themes_us_teens:
        for topic in refined_story_topics:

            print("📌 Evaluating combination:")
            print(f"   📝 Topic: {topic}")
            print(f"   🎭 Tone: {tone}")
            print(f"   🎯 Theme: {theme}\n")

            ideas = generator.generate_ideas(
                topic=topic,
                count=5,
                tone=tone,
                theme=theme
            )

            for idea in ideas:
                print(f"- {idea.story_title} (potencial: {idea.potencial})")
            print(f"\n✅ {len(ideas)} ideas generated and saved. For topic {topic}\n")
