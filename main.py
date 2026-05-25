import datetime
import json
import math
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable

print("=" * 75)
print("  🌟  LuminaCORE v6.2 - Production-Ready & Hybrid-Ready Engine  🌟  ")
print("=" * 75)

# ==============================================================================
# 【安全な配置】 物理系コアコンポーネント (依存関係解消のため最上部に定義)
# ==============================================================================
@dataclass
class PianoTuningConfig:
    short_term_inertia: float = 0.71
    long_term_inertia: float = 0.87
    short_coeff: float = 1.08
    long_coeff: float = 0.41
    decay_short: float = 0.76
    decay_long: float = 0.815

class PianoString:
    """共鳴ピアノ物理弦モデル（循環インポート問題解決のため最上層へ安全に配置）"""
    def __init__(self, name: str, default: float, tuning: PianoTuningConfig):
        self.name = name
        self.default = default
        self.tuning = tuning
        self.short_term = default
        self.long_term = default
        self.residual = 5.0
        self.unresolved_tension = 0.0
        self.pressure = default

    def press(self, strength: float):
        t = self.tuning
        tension_mod = 1.0 + (self.unresolved_tension / 60.0)
        eff_strength = strength * tension_mod
        self.short_term = max(5, min(100, self.short_term * t.short_term_inertia + eff_strength * t.short_coeff))
        self.long_term = max(10, min(95, self.long_term * t.long_term_inertia + eff_strength * t.long_coeff))
        self.residual = min(30, self.residual + abs(eff_strength) * 0.029)
        self.unresolved_tension = min(35.0, self.unresolved_tension + abs(eff_strength) * 0.017)
        self.update_pressure()

    def suppress(self, rate: float):
        self.short_term = max(5, self.short_term * rate)
        self.long_term = max(10, self.long_term * rate)
        self.update_pressure()

    def update_pressure(self):
        self.pressure = (self.default * 0.25 + self.short_term * 0.50 + self.long_term * 0.25)

    def decay_process(self, custom_decay_modifier: float):
        """【改善：中優先】custom_decay_modifierによる自然減衰への感度（影響力）を2倍に強化"""
        t = self.tuning
        
        # 補正係数の影響力を増幅 (modifierが1.0から離れた時のスケーリング幅を拡張)
        amplified_modifier = 1.0 + (custom_decay_modifier - 1.0) * 2.0
        amplified_modifier = max(0.1, min(3.0, amplified_modifier)) # 安全ガード
        
        adj_short = 1.0 - (1.0 - t.decay_short) * amplified_modifier
        adj_long = 1.0 - (1.0 - t.decay_long) * amplified_modifier
        
        self.short_term += (self.default - self.short_term) * (1.0 - adj_short)
        self.long_term += (self.default - self.long_term) * (1.0 - adj_long)
        self.residual *= 0.950  # 揮発加速
        self.unresolved_tension *= 0.945
        self.update_pressure()

# ==============================================================================
# 【第0層】 設定・パラメータ外部化層
# ==============================================================================
@dataclass
class EmotionEngineConfig:
    base_energy_limit: float = 360.0
    jealousy_burst_buffer: float = 40.0
    energy_decay_rate: float = 0.05
    base_aff_decay: float = 0.982
    base_trust_decay: float = 0.988
    jealousy_decay_rate: float = 0.90
    string_pressure_gain: float = 12.5  
    
    antagonism: Dict[str, str] = field(default_factory=lambda: {
        "Joy": "Sadness", "Sadness": "Joy", "Trust": "Anger", "Anger": "Trust"
    })
    jealousy_triggers: List[str] = field(default_factory=lambda: [
        "他の女", "他の男", "元カノ", "元カレ", "可愛い子", "合コン", "べつの人", "浮気", "他の人と"
    ])
    default_string_pressures: Dict[str, float] = field(default_factory=lambda: {
        "Joy": 65.0, "Sadness": 35.0, "Anger": 35.0, 
        "Fear": 35.0, "Trust": 65.0, "親密": 55.0, "恥ずかし": 45.0
    })

# ==============================================================================
# 【第1層】 本能・理性平衡モジュール
# ==============================================================================
class InstinctAndReasonBridge:
    def __init__(self, config: EmotionEngineConfig):
        self.config = config
        self.novelty = 100.0  
        self.last_dominant = "Joy"

    def process_instinct(self, current_dominant: str):
        if current_dominant == self.last_dominant:
            self.novelty = max(8.0, self.novelty * 0.88)  
        else:
            self.novelty = min(100.0, self.novelty + 18.0) 
        self.last_dominant = current_dominant

    def execute_reason_equilibrium(self, strings: Dict[str, PianoString], user_input: str, intensity: float) -> Tuple[float, float]:
        novelty_factor = max(0.5, self.novelty / 100.0)
        input_len_factor = min(1.5, len(user_input) / 30.0)
        
        # custom_decay_modifierのベース計算
        custom_decay_modifier = max(0.4, min(1.2, novelty_factor * (1.2 - (intensity * 0.15)) / (1.0 + input_len_factor * 0.1)))

        for string in strings.values():
            string.decay_process(custom_decay_modifier)
            
        dyn_aff_decay = 1.0 - (1.0 - self.config.base_aff_decay) * custom_decay_modifier
        dyn_trust_decay = 1.0 - (1.0 - self.config.base_trust_decay) * custom_decay_modifier
        
        return dyn_aff_decay, dyn_trust_decay

# ==============================================================================
# 【第2層】 感情検出・評価モジュール (Hybrid / Extensible Detector)
# ==============================================================================
class ExtensibleEmotionDetector:
    """【将来の拡張を見据えたハイブリッド検出設計】"""
    KEYWORDS: Dict[str, List[Tuple[str, float]]] = {
        "Joy": [("嬉しい", 1.8), ("楽しい", 1.6), ("幸せ", 2.0), ("最高", 1.5)],
        "Sadness": [("悲しい", 2.0), ("寂しい", 2.6), ("つらい", 2.2), ("落ち込む", 1.8)],
        "Anger": [("怒", 2.0), ("ムカ", 2.3), ("嫌い", 1.9), ("ひどい", 1.5)],
        "Fear": [("不安", 2.1), ("怖い", 2.2), ("心配", 2.1), ("ごめん", 1.3)],
        "Trust": [("安心", 2.0), ("信じ", 2.0), ("大丈夫", 1.5), ("いつもありがとう", 2.2)],
        "親密": [("好き", 2.1), ("大好き", 2.7), ("ぎゅ", 2.5), ("愛してる", 2.8)],
        "恥ずかし": [("恥ずか", 2.5), ("照れ", 2.4), ("ドキドキ", 2.3), ("赤面", 2.0)]
    }

    def __init__(self, config: EmotionEngineConfig):
        self.config = config
        self.local_negation = re.compile(r"(ない|ず|違い|否定|ダメ|じゃない|ではない|嫌)")
        self.global_negation = re.compile(r"(とは(思わない|言えない))")

    def _execute_keyword_matching(self, text: str, target_emo: str) -> float:
        score = 0.0
        for kw, weight in self.KEYWORDS.get(target_emo, []):
            matches = list(re.finditer(re.escape(kw), text))
            if not matches: continue
            for match in matches:
                window_left = text[max(0, match.start()-6):match.start()]
                window_right = text[match.end():match.end()+10]
                is_negated = bool(self.local_negation.search(window_left)) or \
                             bool(self.local_negation.search(window_right)) or \
                             bool(self.global_negation.search(text))
                score += -weight * 0.8 if is_negated else weight * 1.5
        return score

    def _execute_vector_embedding_similarity(self, text: str, target_emo: str) -> float:
        """
        [将来の拡張スロット] 
        ここに sentence-transformers (rinna/japanese-sentence-bert等) や 
        Lightweight LLM を介したコサイン類似度ベクトル演算を結合するハイブリッド領域。
        現在は安全なゼロベクトルベースとしてフォールバック。
        """
        return 0.0

    def analyze(self, text: str) -> Tuple[str, float, bool]:
        text_clean = unicodedata.normalize('NFKC', text).lower().replace(" ", "")
        
        raw_scores = {}
        for emo in self.KEYWORDS.keys():
            kw_score = self._execute_keyword_matching(text_clean, emo)
            vec_score = self._execute_vector_embedding_similarity(text_clean, emo)
            # 将来的には 0.4 * kw_score + 0.6 * vec_score のようにブレンド可能
            raw_scores[emo] = max(-5.0, kw_score + vec_score)

        shift_scores = {k: math.pow(1.5, min(8.0, max(-4.0, v))) for k, v in raw_scores.items()}
        sum_exp = sum(shift_scores.values())
        
        dominant = max(raw_scores, key=raw_scores.get)
        prob = shift_scores[dominant] / sum_exp if sum_exp > 0 else 0.1
        
        intensity = min(2.6, max(0.4, (raw_scores[dominant] * 0.35) + (prob * 1.4)))
        jealousy_triggered = any(trigger in text_clean for trigger in self.config.jealousy_triggers)
        
        return dominant, intensity, jealousy_triggered

# ==============================================================================
# 【データ駆動型】 複合精神状態判定ルールレジストリ
# ==============================================================================
@dataclass
class ComplexStateRule:
    rule_id: str
    condition: Callable[[Dict[str, float], str, float], bool]
    priority: int
    description: str

class ComplexStateRegistry:
    """【改善：中優先】判定ルールを完全にデータ駆動型クラス化し、メンテナンス性を向上"""
    def __init__(self):
        self.rules: List[ComplexStateRule] = []
        self._load_default_rules()

    def register(self, rule: ComplexStateRule):
        self.rules.append(rule)
        # 登録時に優先度の降順で自動ソート
        self.rules.sort(key=lambda x: x.priority, reverse=True)

    def _load_default_rules(self):
        # 外部JSON等から読み込めるよう、コンストラクタ内でルールをデータ駆動登録
        self.register(ComplexStateRule(
            "disappointed_freeze", lambda p, ema, t: t < 0.65, 110, 
            "感情低迷（ショックや精神的疲弊による防衛的フリーズ・無気力状態）"
        ))
        self.register(ComplexStateRule(
            "love_hate_clash", lambda p, ema, t: p["Anger"] > 60.0 and p["親密"] > 55.0, 100, 
            "強烈な愛憎相半ば（独占欲の暴走、激しい嫉妬を隠すための攻撃的拒絶）"
        ))
        self.register(ComplexStateRule(
            "panic_abandonment", lambda p, ema, t: p["Sadness"] > 60.0 and p["Fear"] > 55.0, 95, 
            "見捨てられ不安の臨界（深い悲愁と恐怖によるパニック、思考の凍結）"
        ))
        self.register(ComplexStateRule(
            "classic_tsundere", lambda p, ema, t: p["Anger"] > 50.0 and p["恥ずかし"] > 50.0, 90, 
            "クラシック・ツンデレ（内面の動揺や好意を、乱暴な言葉や怒りで必死に隠蔽）"
        ))
        self.register(ComplexStateRule(
            "sulk_hiding", lambda p, ema, t: p["Anger"] > 45.0 and p["親密"] > 45.0 and ema == "親密", 80, 
            "拗ね・強がり（寂しさや嫉妬を素直に表現できず、反発の仮面を被っている状態）"
        ))
        self.register(ComplexStateRule(
            "trust_tears", lambda p, ema, t: p["Sadness"] > 45.0 and ema == "Trust", 75, 
            "甘えを孕んだ涙（相手を深く信頼しているからこそ見せる、無防備な拗ね・悲哀）"
        ))
        self.register(ComplexStateRule(
            "pure_shyness", lambda p, ema, t: p["親密"] > 60.0 and p["恥ずかし"] > 55.0, 70, 
            "純情な高揚感（好意が溢れてしまい、どう振る舞えばいいか分からず赤面動揺）"
        ))
        self.register(ComplexStateRule(
            "absolute_happiness", lambda p, ema, t: p["Joy"] > 60.0 and p["親密"] > 60.0, 60, 
            "満たされた幸福感（絶対的な親愛と歓喜、全幅の肯定的信頼に包まれた状態）"
        ))
        self.register(ComplexStateRule(
            "secure_relief", lambda p, ema, t: p["Trust"] > 55.0 and p["Joy"] > 50.0, 50, 
            "無邪気な絶対安堵（何の疑いもなく相手の言葉に寄り添う、健やかで開かれた心）"
        ))
        self.register(ComplexStateRule(
            "anxious_threshold", lambda p, ema, t: p["Fear"] > 50.0 and p["恥ずかし"] > 45.0, 40, 
            "戸惑いと怯え（一歩踏み込まれた関係への嬉しさと、傷つく恐怖の境界線）"
        ))

    def evaluate(self, pressures: Dict[str, float], top_ema: str, temperature: float) -> str:
        for rule in self.rules:
            if rule.condition(pressures, top_ema, temperature):
                return rule.description
        return "ニュートラル（平穏・安定）"

# ==============================================================================
# 【第3層】 メタ層：ペルソナ・関係性ステStateMachine
# ==============================================================================
@dataclass
class PersonaConfig:
    name: str = "ゆら"
    description: str = "優しくて少し照れ屋な20歳の女の子。"
    age: int = 20
    color: str = "  🌸  "
    base_emotion_bias: Dict[str, float] = field(default_factory=lambda: {
        "Joy": 1.25, "Trust": 1.32, "親密": 1.45, "恥ずかし": 1.38, "Sadness": 1.0, "Anger": 1.0, "Fear": 1.0
    })
    experience: float = 0.0
    growth_traits: Dict[str, float] = field(default_factory=lambda: {
        "Trust_Growth": 0.003, "Anger_Decay": -0.002, "Shy_Decay": -0.004
    })
    
    def __post_init__(self):
        self.dynamic_bias = self.base_emotion_bias.copy()

    def update_growth(self, user_input: str, intensity: float):
        input_len = len(user_input)
        density_gain = 0.5 + min(1.5, input_len / 40.0) + min(1.0, intensity * 0.4)
        self.experience = round(self.experience + density_gain, 2)

    def update_dynamic_bias(self, affection_level: float, turn: int):
        aff_factor = max(-0.8, min(0.8, (affection_level - 50) / 80.0))
        log_turn_factor = math.log(turn + 1) * 0.08
        time_decay = max(0.35, 1.0 / (1.0 + log_turn_factor))
        
        g_trust = self.experience * self.growth_traits["Trust_Growth"]
        g_anger = max(-0.3, self.experience * self.growth_traits["Anger_Decay"])
        g_shy = max(-0.4, self.experience * self.growth_traits["Shy_Decay"])

        for emo in list(self.dynamic_bias.keys()):
            bias = self.base_emotion_bias.get(emo, 1.0) * (1.0 + aff_factor * 0.45)
            if emo == "Trust": bias += g_trust
            elif emo == "Anger": bias = max(0.5, bias + g_anger)
            elif emo == "恥ずかし": bias = max(0.4, bias * time_decay + g_shy)
            self.dynamic_bias[emo] = round(bias, 3)


class RelationshipManager:
    ROUTES = {
        "0_他人": {"name": "他人", "color": "  ⚪  "}, "1_顔見知り": {"name": "顔見知り", "color": "  💙  "},
        "2A_友達": {"name": "友達", "color": "  💚  "}, "3A_仲良し": {"name": "仲良し", "color": "  💚  "},
        "4A_親友": {"name": "親友", "color": "  💚  "}, "2B_片思い": {"name": "片思い", "color": "  ❤️  "},
        "3B_恋人": {"name": "恋人", "color": "  💞  "}, "4B_深い恋": {"name": "深い恋", "color": "  🌹  "},
    }

    def __init__(self, config: EmotionEngineConfig):
        self.config = config
        self.stage_key = "2A_友達"
        self.affection = 45.0
        self.trust = 45.0
        self.jealousy = 0.0

    def apply_dynamics(self, effective_intensity: float, is_positive: bool, is_jealousy_trigger: bool):
        if is_positive:
            self.affection = min(99.0, self.affection + effective_intensity * 2.5)
            self.trust = min(98.0, self.trust + effective_intensity * 2.0)
        else:
            self.affection = max(5.0, self.affection - effective_intensity * 1.5)
            
        if is_jealousy_trigger:
            self.jealousy = min(100.0, self.jealousy + effective_intensity * 28.0)
        elif not is_positive:
            self.jealousy = min(85.0, self.jealousy + effective_intensity * 3.0)

    def evaluate_stage_transition(self) -> bool:
        """【改善】ステージ遷移の有無をブーリアン（True/False）で返却するように設計変更"""
        old_stage = self.stage_key
        aff, ts, jl, curr = self.affection, self.trust, self.jealousy, self.stage_key
        
        if aff < 12: self.stage_key = "0_他人"
        elif aff < 32: self.stage_key = "1_顔見知り"
        elif aff >= 45 and jl > 55.0 and curr in ["2A_友達", "3A_仲良し"]: self.stage_key = "2B_片思い"
        elif curr.endswith("B"):
            if aff >= 88 and curr == "3B_恋人": self.stage_key = "4B_深い恋"
            elif aff >= 72 and curr == "2B_片思い" and ts >= 55.0: self.stage_key = "3B_恋人"
            elif aff < 38: self.stage_key = "2A_友達"
        else:
            if aff >= 82: self.stage_key = "4A_親友"
            elif aff >= 58: self.stage_key = "3A_仲良し"
            elif aff >= 38 and curr == "1_顔見知り": self.stage_key = "2A_友達"
            if aff >= 48 and jl > 35.0: self.stage_key = "2B_片思い"
            
        return old_stage != self.stage_key

    def apply_decay(self, aff_rate: float, trust_rate: float):
        self.affection = max(8.0, self.affection * aff_rate)
        self.trust = max(12.0, self.trust * trust_rate)
        self.jealousy = max(0.0, self.jealousy * self.config.jealousy_decay_rate)

    def get_current_route_info(self) -> Dict:
        return self.ROUTES[self.stage_key]

# ==============================================================================
# 【第4層】 観測値層
# ==============================================================================
class ObservationLayer:
    def __init__(self, config: EmotionEngineConfig):
        self.config = config
        self.last_snapshot: Optional[Dict[str, Any]] = None
        self.ema_history: Dict[str, float] = {k: 50.0 for k in config.default_string_pressures.keys()}
        self.ema_alpha = 0.25 
        self.current_energy_limit = config.base_energy_limit
        self.context_memory: List[str] = []
        self.registry = ComplexStateRegistry() # データ駆動型判定レジストリ

    def push_context(self, user_input: str):
        self.context_memory.append(user_input)
        if len(self.context_memory) > 5: self.context_memory.pop(0)

    def enforce_energy_conservation(self, strings: Dict[str, PianoString]):
        current_total = sum(s.pressure for s in strings.values())
        if current_total > self.current_energy_limit:
            scale_factor = self.current_energy_limit / current_total
            for string in strings.values():
                string.short_term *= scale_factor
                string.long_term *= scale_factor
                string.update_pressure()

    def capture(self, orchestrator, dominant_emotion: str, jealousy_style: str, jealousy_triggered: bool) -> Dict[str, Any]:
        p_config = orchestrator.layer3_persona
        rm = orchestrator.layer3_relationship
        stage_info = rm.get_current_route_info()
        
        if jealousy_triggered:
            self.current_energy_limit = self.config.base_energy_limit + self.config.jealousy_burst_buffer
        else:
            self.current_energy_limit = max(
                self.config.base_energy_limit, 
                self.current_energy_limit - (self.current_energy_limit - self.config.base_energy_limit) * self.config.energy_decay_rate
            )

        self.enforce_energy_conservation(orchestrator.layer2_strings)
        current_strings = {name: round(string.pressure, 1) for name, string in orchestrator.layer2_strings.items()}
        current_total_energy = round(sum(current_strings.values()), 1)
        
        for name, curr_p in current_strings.items():
            self.ema_history[name] = round(self.ema_history[name] * (1.0 - self.ema_alpha) + curr_p * self.ema_alpha, 1)

        deltas = {}
        if self.last_snapshot:
            old_strings = self.last_snapshot["all_strings"]
            for name, curr_p in current_strings.items(): deltas[name] = round(curr_p - old_strings.get(name, curr_p), 1)
            delta_affection = round(rm.affection - self.last_snapshot["affection"], 1)
            delta_trust = round(rm.trust - self.last_snapshot["trust"], 1)
        else:
            deltas = {name: 0.0 for name in current_strings}
            delta_affection, delta_trust = 0.0, 0.0

        top_ema_emotion = sorted(self.ema_history.items(), key=lambda x: x[1], reverse=True)[0][0]
        emotion_temperature = round(current_total_energy / self.config.base_energy_limit, 2)

        # データ駆動型レジストリによる複合精神状態の動的解決
        complex_state = self.registry.evaluate(current_strings, top_ema_emotion, emotion_temperature)

        snapshot = {
            "meta_name": p_config.name, "stage_name": stage_info["name"], "stage_color": stage_info["color"],
            "affection": round(rm.affection, 1), "trust": round(rm.trust, 1), "jealousy": round(rm.jealousy, 1),
            "delta_affection": delta_affection, "delta_trust": delta_trust,
            "dominant_emotion": dominant_emotion, "jealousy_style": jealousy_style,
            "all_strings": current_strings, "total_energy": current_total_energy,
            "energy_limit": round(self.current_energy_limit, 1), "emotion_temperature": emotion_temperature,
            "ema_history": self.ema_history.copy(), "deltas": deltas, "complex_state": complex_state,
            "context_memory": list(self.context_memory), "turn": orchestrator.turn, "experience": p_config.experience
        }
        self.last_snapshot = snapshot.copy()
        return snapshot

# ==============================================================================
# 【第5層】 プロンプト生成層
# ==============================================================================
class PromptLayer:
    @staticmethod
    def compile(user_input: str, obs: Dict[str, Any]) -> str:
        sorted_strings = sorted(obs["all_strings"].items(), key=lambda x: x[1], reverse=True)
        emotion_abs = ", ".join([f"{k}(強度:{v})" for k, v in sorted_strings[:3]])
        
        sorted_deltas = sorted(obs["deltas"].items(), key=lambda x: abs(x[1]), reverse=True)
        emotion_deltas = ", ".join([f"{k}(変化量:{'+' if v>0 else ''}{v})" for k, v in sorted_deltas[:2] if v != 0])
        if not emotion_deltas: emotion_deltas = "全体的に安定"

        sorted_ema = sorted(obs["ema_history"].items(), key=lambda x: x[1], reverse=True)
        mood_history = ", ".join([f"{k}(持続圧:{v})" for k, v in sorted_ema[:2]])
        memory_str = " -> ".join([f"「{m}」" for m in obs["context_memory"]])

        jealousy_section = ""
        if obs["jealousy"] > 10.0:
            style_guidelines = {
                "甘える嫉妬 (Melting)": "【演技指示: 可愛い拗ね、抱きつくなど、独占欲と純情な好意の表出】",
                "試す嫉妬 (Testing)": "【演技指示: 突き放すような物言いで気を引こうとする、見捨てられ不安の裏返し】",
                "笑う嫉妬 (Irony)": "【演技指示: 言葉とは裏腹に目が笑っていない、プライドの滲む冷笑・皮肉表現】",
                "凍る嫉妬 (Frozen)": "【演技指示: 感情の起伏が消え、機械的な敬語や極端に短い言葉になる静かな拒絶】"
            }
            jealousy_section = f"\n・[発動中の嫉妬スタイル]: 【 {obs['jealousy_style']} 】\n  💡 スタイル限定演技指示: {style_guidelines.get(obs['jealousy_style'], '')}"

        temp_guide = "通常どおりの生々しい感情起伏"
        if obs["emotion_temperature"] < 0.65:
            temp_guide = "【全体活性度低下】心がエネルギー切れを起こしています。言葉数が少なくリアクションが鈍い『引き算の演技』を徹底してください。"

        prompt = f"""あなたは以下のコプロセッサが弾き出した【5層立体感情パラメトリクス】を内包し、{obs["meta_name"]}として極めて自然な応答を行ってください。

【第3層: メタ・コンテキスト＆成長度】
・現在の心理的距離（ステージ）: {obs["stage_color"]}{obs["stage_name"]} 
・累積経験値(対話密度): {obs["experience"]} （値が大きいほど、初期の過剰な壁やトゲが丸くなり、あなたへの素早な安心感がベースに馴染んでいる演技にすること）

【第4層: 時系列・立体観測値データ】
・[直近数ターンの文脈保持ベクトル]: {memory_str}
・[精神恒常性] 感情総エネルギー: {obs["total_energy"]} / {obs["energy_limit"]}
・[感情活性温度] {obs["emotion_temperature"]} 
  💡 温度ガイダンス: {temp_guide}
・[感情弦絶対値] {emotion_abs}
・[感情弦動的差分($\Delta$)] {emotion_deltas}
・[底流感情ムード(EMA履歴)] {mood_history}
・[複合精神コンテキスト] 現在の心の機微: 【 {obs["complex_state"]} 】
・[関係性ベクトル] 好感度: {obs["affection"]} ({'+' if obs["delta_affection"]>=0 else ''}{obs["delta_affection"]}) | 信頼度: {obs["trust"]} ({'+' if obs["delta_trust"]>=0 else ''}{obs["delta_trust"]}){jealousy_section} | 嫉妬心: {obs["jealousy"]}/100

ユーザーからの入力: 「{user_input}」

【第5層: ロールプレイ出力制限】
1. 直近の文脈を踏まえ、最新の「動的差分」と「底流感情ムード」をブレンドした台詞にすること。
2. 経験値の多さを踏まえ、対話が深まっている場合は「慣れた距離感による安心感」をベースのトーンに含ませてください。
3. 数値データは絶対に出力せず、セリフの間や言葉選びだけで表現すること。"""
        return prompt


# ==============================================================================
# 【第5層】 オーケストレーター（統括モジュール：クリーンリファクタリング済）
# ==============================================================================
class LayeredLuminaSystemV62:
    def __init__(self, persona: PersonaConfig, config: Optional[EmotionEngineConfig] = None):
        self.config = config or EmotionEngineConfig()
        self.layer3_persona = persona
        self.layer3_relationship = RelationshipManager(self.config)
        
        # 依存関係が上部で解消されたPianoStringをクリーンに生成 (循環インポートの完全消滅)
        self.layer2_strings: Dict[str, PianoString] = {}
        self._init_layer2_strings()
        
        self.layer1_bridge = InstinctAndReasonBridge(self.config)
        self.detector = ExtensibleEmotionDetector(self.config)
        self.layer4_observer = ObservationLayer(self.config)
        self.turn = 0
        
        # 初期状態の性格バイアスを適用
        self.layer3_persona.update_dynamic_bias(self.layer3_relationship.affection, self.turn)

    def _init_layer2_strings(self):
        for name, default in self.config.default_string_pressures.items():
            self.layer2_strings[name] = PianoString(name, default, PianoTuningConfig())

    def _process_emotion_input(self, user_input: str) -> Tuple[str, float, bool]:
        dominant, intensity, jealousy_triggered = self.detector.analyze(user_input)
        
        # 経験値（成長度）の加算
        self.layer3_persona.update_growth(user_input, intensity)
        
        # 物理弦の加圧
        bias = self.layer3_persona.dynamic_bias.get(dominant, 1.0)
        effective_intensity = intensity * bias
        if dominant in self.layer2_strings:
            self.layer2_strings[dominant].press(effective_intensity * self.config.string_pressure_gain)
            
        if dominant in self.config.antagonism:
            opposed = self.config.antagonism[dominant]
            if opposed in self.layer2_strings:
                self.layer2_strings[opposed].suppress(rate=0.85)
                
        return dominant, effective_intensity, jealousy_triggered

    def _determine_jealousy_style(self) -> str:
        """【改善】親密圧、恥ずかし圧を色濃く反映した、より多次元で生々しい嫉妬スタイル調停"""
        rm = self.layer3_relationship
        
        def get_blended_pressure(name: str) -> float:
            return self.layer2_strings[name].pressure * 0.6 + self.layer4_observer.ema_history.get(name, 50.0) * 0.4

        anger_blend = get_blended_pressure("Anger")
        sad_blend = get_blended_pressure("Sadness")
        fear_blend = get_blended_pressure("Fear")
        intimacy_blend = get_blended_pressure("親密")
        shy_blend = get_blended_pressure("恥ずかし")

        # 1. 好意や信頼が深く、親密・恥ずかしさが高い場合 ➔ 好意が独占欲としてバースト
        if rm.affection >= 65.0 and (intimacy_blend > 55.0 or shy_blend > 55.0):
            return "甘える嫉妬 (Melting)"
        
        # 2. 信頼が低く、かつ恐怖や恥ずかしさ（からかわれている不安）が勝る ➔ 臆病な試し行動
        if rm.trust < 55.0 and (fear_blend > sad_blend or shy_blend > 50.0):
            return "試す嫉妬 (Testing)"
        
        # 3. 怒りが強く、かつ親密さが低い（あるいはプライドが邪魔をする） ➔ 防衛的な冷笑・皮肉
        if anger_blend > sad_blend:
            return "笑う嫉妬 (Irony)"
            
        # 4. 上記いずれにも当てはまらない、悲しみと見捨てられ不安の拒絶 ➔ フリーズ
        return "凍る嫉妬 (Frozen)"

    def _execute_jealousy_burst(self, style: str):
        rm = self.layer3_relationship
        if style == "甘える嫉妬 (Melting)":
            self.layer2_strings["親密"].press(35.0)
            self.layer2_strings["恥ずかし"].press(30.0)
            self.layer2_strings["Anger"].press(8.0) 
        elif style == "試す嫉妬 (Testing)":
            self.layer2_strings["Fear"].press(40.0)
            self.layer2_strings["Sadness"].press(25.0)
            self.layer2_strings["恥ずかし"].press(20.0)
        elif style == "笑う嫉妬 (Irony)":
            self.layer2_strings["Anger"].press(45.0)
            self.layer2_strings["Joy"].press(22.0)  
            rm.trust = max(10.0, rm.trust - 12.0)
        elif style == "凍る嫉妬 (Frozen)":
            self.layer2_strings["Sadness"].press(40.0)  
            self.layer2_strings["Fear"].press(30.0)      
            self.layer2_strings["Joy"].short_term = 12.0  
            rm.trust = max(10.0, rm.trust - 10.0)        

    def _update_relationship_and_equilibrium(self, dominant: str, effective_intensity: float, jealousy_triggered: bool, user_input: str):
        is_pos = dominant in {"Joy", "Trust", "親密"}
        self.layer3_relationship.apply_dynamics(effective_intensity, is_pos, jealousy_triggered)
        
        # ステージの変化（関係性のマイルストーン遷移）があったかどうかを検証
        stage_changed = self.layer3_relationship.evaluate_stage_transition()
        
        # 【改善】毎ターンの呼び出しを廃止。関係性に構造変化（進化/退化）が起きた時だけ性格を再最適化
        if stage_changed:
            self.layer3_persona.update_dynamic_bias(self.layer3_relationship.affection, self.turn)
            print(f" [📈 StateMachine] 関係性ステージが変動したため、性格バイアス({self.layer3_persona.name})を再計算しました。")

        # 理性平衡の適用
        aff_rate, trust_rate = self.layer1_bridge.execute_reason_equilibrium(self.layer2_strings, user_input, effective_intensity)
        self.layer3_relationship.apply_decay(aff_rate, trust_rate)

    def update_and_compile(self, user_input: str) -> str:
        self.turn += 1
        self.layer4_observer.push_context(user_input)
        
        dominant, effective_intensity, jealousy_triggered = self._process_emotion_input(user_input)
        
        jealousy_style = "なし"
        if jealousy_triggered:
            jealousy_style = self._determine_jealousy_style()
            self._execute_jealousy_burst(jealousy_style)
            
        self.layer1_bridge.process_instinct(dominant)
        self._update_relationship_and_equilibrium(dominant, effective_intensity, jealousy_triggered, user_input)
        
        observation_data = self.layer4_observer.capture(self, dominant, jealousy_style, jealousy_triggered)
        
        print("\n" + "-"*75)
        print(f"📡 [v6.2 観測値] ターン: {observation_data['turn']} | 累積経験値: {observation_data['experience']}")
        print(f"                  複合精神: 【 {observation_data['complex_state']} 】")
        print(f"                  関係ステージ: {observation_data['stage_color']}{observation_data['stage_name']} (好感:{observation_data['affection']} / 信頼:{observation_data['trust']})")
        print("-"*75)

        return PromptLayer.compile(user_input, observation_data)

    # ==============================================================================
    # 状態の永続化層 (Serialization & Persistence Layer)
    # ==============================================================================
    def export_session_json(self) -> str:
        state_dict = {
            "turn": self.turn,
            "relationship": {
                "stage_key": self.layer3_relationship.stage_key,
                "affection": self.layer3_relationship.affection,
                "trust": self.layer3_relationship.trust,
                "jealousy": self.layer3_relationship.jealousy,
            },
            "persona": asdict(self.layer3_persona),
            "strings": {
                name: {
                    "short_term": s.short_term, "long_term": s.long_term,
                    "residual": s.residual, "unresolved_tension": s.unresolved_tension, "pressure": s.pressure
                } for name, s in self.layer2_strings.items()
            },
            "observer": {
                "ema_history": self.layer4_observer.ema_history,
                "context_memory": self.layer4_observer.context_memory,
                "current_energy_limit": self.layer4_observer.current_energy_limit
            }
        }
        return json.dumps(state_dict, ensure_ascii=False, indent=2)

    def import_session_json(self, json_str: str):
        data = json.loads(json_str)
        self.turn = data["turn"]
        
        rm = data["relationship"]
        self.layer3_relationship.stage_key = rm["stage_key"]
        self.layer3_relationship.affection = rm["affection"]
        self.layer3_relationship.trust = rm["trust"]
        self.layer3_relationship.jealousy = rm["jealousy"]
        
        p = data["persona"]
        self.layer3_persona.experience = p["experience"]
        self.layer3_persona.base_emotion_bias = p["base_emotion_bias"]
        self.layer3_persona.dynamic_bias = p["dynamic_bias"]
        
        for name, s_data in data["strings"].items():
            if name in self.layer2_strings:
                s = self.layer2_strings[name]
                s.short_term = s_data["short_term"]
                s.long_term = s_data["long_term"]
                s.residual = s_data["residual"]
                s.unresolved_tension = s_data["unresolved_tension"]
                s.pressure = s_data["pressure"]
                
        obs = data["observer"]
        self.layer4_observer.ema_history = obs["ema_history"]
        self.layer4_observer.context_memory = obs["context_memory"]
        self.layer4_observer.current_energy_limit = obs["current_energy_limit"]
        print(" [💾 System] セッションデータから全パラメータの状態を完全復元しました。")


if __name__ == "__main__":
    persona = PersonaConfig()
    engine_config = EmotionEngineConfig()
    orchestrator = LayeredLuminaSystemV62(persona, engine_config)
    
    print(" ✅  LuminaCORE v6.2 循環インポート解消・データ駆動版、正常稼働。")
    print("テスト用に入力してください（例:他の人と遊びに行ったの？ / 大好き）。\n")
    
    while True:
        u_input = input("あなた: ")
        if u_input.strip() in ["終了", "exit"]: break
        if not u_input.strip(): continue
        
        prompt_output = orchestrator.update_and_compile(u_input)
        print("\n[生成プロンプトプレビュー]")
        print("\n".join(prompt_output.split("\n")[:14]) + "\n...（以下略）")
        print("=" * 75)
