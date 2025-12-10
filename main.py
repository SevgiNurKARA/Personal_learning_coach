import argparse
import json
from agents.orchestrator_agent import OrchestratorAgent
from tools.google_search import GoogleSearchTool
from memory.memory_bank import MemoryBank


def run_demo():
    """Run a demonstration of the learning coach system."""
    memory = MemoryBank()
    search_tool = GoogleSearchTool()
    orchestrator = OrchestratorAgent(search_tool=search_tool, memory_service=memory)

    # Load demo input
    with open("examples/demo_input.json", "r", encoding="utf-8") as f:
        demo = json.load(f)

    print("=" * 50)
    print("🚀 Running initial flow with demo input...")
    print("=" * 50)
    
    out = orchestrator.run_initial_flow(demo)
    print("\n📋 Profile:")
    print(json.dumps(out["profile"], ensure_ascii=False, indent=2))
    print("\n📅 Plan:")
    print(json.dumps(out["plan"], ensure_ascii=False, indent=2))

    # Simulate day report
    print("\n" + "=" * 50)
    print("📊 Simulating daily cycle with day_report -> next plan")
    print("=" * 50)
    
    day_report = {
        "day": 1,
        "completed_tasks": 3,
        "perceived_difficulty": 3,
        "quiz_score": 80
    }
    
    out2 = orchestrator.run_daily_cycle(user_id="demo_user", day_report=day_report)
    print("\n✅ Evaluation:")
    print(json.dumps(out2["evaluation"], ensure_ascii=False, indent=2))
    print("\n📅 Next Plan:")
    print(json.dumps(out2["next_plan"], ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 50)
    print("✨ Demo completed successfully!")
    print("=" * 50)
    
    return orchestrator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AI-Powered Personal Learning Coach")
    parser.add_argument("--demo", action="store_true", help="Run a local demonstration")
    args = parser.parse_args()
    
    if args.demo:
        orchestrator = run_demo()
    else:
        print("Run with --demo to run a local demonstration.")
        print("Example: python main.py --demo")
