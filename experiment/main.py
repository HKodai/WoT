import matplotlib.pyplot as plt
import sys
import re
import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_visualization_code(query, name):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"""
                {query}

                Write Python code with Matplotlib to render the ASCII art as an image.
                Let the main figure be called fig.
                Ensure each character in the input is considered. Remember colors are matplotlib.colors, and colors must be RGB to be displayed. Remember not all rows are necessarily the same length.
                Do NOT produce a final answer to the query until considering the visualization.
                """,
            },
        ],
        temperature=0,
        max_tokens=2048,
        top_p=1,
    )
    # レスポンスからコードを抽出
    code_block = re.search(
        r"```python(.*?)```", response.choices[0].message.content, re.DOTALL
    )
    if code_block:
        code = code_block.group(1).strip()
        with open("code/" + name + ".py", "w") as f:
            f.write(code)
        return code
    else:
        raise ValueError("Code block not found in the response.")


def execute_visualization_code(code, output_file):
    exec_globals = {"plt": plt}  # 必要なライブラリを提供
    exec(code, exec_globals)
    fig = exec_globals.get("fig")
    if fig:
        fig.savefig(output_file, bbox_inches="tight")
        plt.close(fig)
    else:
        raise RuntimeError("Figure not created. Check the generated code.")


def send_visualization_to_model(image_path, query):
    # Read image and convert to base64
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                        },
                    ],
                }
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
        )
    return response.choices[0].message.content


def whiteboard_of_thought(name, ascii):
    python_code = generate_visualization_code(ascii, name)
    # コードを実行して画像を生成
    image_path = "image/" + name + ".png"
    execute_visualization_code(python_code, image_path)
    # 画像をモデルに戻して推論
    result = send_visualization_to_model(
        image_path, "What does this image represent? Output an answer after 'Answer:'"
    )
    return result


def only_text(ascii, cot):
    prompt = f"""
{ascii}
What does this ASCII art represent? Output an answer after 'Answer:'
"""
    if cot:
        prompt += "Let's think step by step."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=2048,
        top_p=1,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    name = sys.argv[1]
    path = "input/" + name + ".txt"
    with open(path, "r") as f:
        ascii_art_prompt = f.read()
    try:
        results = {}
        results["dierct"] = only_text(ascii_art_prompt, False).split("Answer:")[1]
        results["cot"] = only_text(ascii_art_prompt, True).split("Answer:")[1]
        results["wot"] = whiteboard_of_thought(name, ascii_art_prompt).split("Answer:")[
            1
        ]
        with open("result/" + name + ".txt", "w") as f:
            f.write(str(results))
    except Exception as e:
        print(f"An error occurred: {e}")
