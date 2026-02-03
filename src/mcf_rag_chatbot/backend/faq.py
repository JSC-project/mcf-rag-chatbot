# FAQ - Handels question logging and retrival

import json
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import List, Dict



class FAQHandler:

    #Default questions if no history exists
    DEFAULT_QUESTIONS = [
        "Hur mycket kontanter bör jag ha hemma?",
        "Checklista på saker att ha hemma i kris eller krig",
        "Hur mycket mat och vatten bör jag ha hemma?",
        "Får jag tar med mig mitt husdjur till ett skyddsrum?"
    ]

    def __init__(self, log_file_path: Path):

        self.log_file_path = log_file_path
        self.ensure_log_file_exists()


    def ensure_log_file_exists(self):
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file_path.exists():
            self.save_questions_data({"questions": []})

    
    def load_questions_data(self) -> Dict:
        #Load questions data from Json file
        try:
            with open(self.log_file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Misslyckades att ladda frågor: {e}")
            return {"questions": []}

    def save_questions_data(self, data: Dict):
        #Saves questions to JSON file

        try:
            with open(self.log_file_path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"misslyckades att spara frågan: {e}")

        
    def log_question(self, question: str):
        #Logs the question to track frequency
        try:
            question_data = self.load_questions_data()

            #Add new question with timestamp
            question_data["questions"].append({
                "question": question,
                "timestamp": datetime.now().isoformat()
            })

            self.save_questions_data(question_data)
        except Exception as e:
            print(f"Fel vid loggning av frågan: {e}")

    
    def get_top_questions(self, n: int = 6) -> List[str]:
        #Get top most asked quetstions (6)
        try: 
            questions_data = self.load_questions_data()

            #if no questions logged, return defaults
            if not questions_data["questions"]:
                return self.DEFAULT_QUESTIONS[:n]
            
            #count question frequency
            all_questions = [item["question"] for item in questions_data["questions"]]
            question_counts = Counter(all_questions)

            #Get top most common
            top_questions = [q for q, count in question_counts.most_common(n)]

            #if we don´t have enough questions yet, fill with defaults
            if len(top_questions) < n:
                for default in self.DEFAULT_QUESTIONS:
                    if default not in top_questions and len(top_questions) < n:
                        top_questions.append(default)
            return top_questions[:n]
        
        except Exception as e:
            print(f"Fel att hämta top frågor: {e}")
            return self.DEFAULT_QUESTIONS[:n]
        
    def get_statistics(self) -> Dict:
        #Get statitics about logged questions
        #Returns: total_questions = Total number of questions asked, unique_questions = number of unique questions asked, most_common = List of (question, count) touple of top 5
        try: 
            questions_data = self.load_questions_data()
            all_questions = [item["question"] for item in questions_data["questions"]]

            return {
                "total_questions": len(all_questions),
                "unique_questions": len(set(all_questions)),
                "most_common": Counter(all_questions).most_common(5)
            }
        except Exception as e:
            print("Fel vid hämtning av statistik: {e}")
            return {
                "total_questions": 0,
                "unique_questions": 0,
                "most_common": []
            }

