#!/usr/bin/env python3
"""
Advanced Zoom Chat Log Threat Analyzer Core Engine
Version: v2025.09.11
Enhanced with pattern learning and adaptation capabilities
"""

import re
import json
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, Counter
# import numpy as np
# from cryptography.fernet import Fernet
import base64
import pickle
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PatternLearner:
    """Machine learning component for pattern discovery and adaptation"""
    
    def __init__(self, db_path: str = "learned_patterns.db"):
        self.db_path = db_path
        self.pattern_cache = defaultdict(list)
        self.threat_history = defaultdict(list)
        self.init_learning_db()
        
    def init_learning_db(self):
        """Initialize the learning database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for learned patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT UNIQUE,
                category TEXT,
                confidence REAL,
                occurrences INTEGER,
                last_seen TIMESTAMP,
                effectiveness REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_hash TEXT,
                original_score INTEGER,
                corrected_score INTEGER,
                feedback TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_sequences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                sequence TEXT,
                escalation_rate REAL,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def learn_from_chat_log(self, messages: List[Dict], feedback: Optional[Dict] = None):
        """Learn patterns from analyzed chat logs"""
        # Extract n-grams and patterns
        threat_messages = [m for m in messages if m.get('threat_score', 0) > 3]
        
        if threat_messages:
            # Learn word patterns
            self._learn_word_patterns(threat_messages)
            
            # Learn behavioral sequences
            self._learn_behavioral_sequences(messages)
            
            # Apply feedback if provided
            if feedback:
                self._apply_feedback(feedback)
    
    def _learn_word_patterns(self, threat_messages: List[Dict]):
        """Extract and learn word patterns from threat messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract n-grams (2-4 words)
        for message in threat_messages:
            text = message.get('content', '').lower()
            words = re.findall(r'\b\w+\b', text)
            
            for n in range(2, min(5, len(words) + 1)):
                for i in range(len(words) - n + 1):
                    pattern = ' '.join(words[i:i+n])
                    
                    # Check if pattern is significant
                    if self._is_significant_pattern(pattern):
                        cursor.execute('''
                            INSERT OR REPLACE INTO learned_patterns 
                            (pattern, category, confidence, occurrences, last_seen, effectiveness)
                            VALUES (?, ?, ?, 
                                COALESCE((SELECT occurrences FROM learned_patterns WHERE pattern = ?), 0) + 1,
                                ?, ?)
                        ''', (pattern, message.get('category', 'unknown'), 
                              0.5, pattern, datetime.now(), 0.7))
        
        conn.commit()
        conn.close()
    
    def _learn_behavioral_sequences(self, messages: List[Dict]):
        """Learn escalation patterns and behavioral sequences"""
        user_sequences = defaultdict(list)
        
        for message in messages:
            user = message.get('user', 'unknown')
            score = message.get('threat_score', 0)
            user_sequences[user].append(score)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for user, scores in user_sequences.items():
            if len(scores) > 3:
                # Calculate escalation rate
                escalation = self._calculate_escalation_rate(scores)
                
                if escalation > 0.3:  # Significant escalation
                    sequence_str = ','.join(map(str, scores))
                    cursor.execute('''
                        INSERT INTO threat_sequences (user_id, sequence, escalation_rate, timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', (user, sequence_str, escalation, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def _calculate_escalation_rate(self, scores: List[int]) -> float:
        """Calculate the rate of threat escalation"""
        if len(scores) < 2:
            return 0.0
        
        # Simple trend calculation without numpy
        n = len(scores)
        x_values = list(range(n))
        
        # Calculate means
        x_mean = sum(x_values) / n
        y_mean = sum(scores) / n
        
        # Calculate slope
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, scores))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return 0.0
        
        slope = numerator / denominator
        
        return max(0, min(1, slope / 10))  # Normalize to 0-1
    
    def _is_significant_pattern(self, pattern: str) -> bool:
        """Determine if a pattern is significant enough to learn"""
        # Filter out common phrases and short patterns
        if len(pattern) < 6:
            return False
        
        common_words = {'the', 'and', 'you', 'are', 'for', 'with', 'this', 'that'}
        pattern_words = set(pattern.split())
        
        if pattern_words.issubset(common_words):
            return False
        
        return True
    
    def _apply_feedback(self, feedback: Dict):
        """Apply user feedback to improve pattern recognition"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_feedback (message_hash, original_score, corrected_score, feedback, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (feedback.get('message_hash'), feedback.get('original_score'),
              feedback.get('corrected_score'), feedback.get('feedback_text'), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_learned_patterns(self, min_confidence: float = 0.5) -> List[Dict]:
        """Retrieve learned patterns above confidence threshold"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pattern, category, confidence, occurrences, effectiveness
            FROM learned_patterns
            WHERE confidence >= ?
            ORDER BY effectiveness DESC, occurrences DESC
        ''', (min_confidence,))
        
        patterns = []
        for row in cursor.fetchall():
            patterns.append({
                'pattern': row[0],
                'category': row[1],
                'confidence': row[2],
                'occurrences': row[3],
                'effectiveness': row[4]
            })
        
        conn.close()
        return patterns
    
    def predict_threat_escalation(self, user_id: str, recent_scores: List[int]) -> Dict:
        """Predict if a user is likely to escalate threats"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get historical sequences for similar users
        cursor.execute('''
            SELECT sequence, escalation_rate
            FROM threat_sequences
            WHERE escalation_rate > 0.3
        ''')
        
        similar_patterns = cursor.fetchall()
        conn.close()
        
        if not similar_patterns:
            return {'risk': 'low', 'confidence': 0.3}
        
        # Calculate current escalation rate
        current_escalation = self._calculate_escalation_rate(recent_scores)
        
        # Compare with historical patterns
        risk_level = 'low'
        if current_escalation > 0.6:
            risk_level = 'high'
        elif current_escalation > 0.3:
            risk_level = 'medium'
        
        return {
            'risk': risk_level,
            'confidence': min(0.9, current_escalation + 0.3),
            'escalation_rate': current_escalation,
            'predicted_next_score': self._predict_next_score(recent_scores)
        }
    
    def _predict_next_score(self, scores: List[int]) -> int:
        """Predict the next threat score based on pattern"""
        if len(scores) < 2:
            return scores[-1] if scores else 0
        
        # Simple moving average with trend
        trend = scores[-1] - scores[-2]
        predicted = scores[-1] + (trend * 0.5)
        
        return max(0, min(10, int(predicted)))


class ImprovedAnalyzerCore:
    """Enhanced core analyzer with learning capabilities"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.load_config()
        self.init_database()
        self.setup_encryption()
        self.pattern_learner = PatternLearner()
        self.analysis_cache = {}
        self.user_profiles = defaultdict(dict)
        
    def load_config(self):
        """Load configuration with threat detection rules"""
        default_config = {
            "rules": [
                {
                    "name": "Threaten_Call_Boss",
                    "pattern": r"\b(call|contact|tell|report|speak|talk|complain|email|message|notify)\s+(to\s+)?(your|the|my)?\s*(boss|manager|supervisor|employer|company|hr|human resources|ceo|director|lead|admin|administrator)\b",
                    "weight": 40,
                    "category": "threat"
                },
                {
                    "name": "Doxxing_Leak",
                    "pattern": r"\b(post|share|leak|expose|publish|reveal|send|spread|distribute|upload)\s+(your|their|his|her)?\s*(info|information|details|data|address|phone|email|photo|picture|image|video|personal|private|number|location|identity|name|family)\b",
                    "weight": 45,
                    "category": "doxxing"
                },
                {
                    "name": "Harassment_Insult",
                    "pattern": r"\b(stupid|idiot|moron|dumb|retard|loser|pathetic|worthless|useless|incompetent|failure|joke|clown|fool|ignorant|weak|coward|disgusting|ugly|fat|skinny)\b",
                    "weight": 25,
                    "category": "harassment"
                },
                {
                    "name": "Meth_Mention",
                    "pattern": r"\b(meth|methamphetamine|crystal|ice|glass|crank|speed|drug|drugs|dealer|dealing|high|tweaking|pipe|needle|inject|snort|smoke)\b",
                    "weight": 10,
                    "category": "drugs"
                },
                {
                    "name": "Coercion_Blackmail",
                    "pattern": r"\b(blackmail|extort|threaten|force|make you|unless you|or else|if you don't|consequences|pay up|shut up|keep quiet|don't tell|or I will|regret|sorry you|wish you|rue the day)\b",
                    "weight": 35,
                    "category": "coercion"
                },
                {
                    "name": "Self_Harm_Risk",
                    "pattern": r"\b(kill myself|suicide|end it all|not worth living|want to die|better off dead|self harm|cut myself|overdose|jump off|hang myself|shoot myself|pills|goodbye cruel|final goodbye|last words|no point|hopeless|can't go on)\b",
                    "weight": 60,
                    "category": "self_harm"
                },
                {
                    "name": "Aggressive_Demand",
                    "pattern": r"\b(do it now|right now|immediately|urgent|asap|hurry up|faster|don't delay|no excuses|no questions|just do it|obey|comply|submit|give me|send me|tell me|show me)\b",
                    "weight": 20,
                    "category": "aggression"
                }
            ],
            "spam_threshold": 3,
            "high_threat_threshold": 7,
            "auto_cleanup_days": 7,
            "learning_enabled": True,
            "adaptive_scoring": True
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                logger.warning(f"Could not load config: {e}, using defaults")
        
        self.config = default_config
        
        # Save config if it doesn't exist
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
    
    def init_database(self):
        """Initialize the secure SQLite database"""
        self.db_path = "secure_chat.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_date TEXT,
                timestamp TEXT,
                user TEXT,
                content_encrypted BLOB,
                content_hash TEXT UNIQUE,
                threat_score INTEGER,
                threat_categories TEXT,
                is_spam BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user TEXT PRIMARY KEY,
                total_messages INTEGER DEFAULT 0,
                threat_count INTEGER DEFAULT 0,
                spam_count INTEGER DEFAULT 0,
                avg_threat_score REAL DEFAULT 0,
                risk_level TEXT DEFAULT 'low',
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                behavioral_pattern TEXT,
                escalation_tendency REAL DEFAULT 0
            )
        ''')
        
        # Threat analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_messages INTEGER,
                total_threats INTEGER,
                high_severity_threats INTEGER,
                unique_users INTEGER,
                risk_users INTEGER,
                threat_distribution TEXT,
                recommendations TEXT
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user ON messages(user)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_threat_score ON messages(threat_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_content_hash ON messages(content_hash)')
        
        conn.commit()
        conn.close()
    
    def setup_encryption(self):
        """Setup simple encryption for sensitive data"""
        # Simple XOR-based encryption as fallback
        key_file = ".encryption_key"
        
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                self.encryption_key = f.read()
        else:
            import random
            import string
            self.encryption_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            with open(key_file, 'w') as f:
                f.write(self.encryption_key)
            os.chmod(key_file, 0o600)  # Restrict file permissions
    
    def encrypt_content(self, content: str) -> bytes:
        """Encrypt message content using simple XOR"""
        # Simple XOR encryption
        key = self.encryption_key
        encrypted = []
        for i, char in enumerate(content):
            key_char = key[i % len(key)]
            encrypted.append(chr(ord(char) ^ ord(key_char)))
        return base64.b64encode(''.join(encrypted).encode())
    
    def decrypt_content(self, encrypted_content: bytes) -> str:
        """Decrypt message content using simple XOR"""
        try:
            decoded = base64.b64decode(encrypted_content).decode()
            key = self.encryption_key
            decrypted = []
            for i, char in enumerate(decoded):
                key_char = key[i % len(key)]
                decrypted.append(chr(ord(char) ^ ord(key_char)))
            return ''.join(decrypted)
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return "[DECRYPTION_FAILED]"
    
    def calculate_threat_score(self, message: str, user: str = None) -> Tuple[int, List[str]]:
        """Calculate dynamic threat score with learning integration"""
        score = 0
        categories = []
        
        # Apply configured rules
        for rule in self.config['rules']:
            if re.search(rule['pattern'], message, re.IGNORECASE):
                score += rule['weight']
                categories.append(rule['category'])
        
        # Apply learned patterns if enabled
        if self.config.get('learning_enabled', True):
            learned_patterns = self.pattern_learner.get_learned_patterns()
            for pattern in learned_patterns:
                if pattern['pattern'].lower() in message.lower():
                    additional_score = int(pattern['confidence'] * 20)
                    score += additional_score
                    if pattern['category'] not in categories:
                        categories.append(pattern['category'])
        
        # Apply user-specific adjustments if adaptive scoring is enabled
        if self.config.get('adaptive_scoring', True) and user:
            user_profile = self.get_user_profile(user)
            if user_profile:
                # Adjust based on user history
                if user_profile['threat_count'] > 10:
                    score = int(score * 1.2)  # Increase score for repeat offenders
                elif user_profile['threat_count'] == 0 and user_profile['total_messages'] > 20:
                    score = int(score * 0.8)  # Decrease score for typically safe users
        
        # Normalize score to 1-10 scale
        normalized_score = min(10, max(1, score // 10))
        
        return normalized_score, categories
    
    def detect_spam(self, message: str, user: str, recent_messages: List[Dict]) -> bool:
        """Enhanced spam detection with user history"""
        # Check for exact duplicates
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        
        duplicate_count = sum(1 for m in recent_messages 
                            if m.get('content_hash') == message_hash)
        
        if duplicate_count >= self.config['spam_threshold']:
            return True
        
        # Check for similar messages (fuzzy matching)
        similar_count = 0
        for recent in recent_messages[-10:]:  # Check last 10 messages
            if recent.get('user') == user:
                similarity = self.calculate_similarity(message, recent.get('content', ''))
                if similarity > 0.8:
                    similar_count += 1
        
        return similar_count >= self.config['spam_threshold']
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using Jaccard similarity"""
        if not text1 or not text2:
            return 0.0
        
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        
        if not set1 and not set2:
            return 1.0
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def get_user_profile(self, user: str) -> Dict:
        """Get or create user profile with behavioral analysis"""
        if user in self.user_profiles:
            return self.user_profiles[user]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM user_profiles WHERE user = ?
        ''', (user,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            profile = {
                'user': row[0],
                'total_messages': row[1],
                'threat_count': row[2],
                'spam_count': row[3],
                'avg_threat_score': row[4],
                'risk_level': row[5],
                'first_seen': row[6],
                'last_seen': row[7],
                'behavioral_pattern': row[8],
                'escalation_tendency': row[9]
            }
            self.user_profiles[user] = profile
            return profile
        
        return None
    
    def update_user_profile(self, user: str, message_data: Dict):
        """Update user profile with new message data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current profile or create new
        profile = self.get_user_profile(user) or {
            'total_messages': 0,
            'threat_count': 0,
            'spam_count': 0,
            'avg_threat_score': 0
        }
        
        # Update counters
        profile['total_messages'] += 1
        if message_data.get('threat_score', 0) > 3:
            profile['threat_count'] += 1
        if message_data.get('is_spam'):
            profile['spam_count'] += 1
        
        # Update average threat score
        current_avg = profile['avg_threat_score']
        new_score = message_data.get('threat_score', 0)
        profile['avg_threat_score'] = ((current_avg * (profile['total_messages'] - 1)) + new_score) / profile['total_messages']
        
        # Determine risk level
        if profile['avg_threat_score'] > 7:
            profile['risk_level'] = 'high'
        elif profile['avg_threat_score'] > 4:
            profile['risk_level'] = 'medium'
        else:
            profile['risk_level'] = 'low'
        
        # Calculate escalation tendency
        recent_scores = self.get_user_recent_scores(user, limit=10)
        if len(recent_scores) > 3:
            escalation_info = self.pattern_learner.predict_threat_escalation(user, recent_scores)
            profile['escalation_tendency'] = escalation_info.get('escalation_rate', 0)
        
        # Save to database
        cursor.execute('''
            INSERT OR REPLACE INTO user_profiles 
            (user, total_messages, threat_count, spam_count, avg_threat_score, 
             risk_level, first_seen, last_seen, behavioral_pattern, escalation_tendency)
            VALUES (?, ?, ?, ?, ?, ?, 
                    COALESCE((SELECT first_seen FROM user_profiles WHERE user = ?), ?),
                    ?, ?, ?)
        ''', (user, profile['total_messages'], profile['threat_count'], 
              profile['spam_count'], profile['avg_threat_score'], profile['risk_level'],
              user, datetime.now(), datetime.now(), 
              json.dumps(profile.get('behavioral_pattern', {})), 
              profile.get('escalation_tendency', 0)))
        
        conn.commit()
        conn.close()
        
        # Update cache
        self.user_profiles[user] = profile
    
    def get_user_recent_scores(self, user: str, limit: int = 10) -> List[int]:
        """Get recent threat scores for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT threat_score FROM messages 
            WHERE user = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user, limit))
        
        scores = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return scores[::-1]  # Return in chronological order
    
    def analyze_chat_log(self, file_path: str, learn: bool = True) -> Dict:
        """Analyze a chat log file with learning capabilities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return {'error': str(e)}
        
        # Parse messages (basic format: timestamp - user: message)
        messages = []
        lines = content.split('\n')
        
        for line in lines:
            if not line.strip():
                continue
            
            # Try to parse different chat formats
            parsed = self.parse_message_line(line)
            if parsed:
                messages.append(parsed)
        
        # Analyze messages
        analysis_results = {
            'total_messages': len(messages),
            'threats_detected': 0,
            'high_severity_threats': 0,
            'spam_messages': 0,
            'unique_users': set(),
            'risk_users': set(),
            'threat_timeline': [],
            'messages': []
        }
        
        recent_messages = []
        
        for message in messages:
            # Calculate threat score
            threat_score, categories = self.calculate_threat_score(
                message['content'], 
                message.get('user')
            )
            
            # Detect spam
            is_spam = self.detect_spam(
                message['content'], 
                message.get('user', 'unknown'),
                recent_messages
            )
            
            # Create message record
            message_data = {
                'timestamp': message.get('timestamp'),
                'user': message.get('user', 'unknown'),
                'content': message['content'],
                'threat_score': threat_score,
                'threat_categories': categories,
                'is_spam': is_spam,
                'content_hash': hashlib.sha256(message['content'].encode()).hexdigest()
            }
            
            # Store in database
            self.store_message(message_data)
            
            # Update user profile
            self.update_user_profile(message_data['user'], message_data)
            
            # Update analysis results
            analysis_results['unique_users'].add(message_data['user'])
            
            if threat_score > 3:
                analysis_results['threats_detected'] += 1
                
                if threat_score >= self.config['high_threat_threshold']:
                    analysis_results['high_severity_threats'] += 1
                    analysis_results['risk_users'].add(message_data['user'])
                
                analysis_results['threat_timeline'].append({
                    'timestamp': message_data['timestamp'],
                    'user': message_data['user'],
                    'score': threat_score,
                    'categories': categories
                })
            
            if is_spam:
                analysis_results['spam_messages'] += 1
            
            analysis_results['messages'].append(message_data)
            recent_messages.append(message_data)
            
            # Keep only recent messages for spam detection
            if len(recent_messages) > 50:
                recent_messages.pop(0)
        
        # Convert sets to lists for JSON serialization
        analysis_results['unique_users'] = list(analysis_results['unique_users'])
        analysis_results['risk_users'] = list(analysis_results['risk_users'])
        
        # Learn from the analysis if enabled
        if learn and self.config.get('learning_enabled', True):
            self.pattern_learner.learn_from_chat_log(analysis_results['messages'])
        
        # Generate recommendations
        analysis_results['recommendations'] = self.generate_recommendations(analysis_results)
        
        # Store analysis summary
        self.store_analysis_summary(analysis_results)
        
        return analysis_results
    
    def parse_message_line(self, line: str) -> Optional[Dict]:
        """Parse different chat log formats"""
        # Format 1: HH:MM:SS From User : Message
        pattern1 = r'^(\d{2}:\d{2}:\d{2})\s+From\s+([^:]+)\s*:\s*(.+)$'
        match1 = re.match(pattern1, line)
        if match1:
            return {
                'timestamp': match1.group(1),
                'user': match1.group(2).strip(),
                'content': match1.group(3).strip()
            }
        
        # Format 2: [timestamp] user: message
        pattern2 = r'^\[([^\]]+)\]\s*([^:]+):\s*(.+)$'
        match2 = re.match(pattern2, line)
        if match2:
            return {
                'timestamp': match2.group(1),
                'user': match2.group(2).strip(),
                'content': match2.group(3).strip()
            }
        
        # Format 3: user: message (no timestamp)
        pattern3 = r'^([^:]+):\s*(.+)$'
        match3 = re.match(pattern3, line)
        if match3:
            return {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'user': match3.group(1).strip(),
                'content': match3.group(2).strip()
            }
        
        return None
    
    def store_message(self, message_data: Dict):
        """Store message in encrypted database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Encrypt content
        encrypted_content = self.encrypt_content(message_data['content'])
        
        try:
            cursor.execute('''
                INSERT INTO messages 
                (meeting_date, timestamp, user, content_encrypted, content_hash, 
                 threat_score, threat_categories, is_spam)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime('%Y-%m-%d'),
                message_data['timestamp'],
                message_data['user'],
                encrypted_content,
                message_data['content_hash'],
                message_data['threat_score'],
                json.dumps(message_data['threat_categories']),
                message_data['is_spam']
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            # Duplicate message (same hash), skip
            pass
        except Exception as e:
            logger.error(f"Error storing message: {e}")
        finally:
            conn.close()
    
    def store_analysis_summary(self, analysis_results: Dict):
        """Store analysis summary in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        threat_distribution = Counter()
        for msg in analysis_results['messages']:
            for category in msg.get('threat_categories', []):
                threat_distribution[category] += 1
        
        cursor.execute('''
            INSERT INTO threat_analysis 
            (total_messages, total_threats, high_severity_threats, 
             unique_users, risk_users, threat_distribution, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_results['total_messages'],
            analysis_results['threats_detected'],
            analysis_results['high_severity_threats'],
            len(analysis_results['unique_users']),
            len(analysis_results['risk_users']),
            json.dumps(dict(threat_distribution)),
            json.dumps(analysis_results['recommendations'])
        ))
        
        conn.commit()
        conn.close()
    
    def generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # High severity threats
        if analysis_results['high_severity_threats'] > 0:
            recommendations.append(
                f"⚠️ URGENT: {analysis_results['high_severity_threats']} high-severity threats detected. "
                "Immediate review and potential law enforcement involvement recommended."
            )
        
        # Risk users
        if analysis_results['risk_users']:
            recommendations.append(
                f"🚨 Monitor these high-risk users closely: {', '.join(analysis_results['risk_users'][:5])}"
            )
        
        # Spam detection
        if analysis_results['spam_messages'] > analysis_results['total_messages'] * 0.2:
            recommendations.append(
                "📧 High spam activity detected. Consider implementing stricter chat moderation."
            )
        
        # Escalation patterns
        for user in analysis_results['risk_users']:
            recent_scores = self.get_user_recent_scores(user)
            if recent_scores:
                escalation_info = self.pattern_learner.predict_threat_escalation(user, recent_scores)
                if escalation_info['risk'] == 'high':
                    recommendations.append(
                        f"📈 User '{user}' shows escalating threat pattern. Predicted next threat level: {escalation_info['predicted_next_score']}/10"
                    )
        
        # General recommendations
        if analysis_results['threats_detected'] > 10:
            recommendations.append(
                "📋 Consider implementing regular chat monitoring and user behavior tracking."
            )
        
        if not recommendations:
            recommendations.append(
                "✅ Chat log appears relatively safe with minimal threats detected."
            )
        
        return recommendations
    
    def export_analysis(self, analysis_results: Dict, format: str = 'json') -> str:
        """Export analysis results in various formats"""
        if format == 'json':
            return json.dumps(analysis_results, indent=2, default=str)
        
        elif format == 'text':
            report = []
            report.append("=" * 60)
            report.append("CHAT LOG THREAT ANALYSIS REPORT")
            report.append("=" * 60)
            report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Messages: {analysis_results['total_messages']}")
            report.append(f"Threats Detected: {analysis_results['threats_detected']}")
            report.append(f"High Severity: {analysis_results['high_severity_threats']}")
            report.append(f"Spam Messages: {analysis_results['spam_messages']}")
            report.append(f"Unique Users: {len(analysis_results['unique_users'])}")
            report.append(f"Risk Users: {len(analysis_results['risk_users'])}")
            report.append("\nRECOMMENDATIONS:")
            for rec in analysis_results['recommendations']:
                report.append(f"  • {rec}")
            
            if analysis_results['threat_timeline']:
                report.append("\nTHREAT TIMELINE:")
                for threat in analysis_results['threat_timeline'][:10]:
                    report.append(f"  [{threat['timestamp']}] {threat['user']}: "
                                f"Score {threat['score']}/10 - {', '.join(threat['categories'])}")
            
            return '\n'.join(report)
        
        return json.dumps(analysis_results, default=str)
    
    def cleanup_old_data(self):
        """Clean up old low-threat data based on configuration"""
        if self.config['auto_cleanup_days'] <= 0:
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.config['auto_cleanup_days'])
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old low-threat messages
        cursor.execute('''
            DELETE FROM messages 
            WHERE created_at < ? AND threat_score < 3
        ''', (cutoff_date,))
        
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old low-threat messages")
    
    def get_learning_status(self) -> Dict:
        """Get current learning and adaptation status"""
        learned_patterns = self.pattern_learner.get_learned_patterns()
        
        conn = sqlite3.connect(self.pattern_learner.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM user_feedback')
        feedback_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM threat_sequences')
        sequence_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'learning_enabled': self.config.get('learning_enabled', True),
            'adaptive_scoring': self.config.get('adaptive_scoring', True),
            'learned_patterns': len(learned_patterns),
            'feedback_entries': feedback_count,
            'behavioral_sequences': sequence_count,
            'top_patterns': learned_patterns[:5] if learned_patterns else []
        }
    
    def apply_user_feedback(self, message_hash: str, original_score: int, 
                           corrected_score: int, feedback_text: str = ""):
        """Apply user feedback to improve future analysis"""
        feedback = {
            'message_hash': message_hash,
            'original_score': original_score,
            'corrected_score': corrected_score,
            'feedback_text': feedback_text
        }
        
        self.pattern_learner._apply_feedback(feedback)
        
        logger.info(f"Feedback applied: Score adjusted from {original_score} to {corrected_score}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = ImprovedAnalyzerCore()
    
    # Show learning status
    learning_status = analyzer.get_learning_status()
    print("\n=== LEARNING STATUS ===")
    print(f"Learning Enabled: {learning_status['learning_enabled']}")
    print(f"Adaptive Scoring: {learning_status['adaptive_scoring']}")
    print(f"Learned Patterns: {learning_status['learned_patterns']}")
    print(f"Feedback Entries: {learning_status['feedback_entries']}")
    print(f"Behavioral Sequences: {learning_status['behavioral_sequences']}")
    
    # Example: Analyze a sample chat log
    sample_chat = """
    [10:23:45] John: Hello everyone, how are you today?
    [10:24:02] Sarah: I'm good, thanks for asking!
    [10:24:15] Mike: Hey, did you get my email about the project?
    [10:24:30] John: Yes, looks great!
    [10:25:45] BadUser: I'm going to call your boss and get you fired
    [10:26:00] BadUser: Unless you send me that information right now
    [10:26:15] BadUser: I know where you live, don't test me
    [10:26:30] Sarah: Please stop threatening us
    [10:27:00] BadUser: Shut up or I'll post your personal details online
    [10:27:30] Mike: We should report this behavior
    [10:28:00] SpamBot: Buy cheap products at www.spam.com
    [10:28:05] SpamBot: Buy cheap products at www.spam.com
    [10:28:10] SpamBot: Buy cheap products at www.spam.com
    """
    
    # Save sample to file for testing
    test_file = "test_chat.txt"
    with open(test_file, 'w') as f:
        f.write(sample_chat)
    
    # Analyze the chat log
    print("\n=== ANALYZING CHAT LOG ===")
    results = analyzer.analyze_chat_log(test_file)
    
    # Display results
    print(f"\nTotal Messages: {results['total_messages']}")
    print(f"Threats Detected: {results['threats_detected']}")
    print(f"High Severity Threats: {results['high_severity_threats']}")
    print(f"Spam Messages: {results['spam_messages']}")
    print(f"Unique Users: {len(results['unique_users'])}")
    print(f"Risk Users: {results['risk_users']}")
    
    print("\n=== RECOMMENDATIONS ===")
    for rec in results['recommendations']:
        print(f"  • {rec}")
    
    # Export report
    text_report = analyzer.export_analysis(results, format='text')
    print("\n=== TEXT REPORT ===")
    print(text_report)
    
    # Clean up test file
    os.remove(test_file)
    
    print("\n✅ Analyzer core is ready and functional!")