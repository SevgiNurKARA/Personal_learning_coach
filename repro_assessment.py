
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Windows encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

from agents.assessment_agent import get_assessment_agent

def test_questions():
    print("🚀 Testing Assessment Agent...")
    try:
        agent = get_assessment_agent()
        print(f"Agent initialized: {agent}")
        
        goal = "Python Learning"
        print(f"Generating questions for: {goal}")
        
        questions = agent.get_assessment_questions(goal, 5)
        
        print(f"Returned type: {type(questions)}")
        print(f"Question count: {len(questions) if questions else 0}")
        
        if questions:
            print("sample question:", questions[0])
        else:
            print("❌ No questions returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_questions()
