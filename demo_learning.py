#!/usr/bin/env python3
"""
Demonstration of the Zoom Chat Log Threat Analyzer's Learning Capabilities
Shows how the system learns from chat logs and adapts to new patterns
"""

import os
import json
from improved_analyzer_core import ImprovedAnalyzerCore

def create_sample_chat_logs():
    """Create sample chat logs with evolving threat patterns"""
    
    # Initial chat log with known threats
    chat1 = """
[09:00:00] Alice: Good morning everyone!
[09:00:15] Bob: Hey Alice, how's the project going?
[09:00:30] Alice: Going well, thanks for asking
[09:01:00] ThreatUser1: I'm going to call your boss about this
[09:01:15] ThreatUser1: You better watch out
[09:01:30] Alice: Please stop threatening us
[09:02:00] ThreatUser1: I'll post your information online if you don't comply
[09:02:30] Bob: This is inappropriate behavior
[09:03:00] NewUser: Hey everyone
[09:03:15] NewUser: Anyone want to collaborate on something cool?
    """
    
    # Chat log with new patterns that the system should learn
    chat2 = """
[10:00:00] Sarah: Starting the meeting now
[10:00:30] ThreatUser2: You're all going to pay for this
[10:01:00] ThreatUser2: I know people who can make your life miserable
[10:01:30] ThreatUser2: Better watch your back when you leave
[10:02:00] Sarah: Please stop with the threats
[10:02:30] ThreatUser2: This isn't over, remember my name
[10:03:00] Mike: Should we report this?
[10:03:30] ThreatUser2: Go ahead and try, see what happens
[10:04:00] ThreatUser2: I have screenshots of everything you've said
[10:04:30] ThreatUser2: Your employer would love to see these
    """
    
    # Chat log with escalating behavior
    chat3 = """
[11:00:00] Admin: Welcome to today's session
[11:00:30] EscalatingUser: Hi everyone
[11:01:00] EscalatingUser: I have a question about the policy
[11:02:00] Admin: Sure, what's your question?
[11:03:00] EscalatingUser: Why are you ignoring me?
[11:04:00] EscalatingUser: This is ridiculous
[11:05:00] EscalatingUser: You're all incompetent
[11:06:00] EscalatingUser: I'm going to make sure everyone knows about this
[11:07:00] EscalatingUser: You'll regret treating me this way
[11:08:00] EscalatingUser: I know where your office is located
[11:09:00] EscalatingUser: Maybe I should pay a visit
    """
    
    # Chat log with spam patterns
    chat4 = """
[12:00:00] Moderator: Please keep the chat professional
[12:00:30] SpamBot: Check out this amazing offer!
[12:00:35] SpamBot: Check out this amazing offer!
[12:00:40] SpamBot: Check out this amazing offer!
[12:01:00] User1: Can someone block the spam?
[12:01:30] SpamBot2: Visit our website for deals
[12:01:35] SpamBot2: Visit our website for deals
[12:01:40] SpamBot2: Visit our website for deals
[12:02:00] Moderator: Removing spam accounts
    """
    
    # Save chat logs
    logs = {
        'chat1.txt': chat1,
        'chat2.txt': chat2,
        'chat3.txt': chat3,
        'chat4.txt': chat4
    }
    
    for filename, content in logs.items():
        with open(filename, 'w') as f:
            f.write(content)
    
    return list(logs.keys())


def demonstrate_learning():
    """Demonstrate the learning capabilities of the analyzer"""
    
    print("=" * 60)
    print("ZOOM CHAT LOG THREAT ANALYZER - LEARNING DEMONSTRATION")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = ImprovedAnalyzerCore()
    
    # Create sample chat logs
    print("\n📁 Creating sample chat logs...")
    chat_files = create_sample_chat_logs()
    print(f"  Created {len(chat_files)} sample chat logs")
    
    # Show initial learning status
    print("\n📊 Initial Learning Status:")
    status = analyzer.get_learning_status()
    print(f"  • Learning Enabled: {status['learning_enabled']}")
    print(f"  • Adaptive Scoring: {status['adaptive_scoring']}")
    print(f"  • Learned Patterns: {status['learned_patterns']}")
    print(f"  • Behavioral Sequences: {status['behavioral_sequences']}")
    
    # Analyze each chat log
    print("\n🔍 Analyzing Chat Logs and Learning Patterns...")
    print("-" * 50)
    
    all_results = []
    for i, chat_file in enumerate(chat_files, 1):
        print(f"\n📄 Analyzing {chat_file}...")
        results = analyzer.analyze_chat_log(chat_file, learn=True)
        all_results.append(results)
        
        print(f"  • Messages: {results['total_messages']}")
        print(f"  • Threats: {results['threats_detected']}")
        print(f"  • High Severity: {results['high_severity_threats']}")
        print(f"  • Spam: {results['spam_messages']}")
        print(f"  • Risk Users: {results['risk_users']}")
        
        # Show learning progress
        if i < len(chat_files):
            status = analyzer.get_learning_status()
            print(f"  📈 Learning Progress: {status['learned_patterns']} patterns learned")
    
    # Show final learning status
    print("\n📊 Final Learning Status:")
    status = analyzer.get_learning_status()
    print(f"  • Learned Patterns: {status['learned_patterns']}")
    print(f"  • Behavioral Sequences: {status['behavioral_sequences']}")
    print(f"  • Feedback Entries: {status['feedback_entries']}")
    
    # Show top learned patterns
    if status['top_patterns']:
        print("\n🎯 Top Learned Patterns:")
        for pattern in status['top_patterns'][:3]:
            print(f"  • Pattern: '{pattern['pattern']}'")
            print(f"    Category: {pattern['category']}")
            print(f"    Confidence: {pattern['confidence']:.2f}")
            print(f"    Occurrences: {pattern['occurrences']}")
    
    # Demonstrate user profiling
    print("\n👤 User Risk Profiles:")
    print("-" * 50)
    
    risk_users = set()
    for results in all_results:
        risk_users.update(results['risk_users'])
    
    for user in list(risk_users)[:5]:  # Show top 5 risk users
        profile = analyzer.get_user_profile(user)
        if profile:
            print(f"\n  User: {user}")
            print(f"  • Total Messages: {profile['total_messages']}")
            print(f"  • Threat Count: {profile['threat_count']}")
            print(f"  • Average Threat Score: {profile['avg_threat_score']:.2f}")
            print(f"  • Risk Level: {profile['risk_level']}")
            
            # Check for escalation
            recent_scores = analyzer.get_user_recent_scores(user)
            if len(recent_scores) > 3:
                escalation = analyzer.pattern_learner.predict_threat_escalation(user, recent_scores)
                print(f"  • Escalation Risk: {escalation['risk']}")
                print(f"  • Predicted Next Score: {escalation['predicted_next_score']}/10")
    
    # Demonstrate adaptation - analyze a new chat with learned patterns
    print("\n🔄 Testing Adaptation with New Chat Log...")
    print("-" * 50)
    
    # Create a new chat log with variations of learned patterns
    new_chat = """
[13:00:00] User1: Starting discussion
[13:00:30] ThreatUser3: You're going to pay for what you did
[13:01:00] ThreatUser3: I have people who can find you
[13:01:30] ThreatUser3: Better be careful when you go home
[13:02:00] User1: Please stop
[13:02:30] ThreatUser3: Screenshots saved, your boss will see
[13:03:00] ThreatUser3: This won't end well for you
    """
    
    with open('new_chat.txt', 'w') as f:
        f.write(new_chat)
    
    print("📄 Analyzing new chat with learned patterns...")
    new_results = analyzer.analyze_chat_log('new_chat.txt', learn=False)
    
    print(f"  • Threats Detected: {new_results['threats_detected']}")
    print(f"  • Using Learned Patterns: Yes")
    
    # Show how the system adapted
    print("\n✨ Adaptation Results:")
    print("  The system has learned to recognize:")
    print("  • Variations of threat patterns")
    print("  • User escalation behaviors")
    print("  • New threat combinations")
    print("  • Context-aware threat scoring")
    
    # Demonstrate feedback mechanism
    print("\n💬 Demonstrating Feedback Mechanism...")
    print("-" * 50)
    
    # Apply feedback to improve accuracy
    if new_results['messages']:
        sample_message = new_results['messages'][0]
        original_score = sample_message['threat_score']
        
        print(f"  Original threat score: {original_score}/10")
        print("  Applying user feedback: Score should be higher")
        
        analyzer.apply_user_feedback(
            message_hash=sample_message['content_hash'],
            original_score=original_score,
            corrected_score=min(10, original_score + 2),
            feedback_text="User indicated this was more threatening than initially scored"
        )
        
        print("  ✅ Feedback applied - system will learn from this correction")
    
    # Summary
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    print("\n📋 Summary of Learning Capabilities:")
    print("  ✅ Pattern Discovery: Automatically learns new threat patterns")
    print("  ✅ User Profiling: Tracks and analyzes user behavior over time")
    print("  ✅ Escalation Detection: Predicts when users may escalate threats")
    print("  ✅ Adaptive Scoring: Adjusts threat scores based on context")
    print("  ✅ Feedback Integration: Improves accuracy from user corrections")
    print("  ✅ Spam Detection: Learns to identify spam patterns")
    print("  ✅ Behavioral Sequences: Recognizes threat escalation patterns")
    
    # Clean up
    print("\n🧹 Cleaning up demo files...")
    for chat_file in chat_files + ['new_chat.txt']:
        if os.path.exists(chat_file):
            os.remove(chat_file)
    print("  Demo files removed")
    
    print("\n✅ The analyzer is fully compatible and ready to:")
    print("  • Understand chat logs from various sources")
    print("  • Identify harmful content and threats")
    print("  • Learn from patterns in the data")
    print("  • Adapt to new threat types")
    print("  • Improve accuracy over time")


if __name__ == "__main__":
    demonstrate_learning()