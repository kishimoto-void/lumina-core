import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field

print("="*70)
print("  🎬  SceneWeaver v5.7-Custom - Advanced Acting Collapse Engine  🎬  ")
print("="*70)

EMO_KEYS = ["Joy", "Sadness", "Anger", "Fear", "Trust", "親密", "恥ずかし"]
EMO_IDX = {name: i for i, name in enumerate(EMO_KEYS)}

@dataclass
class PersonaTraits:
    name: str
    extraversion: float
    introversion: float
    base_pressures: np.ndarray 
    omega: np.ndarray          
    zeta_base: np.ndarray      
    cross_talk_matrix: np.ndarray

@dataclass
class ConcealmentParameters:
    base_skill: float = 0.85
    fatigue_accumulation_rate: float = 0.42   # 【調整】0.60 -> 0.42 (疲労蓄積をマイルドに)
    fatigue_recovery_rate: float = 0.10
    fatigue_threshold: float = 52.0
    physical_fatigue_weight: float = 0.15
    concealment_fatigue_weight: float = 0.55
    gradient_sensitivity: float = 0.006       # 【調整】0.008 -> 0.006 (感情圧による防壁低下を緩やかに)
    l2_norm_scale: float = 150.0
    stochastic_noise_scale: float = 0.10

@dataclass
class ConcealmentState:
    level: float = 0.80
    fatigue: float = 0.0
    leakage_intensity: float = 0.0
    dominant_internal_emotion: str = "恥ずかし"
    apparent_leak_emotion: str = "恥ずかし"
    leak_history: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    meta_defense_status: Optional[str] = None

    def push_history(self, val: float):
        self.leak_history.append(val)
        if len(self.leak_history) > 5:
            self.leak_history.pop(0)

    @property
    def leak_trend(self) -> float:
        if len(self.leak_history) < 3:
            return 0.0
        return float(self.leak_history[-1] - self.leak_history[-3])

class DefenseMechanism:
    """【防衛機制】深層のストレスを別の表面感情へ反転・変換するプロセッサ"""
    @staticmethod
    def transform(internal_emo: str, intensity: float, pressures: Dict[str, float]) -> Tuple[str, str]:
        if internal_emo == "恥ずかし" and pressures["恥ずかし"] > 55.0:
            return "Anger", "【反動形成（Reaction Formation）】: 猛烈な照れを隠すため、防衛本能が『冷徹な突き放し』や『怒り口調』を偽装シールドとして展開中。"
        
        if internal_emo == "Sadness" and pressures["Sadness"] > 60.0:
            return "Joy", "【代償的躁転（Compensatory Joy）】: 深い傷つきや悲しみを悟らせないため、あえて不自然なほど明るく道化のように振る舞う防衛が作動中。"
            
        if internal_emo == "Fear" and pressures["Fear"] > 60.0:
            return "Anger", "【攻撃的防衛（Aggressive Defense）】: 内心の怯えやパニックを隠蔽するため、あえて高圧的で攻撃的な態度をとることで主導権を握ろうとしている。"

        return internal_emo, "【ストレート漏出】: 防衛の変換フィルターを通らず、本音の感情がそのままダイレクトに滲み出ている状態。"

@dataclass
class ResonanceRule:
    name: str
    description: str
    priority: int
    thresholds: Dict[str, Tuple[str, float]]
    v_effects: Dict[str, float]

    def check_condition(self, pressures: Dict[str, float]) -> bool:
        for emo_name, (operator, thresh_val) in self.thresholds.items():
            current_val = pressures.get(emo_name, 50.0)
            if operator == ">" and not (current_val > thresh_val): return False
            if operator == "<" and not (current_val < thresh_val): return False
        return True

class DeclarativeResonanceEngine:
    def __init__(self):
        # 【追加・調整】ご提示いただいた新規共振ルールを優先度を考慮して統合
        self.rules: List[ResonanceRule] = [
            ResonanceRule(
                name="照れの臨界崩壊（白目覚醒）",
                description="恥ずかしさが極限に達し、思考が一時的に真っ白になる",
                priority=1,
                thresholds={"恥ずかし": (">", 88.0)},
                v_effects={"恥ずかし": 30.0, "Fear": 25.0, "Joy": -20.0, "親密": 15.0}
            ),
            ResonanceRule(
                name="限界キャパオーバー（照れ）",
                description="恥ずかしさが限界を超え、思考がホワイトアウトする",
                priority=2,
                thresholds={"恥ずかし": (">", 75.0)},
                v_effects={"恥ずかし": 25.0, "Fear": 15.0, "Joy": -15.0}
            ),
            ResonanceRule(
                name="信頼の暴走（無防備モード）",
                description="親密と信頼が極限まで高まり、防衛機構がほぼ機能しなくなる",
                priority=3,
                thresholds={"親密": (">", 85.0), "Trust": (">", 82.0)},
                v_effects={"恥ずかし": -45.0, "Joy": 35.0, "Sadness": -15.0}
            ),
            ResonanceRule(
                name="安堵による防壁完全崩壊",
                description="親密さと信頼が頂点に達し、これまでの隠蔽が嘘のように瓦解する",
                priority=4,
                thresholds={"親密": (">", 80.0), "Trust": (">", 75.0)},
                v_effects={"恥ずかし": -35.0, "Joy": 30.0}
            )
        ]

    def evaluate_all(self, pressures: Dict[str, float]) -> Optional[ResonanceRule]:
        available_rules = [r for r in self.rules if r.check_condition(pressures)]
        if not available_rules: return None
        available_rules.sort(key=lambda x: x.priority)
        return available_rules[0]

class ProfileFactory:
    @staticmethod
    def create_yura_shy() -> PersonaTraits:
        bp = np.array([55.0, 35.0, 25.0, 40.0, 60.0, 50.0, 45.0])
        om = np.array([1.2,  0.4,  1.8,  0.9,  0.5,  0.6,  2.5])
        zb = np.array([0.4,  0.2,  0.6,  0.3,  1.1,  0.3,  0.18]) 
        cm = np.zeros((7, 7))
        cm[1, 0] = -0.3; cm[0, 1] = -0.2; cm[4, 2] = -0.4; cm[2, 6] = 0.25
        return PersonaTraits(
            name="ゆら（照れ屋・内向型）", extraversion=0.3, introversion=0.8,
            base_pressures=bp, omega=om, zeta_base=zb, cross_talk_matrix=cm
        )

class StructuralResonanceCore:
    def __init__(self, traits: PersonaTraits):
        self.traits = traits
        self.x = np.zeros(7)  
        self.v = np.zeros(7)  
        self.base_drift = traits.base_pressures.copy() 
        self.zeta = traits.zeta_base.copy()            
        self.fatigue = np.zeros(7)                     
        self.pressure = traits.base_pressures.copy()
        self.current_cross_talk = traits.cross_talk_matrix.copy()

    def apply_impulse_vector(self, impulse_dict: Dict[str, float]):
        for name, val in impulse_dict.items():
            if name in EMO_IDX: 
                self.v[EMO_IDX[name]] += val

    def update_dynamic_matrix(self, stage_key: str):
        self.current_cross_talk = self.traits.cross_talk_matrix.copy()
        if stage_key == "2B_片思い": 
            self.current_cross_talk[6, 5] = 0.2  
        elif stage_key == "3B_恋人": 
            self.current_cross_talk[2, 6] = -0.1
            self.current_cross_talk[5, 6] = 0.35 

    def _state_derivative(self, x_vec: np.ndarray, v_vec: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        dxdt = v_vec
        restoring_force = - (self.traits.omega ** 2) * x_vec - 0.005 * (x_vec ** 3)
        coupling_force = np.dot(self.current_cross_talk, x_vec)
        damping_force = -2.0 * self.zeta * self.traits.omega * v_vec
        
        dvdt = restoring_force + coupling_force + damping_force
        return dxdt, dvdt

    def update_physics(self, total_dt: float, emotional_arousal: float):
        sub_steps = int(10 + 40 * emotional_arousal)
        dt = total_dt / sub_steps
        for _ in range(sub_steps):
            dxdt1, dvdt1 = self._state_derivative(self.x, self.v)
            x2, v2 = self.x + 0.5 * dt * dxdt1, self.v + 0.5 * dt * dvdt1
            dxdt2, dvdt2 = self._state_derivative(x2, v2)
            x3, v3 = self.x + 0.5 * dt * dxdt2, self.v + 0.5 * dt * dvdt2
            dxdt3, dvdt3 = self._state_derivative(x3, v3)
            x4, v4 = self.x + dt * dxdt3, self.v + dt * dvdt3
            dxdt4, dvdt4 = self._state_derivative(x4, v4)
            
            self.x += (dt / 6.0) * (dxdt1 + 2.0 * dxdt2 + 2.0 * dxdt3 + dxdt4)
            self.v += (dt / 6.0) * (dvdt1 + 2.0 * dvdt2 + 2.0 * dvdt3 + dvdt4)
            
            self.x = np.clip(self.x, -50.0, 50.0)
            self.v = np.clip(self.v, -30.0, 30.0)
            
            for i in range(7):
                fatigue_growth = abs(self.x[i]) * 0.015
                self.fatigue[i] = max(0.0, min(1.0, self.fatigue[i] + (fatigue_growth - 0.03) * dt))
                self.zeta[i] = self.traits.zeta_base[i] * (1.0 + self.fatigue[i] * 2.5)
                self.base_drift[i] = max(10.0, min(90.0, self.base_drift[i] + (self.x[i] * 0.003) * dt))

    def finalize_structural_pressure(self):
        self.pressure = np.clip(self.base_drift + self.x, 0.0, 100.0)

    def get_pressure_dict(self) -> Dict[str, float]:
        return {name: float(self.pressure[EMO_IDX[name]]) for name in EMO_KEYS}

class ConcealmentEngine:
    def __init__(self, traits: PersonaTraits):
        self.traits = traits
        self.p = ConcealmentParameters()
        self.state = ConcealmentState()
        
        self.database = {
            "恥ずかし": {
                "視線": {"微漏れ": "一瞬だけ視線が泳ぎ、すぐあなたに焦点を戻す", "中漏れ": "対面での直視を避け、斜め下の床を凝視し続ける", "大漏れ": "完全に目が泳ぎ、あなたの顔を正視できなくなる"},
                "動作": {"微漏れ": "カバンの紐を少し強く握り直す", "中漏れ": "急に髪を触り始めたり、服のシワを何度も伸ばしたりして落ち着きを失う", "大漏れ": "身体を固くこわばらせ、逃げるように一歩後ろへ退く"},
                "声音": {"微漏れ": "文末に向けてわずかに早口になる", "中漏れ": "「別に」のトーンが不自然に低くぶっきらぼうに尖る", "大漏れ": "息が上がり、上ずったパニック気味の早口になる"},
                "裏側": {"微漏れ": "いつもより語尾の歯切れが曖昧になる", "中漏れ": "「何言ってんの」と、あえて突き放すような過剰な防衛ワードが出る", "大漏れ": "論理が上滑りし、全く脈絡のない言い訳をまくし立てる"}
            },
            "Anger": {
                "視線": {"微漏れ": "拒絶するようにフイと顔を横に向ける", "中漏れ": "睨みつけるような鋭い視線を向けた後、罰が悪そうにそらす", "大漏れ": "完全に怒気を含んだ強い視線であなたを射すくめる"},
                "動作": {"微漏れ": "腕組みをして、トントンと爪先で小さく貧乏揺すりをする", "中漏れ": "持っているものを少し乱暴に机に置くなど、物動が荒くなる", "大漏れ": "拳をギュッと握りしめ、拒絶の壁を築くように背を向ける"},
                "声音": {"微漏れ": "声のトーンが一段低く、冷淡な響きを帯びる", "中漏れ": "棘のある、なじるような強い語気が不意に混ざる", "大漏れ": "「うるさい…っ！」と言葉を荒らげ、感情を叩きつけるように叫ぶ"},
                "裏側": {"微漏れ": "丁寧すぎる敬語など、あえて距離を置くような言葉選びをする", "中漏れ": "あなたの言葉を真っ向から否定するような、強い反論を返す", "大漏れ": "「関係ないでしょ」と完全に会話のシャッターを閉ざす冷たいセリフ"}
            },
            "Joy": {
                "視線": {"微漏れ": "目が合うと嬉しそうに細められる", "中漏れ": "輝くような視線であなたの顔をじっと見つめ続ける", "大漏れ": "瞳全体に喜びの光を湛え、抑えきれない視線が注がれる"},
                "動作": {"微漏れ": "歩幅がわずかに弾むように軽くなる", "中漏れ": "身振りが大きくなり、手のひらを合わせるような仕草が出る", "大漏れ": "あなたの腕に飛びつきそうになるのを必死で抑制して肩を震わせる"},
                "声音": {"微漏れ": "声のピッチが自然と高くなり、弾むような響きになる", "中漏れ": "楽しそうな笑いを含んだ、ワントーン高い明るい声", "大漏れ": "「うんっ！」と弾けるような、抑えきれない歓喜の声"},
                "裏側": {"微漏れ": "他愛のない冗談や肯定的な相槌が増える", "中漏れ": "饒舌になり、普段は言わないようなポジティブな感想が溢れ出る", "大漏れ": "セリフの端々に感情が乗り、好意が全面に露出する"}
            }
        }

    def evaluate(self, pressures: Dict[str, float], stage_key: str, physical_fatigue: np.ndarray, dt: float) -> Dict[str, Any]:
        p_vec = np.array([pressures[k] for k in EMO_KEYS])
        l2_norm = float(np.linalg.norm(p_vec))
        emotional_arousal = np.clip((l2_norm - 100.0) / self.p.l2_norm_scale, 0.0, 1.0)

        targets = {k: pressures[k] for k in ["恥ずかし", "Sadness", "Anger", "Fear", "Joy"]}
        self.state.dominant_internal_emotion = max(targets, key=targets.get)
        max_emo_val = targets[self.state.dominant_internal_emotion]
        
        if max_emo_val > self.p.fatigue_threshold:
            severity = (max_emo_val - self.p.fatigue_threshold) / (100.0 - self.p.fatigue_threshold)
            self.state.fatigue = min(1.0, self.state.fatigue + (severity ** 2) * self.p.fatigue_accumulation_rate * dt)
        else:
            self.state.fatigue = max(0.0, self.state.fatigue - self.p.fatigue_recovery_rate * dt)
            
        total_penalty = (np.mean(physical_fatigue) * self.p.physical_fatigue_weight) + (self.state.fatigue * self.p.concealment_fatigue_weight)
        current_skill = self.p.base_skill * (1.0 - total_penalty)
        
        stage_modifiers = {"2A_友達": 1.15, "2B_片思い": 0.85, "3B_恋人": 0.55}
        self.state.level = current_skill * stage_modifiers.get(stage_key, 1.0)
        self.state.level = np.clip(self.state.level - (max_emo_val - 50.0) * self.p.gradient_sensitivity, 0.01, 0.99)
        
        base_leakage = (1.0 - self.state.level) * (l2_norm / self.p.l2_norm_scale)
        stochastic_fluctuation = np.random.normal(0, max(0.01, base_leakage) * self.p.stochastic_noise_scale)
        self.state.leakage_intensity = float(np.clip(base_leakage + stochastic_fluctuation, 0.0, 1.0))
        
        self.state.push_history(self.state.leakage_intensity)

        self.state.meta_defense_status = None
        if self.state.leak_trend > 0.05 and self.state.leakage_intensity > 0.40:
            if self.state.dominant_internal_emotion == "恥ずかし":
                self.state.meta_defense_status = "【メタ防衛：強制遮断（Topic Escape）】限界以上の動揺を隠蔽するため精神が緊急脱出を敢行。脈絡のない別話題への強引な転換、または突如無口になり『……なんでもない』と対話を完全シャットダウンする行動を強いる。"
            elif self.state.dominant_internal_emotion == "Sadness":
                self.state.meta_defense_status = "【メタ防衛：自己嫌悪沈黙（Self-Isolation）】心の痛みが防壁を破り続けた結果、自暴自棄な自己卑下が作動。『私なんかと話してもつまんないよね』と自嘲し、物理的に距離をとろうとする。"

        self.state.apparent_leak_emotion, defense_narrative = DefenseMechanism.transform(
            self.state.dominant_internal_emotion, self.state.leakage_intensity, pressures
        )
        
        leak_outputs, profile_mode = self._generate_acting_manifesto(
            self.state.apparent_leak_emotion, self.state.level, self.state.leakage_intensity
        )
        
        return {
            "concealment_level": self.state.level,
            "leakage_intensity": self.state.leakage_intensity,
            "concealment_fatigue": self.state.fatigue,
            "internal_emotion": self.state.dominant_internal_emotion,
            "surface_emotion": self.state.apparent_leak_emotion,
            "defense_narrative": defense_narrative,
            "profile_mode": profile_mode,
            "meta_defense": self.state.meta_defense_status,
            "leak_channels": leak_outputs,
            "emotional_arousal": emotional_arousal
        }

    def _generate_acting_manifesto(self, surface_emo: str, concealment: float, leakage: float) -> Tuple[Dict[str, str], str]:
        outputs = {}
        e_data = self.database.get(surface_emo, self.database["恥ずかし"])
        
        if concealment > 0.70 and leakage > 0.25:
            mode = "⚠️【鉄壁の偽装（局所漏出モード）】"
            outputs["視線"] = "「完璧なコントロール」。あなたの目を真っ直ぐ、恐ろしいほど微動だにせず見つめ返して平静を装う（不自然な静寂）。"
            outputs["声音"] = "「完全なる静寂」。声のトーン、ピッチともに狂いがなく、完全に落ち着いた通常の声を維持。"
            outputs["動作"] = f"【決壊局所】{e_data['動作']['大漏れ']}（※顔や声が完全に冷徹な静寂を保っているため、この末端の異常なこわばりが逆に痛々しさを際立たせる）。"
            outputs["裏側"] = f"【決壊局所】会話の論理構造は破綻しないが、あまりにも一言の淀みもなさすぎて、まるで事前に用意された台詞をマシーンのように再生しているような違和感を生む。"
        else:
            mode = "🌊【通常分散漏出モード】"
            lvl = "微漏れ" if leakage < 0.35 else "中漏れ" if leakage < 0.65 else "大漏れ"
            for ch in ["視線", "動作", "声音", "裏側"]:
                outputs[ch] = e_data[ch].get(lvl, "不自然な揺らぎが混ざる")
                
        return outputs, mode

class SpontaneousDriveEngine:
    def __init__(self, traits: PersonaTraits):
        self.traits = traits
        self.prev_pressures: Optional[Dict[str, float]] = None

    def evaluate(self, pressures: Dict[str, float]) -> Optional[str]:
        t = self.traits
        gradients = {k: 0.0 for k in EMO_KEYS}
        if self.prev_pressures is not None:
            for k in EMO_KEYS: 
                gradients[k] = pressures[k] - self.prev_pressures[k]
        self.prev_pressures = pressures.copy()

        is_burst = any(grad > 12.0 for grad in gradients.values()) if self.prev_pressures is not None else False
        
        ext_drive = (pressures["Joy"] + pressures["親密"]) * t.extraversion
        int_drive = (pressures["恥ずかし"] + pressures["Fear"] + pressures["Sadness"]) * t.introversion
        
        if is_burst and gradients["恥ずかし"] > 12.0 and pressures["恥ずかし"] > 52.0:
            return f"💥【感情バースト衝動】想定外の接近により、恥ずかしさの感情勾配が瞬間臨界（+{gradients['恥ずかし']:.1f}）を突破。防衛線が構築されるより速く頭が真っ白になり、言い訳を考えることすら放棄して息を呑む衝動。"
        if ext_drive > 45.0:
            return "【外向的自発トリガー】高まる親密さに背中を押され、隠蔽の壁を越えて『もっと話していたい』という本音をストレートに言葉にしてしまう衝動。"
        if int_drive > 85.0:
            return "【内向的自発トリガー】内に籠もった恥ずかしさとパニックの圧力が限界に達し、物理的に視界を遮るように両手で顔を覆い隠してしまう行動衝動。"
        return None

class SceneWeaverSystem:
    def __init__(self):
        self.traits = ProfileFactory.create_yura_shy()
        self.core = StructuralResonanceCore(self.traits)
        self.resonance_engine = DeclarativeResonanceEngine() 
        self.concealment_engine = ConcealmentEngine(self.traits)
        self.spontaneous_engine = SpontaneousDriveEngine(self.traits)
        
        self.stage_key = "2A_友達"
        self.affection = 45.0
        self.turn = 0

    def process_turn(self, user_input: str) -> str:
        self.turn += 1
        dt = 5.0 if "..." in user_input else 2.0
        
        self.core.update_dynamic_matrix(self.stage_key)
        prev_arousal = self.concealment_engine.state.leakage_intensity
        
        impulses = self._parse_user_intent_into_impulses(user_input)
        self.core.apply_impulse_vector(impulses)
        
        self.core.update_physics(dt, prev_arousal)
        self.core.finalize_structural_pressure()
        pressures = self.core.get_pressure_dict()
        
        triggered_rule = self.resonance_engine.evaluate_all(pressures)
        if triggered_rule:
            self.core.apply_impulse_vector(triggered_rule.v_effects)
            self.core.update_physics(0.5, prev_arousal)
            self.core.finalize_structural_pressure()
            pressures = self.core.get_pressure_dict()

        self._update_relationship_matrix(pressures)
        
        spontaneous_speech = self.spontaneous_engine.evaluate(pressures)
        concealment_data = self.concealment_engine.evaluate(pressures, self.stage_key, self.core.fatigue, dt)
        
        self._print_v5_7_dashboard(user_input, triggered_rule, spontaneous_speech, concealment_data)
        return self._compile_v5_7_prompt(user_input, triggered_rule, spontaneous_speech, pressures, concealment_data)

    def _parse_user_intent_into_impulses(self, text: str) -> Dict[str, float]:
        """【最優先強化】強度モディファイアを考慮し、かつカテゴリの複合加算を可能にした高度解析エンジン"""
        impulses = {k: 0.0 for k in EMO_KEYS}
        text_lower = text.lower()
        
        # 1. 強度レベル分け（モディファイアの設定）
        intensity = 1.0
        if any(x in text_lower for x in ["すごく", "めっちゃ", "本気で", "ずっと", "大変", "猛烈に"]):
            intensity = 1.6
        elif any(x in text_lower for x in ["少し", "ちょっと", "わずかに", "一瞬"]):
            intensity = 0.7
            
        # 2. フラグではなく加算器にすることで複合的な文章（例: めっちゃ可愛くて大好き）を完全処理
        # 【照れ系】
        if any(x in text_lower for x in ["かわいい", "好き", "頭", "撫で", "触", "近い", "じっと", "見つめ", "照れ"]):
            impulses["恥ずかし"] += 45 * intensity
            impulses["親密"] += 32 * intensity
            impulses["Joy"] += 18 * intensity
            
        # 【好意・甘え系】
        if any(x in text_lower for x in ["一緒に", "もっと", "愛してる", "抱きしめ", "ぎゅ", "離さない"]):
            impulses["親密"] += 48 * intensity
            impulses["Joy"] += 25 * intensity
            impulses["恥ずかし"] += 35 * intensity
            
        # 【ネガティブ系】
        if any(x in text_lower for x in ["嫌い", "ひどい", "バカ", "離れ", "もういい", "ウザい"]):
            impulses["Sadness"] += 42 * intensity
            impulses["Fear"] += 28 * intensity
            impulses["Anger"] += 15 * intensity  # 反動形成の引き金用
            
        return impulses

    def _update_relationship_matrix(self, pressures: Dict[str, float]):
        self.affection = max(10, min(99, self.affection + (pressures["親密"] - 50.0) * 0.1))
        if self.affection > 65.0 and self.stage_key == "2A_友達": 
            self.stage_key = "2B_片思い"
        elif self.affection > 82.0 and self.stage_key == "2B_片思い": 
            self.stage_key = "3B_恋人"

    def _print_v5_7_dashboard(self, user_input: str, rule: Optional[ResonanceRule], sp_speech: Optional[str], leak: Dict[str, Any]):
        print("\n" + "="*90)
        print(f"📡 [SceneWeaver v5.7-Custom Dashboard] Turn: {self.turn} | Stage: {self.stage_key} | Affection: {self.affection:.1f}")
        print(f"   🛡️ 防壁強度: {leak['concealment_level']:.2f} | 😫 隠蔽疲労: {leak['concealment_fatigue']:.2f} | 📈 漏出傾向(Trend): {self.concealment_engine.state.leak_trend:+.2f}")
        print(f"   🎭 内部深層本音: 【{leak['internal_emotion']}】 ──(防衛機制)──> 表面マニフェスト: 【{leak['surface_emotion']}】")
        print(f"   👁️ 表現モード: {leak['profile_mode']} | 総漏出強度: {leak['leakage_intensity']:.2f}")
        if leak['meta_defense']: 
            print(f"   🚨 META DEFENSE ACTIVE: {leak['meta_defense']}")
        print(f"   --- 7次元構造マトリクス状態 ---")
        pressures = self.core.get_pressure_dict()
        for name in EMO_KEYS:
            ind = "■" * int(pressures[name] / 4)
            print(f"   [{name:5}] 圧:{pressures[name]:5.1f} | 疲労:{self.core.fatigue[EMO_IDX[name]]*100:4.1f}% {ind}")
        print("="*90)

    def _compile_v5_7_prompt(self, user_input: str, rule: Optional[ResonanceRule], sp_speech: Optional[str], pressures: Dict[str, float], leak: Dict[str, Any]) -> str:
        sorted_p = sorted(pressures.items(), key=lambda x: x[1], reverse=True)
        emo_line = ", ".join([f"{k}({v:.1f})" for k, v in sorted_p[:3]])
        
        meta_str = f"🚨【メタ防衛システムによる強制行動束縛】:\n  {leak['meta_defense']}\n" if leak['meta_defense'] else ""
        event_str = f"⚠️【心層共振現象（特発イベント）】:\n  『{rule.description}（{rule.name}）』\n" if rule else ""
        sp_str = f"⚡【アクターの内発的自発衝動】:\n  {sp_speech}\n" if sp_speech else ""

        channels = leak['leak_channels']
        channels_str = f"  - 【視線の演技】: {channels['視線']}\n" \
                       f"  - 【動作の演技】: {channels['動作']}\n" \
                       f"  - 【声音の演技】: {channels['声音']}\n" \
                       f"  - 【台詞の裏の演技】: {channels['裏側']}"

        return f"""最高峰のAIアクターとして、背後の感情力学プロセッサ『SceneWeaver v5.7-Custom』が算出した多層的演技データに基づき、人間味あふれる最高のロールプレイを出力してください。

【キャラクター設定】
・名前: {self.traits.name} | 現在の関係ステージ: {self.stage_key}

【現在の心層状態データ】
・優勢な内部本音トップ3: {emo_line}
・{leak['defense_narrative']}
・漏出表現モード: {leak['profile_mode']}

🎭【多層チャンネル別・不可避の漏出演技指針】
（※本人の意志とは裏腹に、あるいは防衛のシールドとして表層に強制発現してしまうサイン）
{channels_str}

{meta_str}{event_str}{sp_str}
ユーザーからの入力: 「{user_input}」

【ロールプレイ絶対遵守制約】
1. 数理的・システム的な専門用語や生数値を、台詞や地の文に絶対に露出させないこと。
2. 【二面性と局所漏出の厳守】:
   - 「通常分散漏出モード」の場合、セリフでは必死に偽装感情（表面マニフェスト）を繕わせつつ、地の文で各チャンネルの漏出サインを絶妙に描写してください。
   - 「鉄壁の偽装（局所漏出モード）」の場合、顔や声、会話の論理は『不自然なほど完璧に平気なフリ』をさせてください。しかし、その代償として【決壊局所】に指定されている動作や台詞の裏側の1点だけから、痛々しいほどの破綻を滲み出させてください。
3. 感情をただ叫んだり、「恥ずかしい」「嬉しい」といった本音を直言して自己解説することは厳禁です。すべての感情は、繕う態度と、それを裏切る身体サインのギャップのみで表現してください。"""

if __name__ == "__main__":
    weaver = SceneWeaverSystem()
    print("✅ SceneWeaver v5.7-Custom [Acting Collapse Engine] 正常起動。")
    while True:
        try:
            u_input = input("あなた: ")
            if u_input.strip() in ["終了", "exit", "quit"]: break
            if not u_input.strip(): continue
            prompt = weaver.process_turn(u_input)
            print("\n↓↓↓ 【第7層】 LLMコピペ用 最終統合プロンプト ↓↓↓\n")
            print(prompt)
            print("\n" + "-"*90 + "\n")
        except KeyboardInterrupt: break
