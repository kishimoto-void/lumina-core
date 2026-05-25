# 🌟 LuminaCORE v6.2

**Production-Ready & Hybrid-Ready 多層感情エンジン**

キャラクターAIのための、物理モデルベースの感情シミュレーションエンジンです。  
ピアノの弦の共鳴にインスパイアされた独自アーキテクチャで、喜怒哀楽を静的なフラグではなく**動的に振動する物理量**として扱います。

---

## 🎯 概要

LuminaCORE は、LLM（大規模言語モデル）へ渡すプロンプトを**感情状態に応じてリアルタイムに生成・最適化**するコプロセッサです。  
ゲーム・VTuber・会話AIなど、感情豊かなキャラクターが必要なあらゆる場面で活用できます。

---

## ✨ 主な特徴

- **🎹 ピアノ弦物理モデル**  
  感情を「弦の張力」として表現。短期・長期の慣性や残響を再現し、感情の余韻・積み重ねをシミュレート。

- **🧠 5層アーキテクチャ**  
  設定層 → 本能/理性層 → 感情検出層 → 観測値層 → プロンプト生成層、と責務を明確に分離。

- **💡 ハイブリッド感情検出**  
  現在はキーワードマッチング方式。将来的に sentence-transformers 等のベクトル類似度との統合スロットを用意済み。

- **📊 データ駆動型複合精神状態判定**  
  「ツンデレ」「見捨てられ不安」「純情な高揚感」など10種類以上の複合状態を、優先度付きルールレジストリで判定。

- **💞 関係性ステートマシン**  
  他人 → 顔見知り → 友達 → 恋人 → 深い恋、など8ステージを好感度・信頼度・嫉妬心によって動的に遷移。

- **🎭 嫉妬スタイル分岐**  
  嫉妬心の発動時に「甘える・試す・皮肉・フリーズ」の4スタイルを感情圧力の複合評価で自動選択。

- **💾 セッション永続化**  
  `export_session_json` / `import_session_json` で全状態のシリアライズ・復元に対応。

---

## 🏗️ アーキテクチャ

```
LayeredLuminaSystemV62（オーケストレーター）
│
├── 【第0層】 EmotionEngineConfig      # パラメータ外部化
├── 【第1層】 InstinctAndReasonBridge  # 本能・理性平衡
├── 【第2層】 ExtensibleEmotionDetector # 感情検出（ハイブリッド対応）
│            PianoString              # 物理弦モデル
├── 【第3層】 PersonaConfig            # ペルソナ・成長モデル
│            RelationshipManager      # 関係性ステートマシン
├── 【第4層】 ObservationLayer         # 時系列観測値・複合状態判定
│            ComplexStateRegistry     # データ駆動型ルールレジストリ
└── 【第5層】 PromptLayer              # LLMプロンプト生成
```

---

## 🚀 使い方

### 必要環境

- Python 3.9 以上
- 標準ライブラリのみ（追加インストール不要）

### 起動

```bash
python lumina_core.py
```

起動後、ターミナルでキャラクターへの入力を行うと、LLMへ渡すプロンプトが生成されます。

### 基本的な組み込み方法

```python
from lumina_core import LayeredLuminaSystemV62, PersonaConfig, EmotionEngineConfig

# ペルソナと設定を定義
persona = PersonaConfig(name="ゆら", description="優しくて少し照れ屋な20歳の女の子。")
config = EmotionEngineConfig()

# エンジン初期化
engine = LayeredLuminaSystemV62(persona, config)

# ユーザー入力からプロンプトを生成
prompt = engine.update_and_compile("今日も会いに来たよ！")
print(prompt)
# → このpromptをOpenAI / Anthropic / Gemini等のAPIに渡すだけでOK
```

### セッションの保存と復元

```python
# 保存
json_str = engine.export_session_json()
with open("session.json", "w") as f:
    f.write(json_str)

# 復元
with open("session.json") as f:
    engine.import_session_json(f.read())
```

---

## ⚙️ カスタマイズ

### ペルソナの変更

`PersonaConfig` を編集することで、キャラクターの基礎感情バイアスや成長特性を自由に設定できます。

```python
persona = PersonaConfig(
    name="あかね",
    description="クールに見えて実は甘えたがりな先輩。",
    base_emotion_bias={"Joy": 1.0, "Trust": 1.5, "Anger": 1.3, "恥ずかし": 1.6, ...}
)
```

### キーワード辞書の拡張

`ExtensibleEmotionDetector.KEYWORDS` に語句と重みを追加するだけで検出精度を向上させられます。

### 複合状態ルールの追加

```python
from lumina_core import ComplexStateRule

engine.layer4_observer.registry.register(ComplexStateRule(
    rule_id="my_custom_state",
    condition=lambda p, ema, t: p["Joy"] > 80.0 and p["恥ずかし"] > 70.0,
    priority=85,
    description="最高潮の幸福と恥ずかしさが爆発している状態"
))
```

---

## 📄 ライセンス

[LICENSE](./LICENSE) をご確認ください。  
個人・非商用利用は自由です。商用利用の場合はご連絡ください。

---

## 🙏 コントリビューション

Issue・PR 歓迎です。  
感情キーワード辞書の拡充、新しい複合状態ルールの提案など、どんな形でも貢献を歓迎します。
