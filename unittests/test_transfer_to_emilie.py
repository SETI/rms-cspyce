import os

import cspyce as cs

"""
Nothing to see here for now
"""

import subprocess
import sys
import textwrap
from pathlib import Path

def test_prompt(tmp_path):
    prompt = 'PROMPT: '
    user_input = "My User Input"
    path = Path(__file__).parent.parent  # root directory
    script_file = tmp_path / "script.py"
    script = f"""
        import sys
        sys.path.insert(0, "{path}")  # Make sure we get the correct cspyce
        import cspyce as cs
        text = cs.prompt("{prompt}")
        print(text, end='', file=sys.stderr)
    """
    with open(script_file, "w") as file:
        file.write(textwrap.dedent(script))

    result = subprocess.run([sys.executable, script_file],
                            input=user_input + "\n", text=True,
                            capture_output=True)
    assert result.stderr == user_input  # Contains the prompt
    assert result.stdout == prompt

