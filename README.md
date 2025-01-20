Whiteboard-of-Thought: Thinking Step-by-Step Across Modalities(https://whiteboard.cs.columbia.edu/ )を参考に、Whiteboard-of-Thoughtを実装しました。

OpenAIのAPIを使用します。以下のコマンドを実行してください。

```bash
export OPENAI_API_KEY="your-api-key"
```
experiment/に移動し、アスキーアートのファイル({name}.txt)をinput/に配置して、以下のコマンドを実行してください。

```bash
python3 main.py {name}
```
direct, CoT, WoTの結果がresult/に保存されます。WoTの生成したコードはcode/に、画像はimage/に保存されます。
