import sys
import os
import uvicorn

# Inject the agent directory into path
agent_path = os.path.abspath('../Kinetifi-agent')
sys.path.append(agent_path)

if __name__ == "__main__":
    # Change CWD to agent path so it loads its own .env and files
    os.chdir(agent_path)
    
    from main import app
    print(f"Starting KinetiFi Agent from {agent_path}...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
