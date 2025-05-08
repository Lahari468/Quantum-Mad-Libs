import random
import time
import json
from datetime import datetime
import os

class QuantumMadLibs:
    def __init__(self):
        self.story_history = []
        self.players = []
        self.current_player_idx = 0
        self.scores = {}
        self.custom_stories = []
        self.themes = {
            'light': {'text': '⚪', 'bg': ''},
            'dark': {'text': '⚫', 'bg': ''},
            'rainbow': {'text': '🌈', 'bg': ''}
        }
        self.current_theme = 'light'
        self.achievements = {}
        self.load_data()

        # Enhanced story templates
        self.story_categories = {
            'quantum': [
                ("The {adjective} Quantum {noun}", "In a parallel universe, {name} discovered how to {verb} {adverb} using quantum {noun}."),
                ("{hero}'s Quantum Leap", "Using a {adjective} quantum device, {hero} learned to {verb} through {noun} {adverb}.")
            ],
            'cyberpunk': [
                ("Neon {noun}", "In 2{number}, the {adjective} hacker {name} had to {verb} {adverb} to crack the {noun} mainframe."),
                ("{villain}'s Algorithm", "The AI {villain} created a {adjective} algorithm that could {verb} {adverb} across the net.")
            ],
            'mythology': [
                ("The {noun} of {place}", "When the {adjective} gods decided to {verb} {adverb}, {hero} intervened with a magical {noun}."),
                ("Curse of the {noun}", "The ancient {noun} made everyone {verb} {adverb} until {hero} broke the {adjective} spell.")
            ],
            'custom': []
        }

    def clear_screen(self):
        """Clear console output"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def apply_theme(self, text):
        """Apply visual theme to text"""
        if self.current_theme == 'dark':
            return f"\033[30m\033[47m{text}\033[0m"
        elif self.current_theme == 'rainbow':
            colors = ['\033[31m', '\033[33m', '\033[32m', '\033[36m', '\033[34m', '\033[35m']
            return ''.join(f"{colors[i%len(colors)]}{char}" for i, char in enumerate(text)) + '\033[0m'
        return text

    def typewriter(self, text, delay=0.03):
        """Print text with typewriter effect"""
        for char in self.apply_theme(text):
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def setup_players(self):
        """Set up players for the game"""
        self.clear_screen()
        
        while True:
            try:
                num_players = int(input("How many quantum players? (1-5): "))
                if 1 <= num_players <= 5:
                    break
                print("Please enter between 1-5 players")
            except ValueError:
                print("Please enter a number")

        for i in range(num_players):
            name = input(f"Enter quantum designation for Player {i+1}: ").strip()
            while not name:
                print("Designation cannot be void!")
                name = input(f"Enter quantum designation for Player {i+1}: ").strip()
            
            if "quantum" in name.lower():
                self.unlock_achievement("Quantum Entangled", "Used 'quantum' in player name")
            
            self.players.append(name)
            self.scores[name] = 0

    def select_theme(self):
        """Select visual theme for the game"""
        self.clear_screen()
        print("\nSelect Quantum Interface Theme:")
        for i, (theme, data) in enumerate(self.themes.items(), 1):
            print(f"{i}. {theme.capitalize()} {data['text']}")

        while True:
            choice = input("\nChoose theme (1-3): ")
            try:
                if 1 <= int(choice) <= 3:
                    self.current_theme = list(self.themes.keys())[int(choice)-1]
                    self.unlock_achievement("Theme Master", "Changed interface theme")
                    break
            except ValueError:
                pass
            print("Invalid choice. Try again.")

    def select_story(self):
        """Select story category and template"""
        self.clear_screen()
        
        print("\nQuantum Story Categories:")
        categories = list(self.story_categories.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.capitalize()}")
        print(f"{len(categories)+1}. Create New Story")

        while True:
            choice = input("\nSelect category (1-5): ")
            if choice == str(len(categories)+1):
                return self.create_story()
            try:
                if 1 <= int(choice) <= len(categories):
                    category = categories[int(choice)-1]
                    if category == 'custom':
                        if not self.custom_stories:
                            print("No custom stories in the quantum void yet!")
                            time.sleep(1)
                            continue
                        return random.choice(self.custom_stories)
                    return random.choice(self.story_categories[category])
            except (ValueError, KeyError):
                pass
            print("Invalid quantum choice. Try again.")

    def create_story(self):
        """Create and save custom story"""
        self.clear_screen()
        
        print("\n✍️ Quantum Story Generator ✍️")
        title = input("\nEnter story title: ").strip()
        while not title:
            print("Title cannot be quantum void!")
            title = input("Enter story title: ").strip()

        print("\nWrite your story with quantum placeholders like {noun}, {verb}, etc.")
        print("Example: The {adjective} quantum {noun} {verb} {adverb}.")
        template = input("\nStory template: ").strip()
        
        while not template or '{' not in template or '}' not in template:
            print("Template must contain quantum placeholders like {noun}!")
            template = input("Story template: ").strip()

        new_story = (title, template)
        self.custom_stories.append(new_story)
        self.save_data()
        
        self.unlock_achievement("Story Weaver", "Created a custom story")
        print("\nStory saved in quantum memory!")
        time.sleep(1)
        return new_story

    def get_word_input(self, word_type, player):
        """Get word input with validation"""
        hints = {
            'noun': 'quantum object',
            'verb': 'quantum action',
            'adjective': 'quantum descriptor',
            'adverb': 'quantum manner (-ly)',
            'name': "quantum being",
            'place': 'quantum location',
            'number': 'quantum integer',
            'hero': "quantum hero",
            'villain': "quantum villain"
        }

        self.clear_screen()
        
        print(f"\n{player}'s quantum turn!")
        hint = hints.get(word_type, 'quantum word')
        
        # Quantum fluctuation easter egg
        if random.random() < 0.1:
            print("Quantum fluctuation detected! Try 'entanglement'")

        while True:
            word = input(f"Enter a quantum {word_type} ({hint}): ").strip()
            if not word:
                print("Quantum void not allowed!")
                continue
                
            if word_type == 'number' and not word.isdigit():
                print("Please enter a quantum integer")
                continue
                
            if word.lower() == 'entanglement':
                self.unlock_achievement("Quantum Physicist", "Used 'entanglement' in a story")
                
            return word

    def play_round(self):
        """Play one round of Quantum Mad Libs"""
        title, template = self.select_story()
        
        # Get unique word types
        word_types = sorted(list(set(
            word[1:-1] for word in template.split() 
            if word.startswith('{') and word.endswith('}')
        )))
        
        words = {}
        for word_type in word_types:
            player = self.players[self.current_player_idx]
            word = self.get_word_input(word_type, player)
            words[f"{{{word_type}}}"] = word
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

        # Generate story
        story = template
        for placeholder, word in words.items():
            story = story.replace(placeholder, word)

        full_story = f"{title}\n\n{story}"
        self.story_history.append((datetime.now().strftime("%Y-%m-%d %H:%M"), full_story))

        # Score the story
        self.score_story(full_story)

        # Display results
        self.clear_screen()
        print("\n🌟 Quantum Story Result 🌟\n")
        self.typewriter(full_story)
        
        print("\n🎉 Quantum entanglement complete! 🎉")
        self.show_scores()
        input("\nPress Enter to continue quantum play...")

    def score_story(self, story):
        """Calculate and award quantum points"""
        score = min(100, len(story) // 2)
        winner = self.players[self.current_player_idx]
        
        if "quantum" in story.lower():
            score += 30
            print("\nQUANTUM BONUS +30 POINTS! ⚛️")
            time.sleep(1)
        
        if "entanglement" in story.lower():
            score += 50
            print("\nQUANTUM ENTANGLEMENT DETECTED! +50 POINTS! ⚛️")
            time.sleep(1)
        
        self.scores[winner] += score

    def show_scores(self):
        """Display current quantum scores"""
        print("\n🏆 Quantum Scores 🏆")
        for name, score in sorted(self.scores.items(), key=lambda x: -x[1]):
            print(f"{name}: {score} qubits")

    def show_history(self):
        """Display quantum story history"""
        self.clear_screen()
        
        if not self.story_history:
            print("\nNo quantum stories generated yet!")
            input("\nPress Enter to continue...")
            return

        print("\n📜 Quantum History 📜")
        for i, (date, story) in enumerate(self.story_history, 1):
            print(f"\n#{i} - {date}")
            print("-" * 50)
            print(story)

        input("\nPress Enter to quantum continue...")

    def show_achievements(self):
        """Display unlocked achievements"""
        self.clear_screen()
        
        if not self.achievements:
            print("\nNo quantum achievements unlocked yet!")
        else:
            print("\n🏅 Quantum Achievements 🏅")
            for name, (desc, date) in self.achievements.items():
                print(f"\n{name}: {desc}")
                print(f"Unlocked: {date}")

        input("\nPress Enter to return to quantum menu...")

    def unlock_achievement(self, name, description):
        """Unlock a new achievement"""
        if name not in self.achievements:
            self.achievements[name] = (description, datetime.now().strftime("%Y-%m-%d %H:%M"))
            print(f"\n⚡ Achievement Unlocked: {name}! ⚡")
            time.sleep(1.5)

    def save_data(self):
        """Save quantum game data"""
        data = {
            'scores': self.scores,
            'custom_stories': self.custom_stories,
            'history': self.story_history,
            'achievements': self.achievements,
            'theme': self.current_theme
        }
        try:
            if 'REPLIT_DB_URL' in os.environ:
                import replit
                replit.db['quantum_madlibs'] = json.dumps(data)
            else:
                with open('quantum_madlibs.json', 'w') as f:
                    json.dump(data, f)
        except Exception as e:
            print(f"Quantum storage error: {e}")

    def load_data(self):
        """Load quantum game data"""
        try:
            if 'REPLIT_DB_URL' in os.environ:
                import replit
                data = json.loads(replit.db['quantum_madlibs'])
            else:
                try:
                    with open('quantum_madlibs.json', 'r') as f:
                        data = json.load(f)
                except FileNotFoundError:
                    data = {}
            
            self.scores = data.get('scores', {})
            self.custom_stories = data.get('custom_stories', [])
            self.story_history = data.get('history', [])
            self.achievements = data.get('achievements', {})
            self.current_theme = data.get('theme', 'light')
        except Exception as e:
            print(f"Quantum retrieval error: {e}")

    def main_menu(self):
        """Main quantum menu"""
        self.select_theme()
        while True:
            self.clear_screen()
            
            print("\nQuantum Interface:")
            print("1. New Quantum Game")
            print("2. Continue Quantum Game" if self.players else "2. Continue (quantum void)")
            print("3. Quantum History")
            print("4. Quantum Story Creator")
            print("5. Quantum Achievements")
            print("6. Quit Quantum Realm")

            choice = input("\nEnter quantum choice (1-6): ")

            if choice == '1':
                self.setup_players()
                while True:
                    self.play_round()
                    again = input("\nContinue quantum play? (y/n): ").lower()
                    if again != 'y':
                        break
            elif choice == '2':
                if not self.players:
                    print("\nQuantum void detected! Start new game.")
                    time.sleep(1)
                else:
                    while True:
                        self.play_round()
                        again = input("\nContinue quantum play? (y/n): ").lower()
                        if again != 'y':
                            break
            elif choice == '3':
                self.show_history()
            elif choice == '4':
                self.create_story()
            elif choice == '5':
                self.show_achievements()
            elif choice == '6':
                print("\nExiting quantum realm... Goodbye! ⚛️")
                self.save_data()
                break
            else:
                print("\nQuantum error. Try again.")
                time.sleep(1)

if __name__ == "__main__":
    game = QuantumMadLibs()
    game.main_menu()