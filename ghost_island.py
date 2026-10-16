"""
유령의 섬 - 파이썬 미니 프로젝트

장르: 자유형 프로그램 / 주어: 유령 / 공간: 무인도
돌발 상황: 숨겨져 있던 조건이 뒤늦게 드러난다

무인도에 표류한 주인공이, 먼저 이 섬에 와서 죽은 유령 '윤서'와 함께
섬의 비밀을 찾으며 탈출을 준비하는 어드벤처 게임 (tkinter 창).
"""
import os
import random
import tkinter as tk

# ===== 게임 데이터 =====
DAY_LIMIT = 20

# 윤서 신뢰도: 최대치가 되어야 진엔딩
MAX_TRUST = 5
# 대화했을 때 신뢰도가 오를 확률 (지금 신뢰도 0, 1, 2, 3, 4일 때)
TRUST_UP_CHANCE = [1.0, 0.8, 0.6, 0.4, 0.2]

# 엔딩 그림 파일이 있는 폴더 (이 파이썬 파일과 같은 폴더)
IMAGE_DIR = os.path.dirname(os.path.abspath(__file__))
# 장소별 그림 파일
PLACE_IMAGES = {
    "해변": "place_beach.png",
    "정글": "place_jungle.png",
    "동굴": "place_cave.png",
    "언덕": "place_hill.png",
}

PLACES = {
    "해변": "하얀 모래사장. 부서진 배 조각들이 파도에 밀려와 있다.",
    "정글": "빽빽한 나무와 덩굴. 새 울음소리가 끊이지 않는다.",
    "동굴": "차가운 바람이 새어 나오는 어두운 동굴. 안쪽은 보이지 않는다.",
    "언덕": "섬이 한눈에 내려다보이는 언덕. 낡은 오두막 한 채가 서 있다.",
}

# 장소별로 탐색했을 때 나올 수 있는 물건 (None = 아무것도 없음)
LOOT = {
    "해변": ["나무판자", "나무판자", "돛천", "기름통", None],
    "정글": ["덩굴", "덩굴", "나뭇가지", "열매", "열매"],
    "언덕": ["열매", None, None],
}

# 제작법: 만들 물건 -> 필요한 재료와 개수
RECIPES = {
    "횃불": {"나뭇가지": 1, "기름통": 1},
    "뗏목": {"나무판자": 3, "덩굴": 2, "돛천": 1},
}

# 윤서가 남긴 일지 조각 (장소마다 하나씩 숨겨져 있음)
DIARY = {
    "해변": "[일지 1] 3일째. 뗏목을 완성했다. 내일 아침이면 집에 간다!",
    "정글": "[일지 2] 9일째. 또 안개다. 몇 번을 나가도 섬으로 되돌아온다. "
            "섬이 나를 붙잡고 있는 것 같다.",
    "언덕": "[일지 3] 이 섬엔 나보다 먼저 온 사람의 무덤이 있다. "
            "그 사람은... 떠날 수 있었을까?",
}
LAST_PAGE = ("[마지막 일지] 몸이 움직이지 않는다. 누군가 이걸 읽는다면 부탁한다. "
             "나를 여기 두고 가지 마. 그러면 너도 못 떠날 거야.")

# 장소에 처음 도착했을 때 윤서의 한마디
FIRST_VISIT = {
    "해변": "여기서 매일 수평선을 봤어. 배가 지나가길 바라면서.",
    "정글": "밤엔 들어오지 마. 길을 잃으면... 아, 난 이미 잃었구나.",
    "동굴": "...여긴 별로 오고 싶지 않은데. 왠지 춥거든. 유령인데도.",
    "언덕": "저 오두막, 내가 지었어. 꽤 괜찮지?",
}

# 날짜별 안개 묘사: (시작하는 날, 아침 묘사들, 그 단계 첫날 윤서의 경고)
FOG_STAGES = [
    (1, ["수평선 너머에 옅은 안개가 걸려 있다. 아직은 멀다.",
         "아침 바다 위로 안개가 얇게 깔려 있다. 별일 아니겠지."],
     None),
    (6, ["안개가 해변까지 올라왔다. 손끝이 유난히 차갑다.",
         "자고 일어나니 옷이 축축하다. 안개가 밤새 몸을 감싸고 있었다."],
     "윤서: \"안개가 가까워졌어. ...예전에 나한테도 이랬어.\""),
    (11, ["햇빛에 손을 비춰 보니... 손바닥 너머로 모래가 희미하게 비친다.",
          "집 주소가 잘 떠오르지 않는다. 안개가 기억까지 갉아먹는 것 같다."],
     "윤서: \"너... 점점 나랑 비슷해지고 있어. 서둘러.\""),
    (16, ["발자국이 모래에 거의 남지 않는다. 몸이 안개처럼 가벼워졌다.",
          "안개 속에서 누군가 내 이름을 부른다. 돌아보니... 내 목소리였다."],
     "윤서: \"안 돼, 시간이 얼마 없어! 너까지 여기 남게 둘 순 없어!\""),
]

# 먹을 수 있는 것 -> 체력 회복량
FOODS = {"열매": 3, "고기": 5}

# 장소별로 나타나는 큰 동물: (등장, 도망쳤을 때, 싸워서 이겼을 때, 싸워서 졌을 때)
FIGHT_WIN_RATE = 0.6
ANIMALS = {
    "해변": ("물가에 떠 있던 통나무가 움직인다... 바다악어다!",
             "모래에 발이 푹푹 빠졌지만 물가에서 멀리 도망쳤다.",
             "막대기로 콧등을 정확히 내리쳤다! 바다악어가 축 늘어졌다.",
             "콧등을 노렸지만 빗나갔다. 휘두른 꼬리에 크게 얻어맞았다."),
    "정글": ("덤불이 흔들리더니 거대한 멧돼지가 튀어나왔다!",
             "나무 사이로 정신없이 달려 멧돼지를 따돌렸다.",
             "돌진을 옆으로 피하고 맞받아쳤다! 멧돼지가 쓰러졌다.",
             "돌진을 피하지 못했다. 멧돼지에게 들이받혀 나뒹굴었다."),
    "동굴": ("어둠 속에서 낮은 으르렁 소리... 곰이다!",
             "숨을 죽이고 뒷걸음질쳐 동굴 밖으로 빠져나왔다.",
             "날카로운 돌로 급소를 내리쳤다! 곰이 쿵 하고 쓰러졌다.",
             "곰은 꿈쩍도 하지 않았다. 앞발에 팔을 깊게 긁혔다."),
    "언덕": ("풀숲에서 들개 무리가 으르렁거리며 둘러싼다!",
             "오두막 안으로 뛰어들어 문을 걸어 잠갔다.",
             "막대기로 우두머리를 쓰러뜨리자 무리가 흩어졌다!",
             "사방에서 달려드는 들개들에게 여기저기 물렸다."),
}

# 신뢰도에 따라 달라지는 윤서의 대사 (탈출 시도 전)
GHOST_LINES = [
    "...산 사람이 오다니. 난 윤서야. 여기서 죽었지. 겁먹지 마, 해치진 않아.",
    "해변엔 내 배 조각이 아직 굴러다녀. 판자랑 돛천은 쓸 만할 거야.",
    "정글 덩굴은 질겨. 뗏목을 묶기엔 그만이지. ...나도 그렇게 만들었었어.",
    "동굴은 너무 어두워. 나뭇가지에 기름을 먹이면 횃불이 될 거야.",
    "뗏목을 다 만들면 꼭 떠나. 나처럼 되지 말고.",
    "가끔 생각해. 나는 왜 죽어서도 이 섬을 못 떠나는 걸까.",
]

game = {
    "day": 1,
    "energy": 10,
    "place": "해변",
    "trust": 0,            # 윤서와의 신뢰도
    "talked_today": False,
    "bag": {},             # 물건 이름 -> 개수
    "diary": [],           # 찾은 일지 조각
    "visited": {"해변"},   # 한 번이라도 가 본 장소
    "revealed": False,     # 숨겨진 조건이 드러났는가
    "buried": False,       # 윤서의 유골을 묻어 주었는가
    "running": True,
}


# ===== 화면 / 입력 도우미 =====
def show_status():
    update_status()
    show_picture(PLACE_IMAGES[game["place"]], game["place"])


def choose(title, options):
    """options: [(키, 설명), ...] 를 버튼으로 보여 주고, 누른 버튼의 키를 돌려준다."""
    if ui["closed"]:
        return None
    update_status()
    ui["question"].config(text=title)
    for old in ui["buttons"].winfo_children():
        old.destroy()
    ui["options"] = options
    for i, (_, text) in enumerate(options):
        tk.Button(ui["buttons"], text=f"{i + 1}. {text}", anchor="w", justify="left",
                  wraplength=190, font=(FONT, 10), bg=BUTTON, fg=TEXT,
                  activebackground="#4a5361", activeforeground=TEXT, relief="flat",
                  padx=8, pady=4, command=lambda i=i: ui["picked"].set(i)
                  ).grid(row=i // 2, column=i % 2, sticky="ew", padx=2, pady=2)

    ui["root"].wait_variable(ui["picked"])  # 버튼을 누를 때까지 기다린다
    if ui["closed"]:
        return None
    key, text = options[ui["picked"].get()]
    say(f"\n▶ {text}", "choice")
    return key


def add_item(name, count=1):
    game["bag"][name] = game["bag"].get(name, 0) + count


def has(name, count=1):
    return game["bag"].get(name, 0) >= count


def remove_item(name, count=1):
    game["bag"][name] -= count
    if game["bag"][name] <= 0:
        del game["bag"][name]


def use_energy(amount):
    game["energy"] -= amount
    if game["energy"] <= 0:
        say("\n눈앞이 캄캄해진다... 당신은 그 자리에서 쓰러졌다.")
        # 뗏목, 유골, 횃불은 너무 중요해서 잃어버리지 않게 한다
        losable = [name for name in game["bag"]
                   if name not in ("뗏목", "유골", "횃불")]
        if losable:
            lost = random.choice(losable)
            remove_item(lost)
            say(f"정신을 차려 보니 {lost} 하나가 사라졌다...")
        next_day(3)


def next_day(energy):
    game["day"] += 1
    game["energy"] = energy
    game["talked_today"] = False
    say(f"\n☀ {game['day']}일째 아침이 밝았다.")
    if game["day"] > DAY_LIMIT:
        bad_ending()
    else:
        fog_morning()


def fog_morning():
    """날짜가 지날수록 안개가 주인공을 집어삼키는 아침 묘사"""
    if game["buried"]:
        say("안개가 걷힌 맑은 아침이다. 몸이 한결 가볍다.")
        return
    day = game["day"]
    for start, lines, warning in reversed(FOG_STAGES):
        if day >= start:
            say(random.choice(lines))
            if day == start and warning:
                say(warning)
            break


# ===== 핵심 기능 1: 이동과 탐색 =====
def move():
    options = [(p, p) for p in PLACES if p != game["place"]]
    options.append((None, "취소"))
    dest = choose("어디로 갈까?", options)
    if dest is None:
        return
    game["place"] = dest
    say(f"\n{dest}(으)로 이동했다. {PLACES[dest]}")

    first_visit = dest not in game["visited"]
    if first_visit:
        game["visited"].add(dest)
        say(f"윤서: \"{FIRST_VISIT[dest]}\"")
    place_hint(dest)
    if not first_visit and random.random() < 0.35:
        travel_event()

    day = game["day"]
    use_energy(1)
    if game["day"] == day and game["running"] and random.random() < 0.05:
        animal_encounter()


def animal_encounter():
    """큰 동물과 마주치는 사건. 기절했거나 게임이 끝났으면 True를 돌려준다."""
    appear, run_text, win_text, lose_text = ANIMALS[game["place"]]
    say(f"\n{appear}")
    action = choose("어떻게 할까?", [
        ("run", "도망친다 (체력 -1)"),
        ("fight", f"맞서 싸운다 (체력 -2, 승률 {int(FIGHT_WIN_RATE * 100)}%, 이기면 고기)"),
    ])
    if action is None:
        return True
    if action == "run":
        say(f"\n{run_text} (체력 -1)")
        damage = 1
    elif random.random() < FIGHT_WIN_RATE:
        add_item("고기")
        say(f"\n{win_text} 고기를 얻었다! (체력 -2)")
        damage = 2
    else:
        say(f"\n{lose_text} 결국 도망칠 수밖에 없었다. (체력 -2)")
        damage = 2

    day = game["day"]
    use_energy(damage)
    return game["day"] != day or not game["running"]


def place_hint(place):
    """윤서가 이 장소에서 탐색하면 얻을 수 있는 것을 알려 준다."""
    if place == "동굴":
        if not has("횃불"):
            hint = "여긴 너무 어두워. 횃불 없이는 안쪽에 못 들어가."
        elif game["revealed"] and not has("유골") and not game["buried"]:
            hint = "가장 안쪽... 내가 있는 곳이야."
        else:
            hint = "여긴 주울 만한 건 없어."
    else:
        items = [item for item in dict.fromkeys(LOOT[place]) if item]
        hint = f"이 근처엔 {', '.join(items)} 같은 게 있어."
        if DIARY[place] not in game["diary"]:
            hint += " 그리고... 내 일지가 어디 떨어져 있을지도 몰라."
    say(f"윤서: \"{hint}\"")


def travel_event():
    """이동 중에 일어나는 랜덤 사건"""
    event = random.choice(["item", "trip", "memory", "wind"])
    if event == "item":
        found = random.choice(["나무판자", "덩굴", "나뭇가지", "열매"])
        add_item(found)
        say(f"\n가는 길에 {found}을(를) 주웠다!")
    elif event == "trip":
        say("\n돌부리에 걸려 넘어졌다! 무릎이 욱신거린다. (체력 -1)")
        game["energy"] -= 1
    elif event == "memory":
        say("\n윤서가 갑자기 멈춰 서서 먼 곳을 본다.")
        say("윤서: \"...방금 엄마 목소리가 들린 것 같았어. 착각이겠지.\"")
        if game["trust"] < MAX_TRUST:
            game["trust"] += 1
            say("(윤서가 마음을 조금 열었다.)")
    else:
        if game["revealed"] and not game["buried"]:
            say("\n바다 쪽에서 안개가 스멀스멀 몰려온다. 섬이 지켜보는 것 같다.")
        else:
            say("\n시원한 바닷바람이 분다. 기분이 조금 나아졌다. (체력 +1)")
            game["energy"] = min(10, game["energy"] + 1)


def search():
    place = game["place"]
    day = game["day"]
    use_energy(1)
    if game["day"] != day or not game["running"]:
        return

    # 수색하다가 큰 동물과 마주칠 수 있다
    if random.random() < 0.10 and animal_encounter():
        return

    if place == "동굴":
        search_cave()
        return

    # 아직 못 찾은 일지 조각이 있으면 일정 확률로 발견
    page = DIARY[place]
    if page not in game["diary"] and random.random() < 0.35:
        game["diary"].append(page)
        say("\n낡은 종이 한 장을 주웠다. 윤서의 글씨다.")
        say("  " + page)
        return

    found = random.choice(LOOT[place])
    if found:
        add_item(found)
        say(f"\n{found}을(를) 찾았다!")
    else:
        say("\n한참 뒤졌지만 쓸 만한 건 없었다.")


def search_cave():
    if not has("횃불"):
        say("\n너무 어두워서 안쪽으로 들어갈 수가 없다. 불빛이 필요하다.")
    elif not game["revealed"]:
        say("\n횃불을 들고 깊숙이 들어가자, 바위 틈에 하얀 무언가가 보인다.")
        say("윤서: \"...거긴 보지 마. 아직은.\"")
        say("윤서가 앞을 막아선다. 당신은 발걸음을 돌렸다.")
    elif not has("유골") and not game["buried"]:
        add_item("유골")
        game["diary"].append(LAST_PAGE)
        say("\n바위 틈에서 유골과 찢어진 일지 한 장을 찾았다.")
        say("  " + LAST_PAGE)
        say("윤서: \"...그게 나야. 언덕에 묻어 줄래? 오두막 앞이 좋겠어.\"")
    else:
        say("\n동굴은 조용하다. 더 이상 찾을 것은 없다.")


# ===== 핵심 기능 2: 유령과 대화 =====
def talk():
    if game["buried"]:
        line_text = "고마워. 이제 바람 소리가 무섭지 않아. 해변에서 기다릴게."
    elif game["revealed"] and has("유골"):
        line_text = "언덕 위 오두막 앞... 거기라면 바다가 보이거든."
    elif game["revealed"]:
        line_text = ("동굴 가장 깊은 곳. 그때 내가 막아섰던 곳 말이야. "
                     "...사실 보여주기 무서웠어.")
    else:
        line_text = GHOST_LINES[min(game["trust"], len(GHOST_LINES) - 1)]
    say(f"\n윤서: \"{line_text}\"")

    if not game["talked_today"]:
        game["talked_today"] = True
        if game["trust"] < MAX_TRUST:
            # 신뢰도가 높을수록 더 가까워지기 어렵다
            if random.random() < TRUST_UP_CHANCE[game["trust"]]:
                game["trust"] += 1
                say("(윤서와 조금 가까워진 것 같다.)")
            else:
                say("(윤서는 아직 마음을 다 열지 않은 것 같다.)")


# ===== 핵심 기능 3: 제작 / 가방 =====
def craft():
    options = []
    for item, needs in RECIPES.items():
        need_text = ", ".join(f"{k} {v}" for k, v in needs.items())
        options.append((item, f"{item}  ({need_text})"))
    options.append((None, "취소"))
    item = choose("무엇을 만들까? (체력 2 소모)", options)
    if item is None:
        return

    needs = RECIPES[item]
    if not all(has(k, v) for k, v in needs.items()):
        say("\n재료가 부족하다.")
        return
    for k, v in needs.items():
        remove_item(k, v)
    add_item(item)
    say(f"\n{item}을(를) 만들었다!")
    use_energy(2)


def view_bag():
    say("\n[가방]")
    if game["bag"]:
        for name, count in game["bag"].items():
            say(f"  - {name} x{count}")
    else:
        say("  (비어 있음)")
    say("[일지 조각]")
    if game["diary"]:
        for page in game["diary"]:
            say("  " + page)
    else:
        say("  (아직 없음)")


def eat(food):
    remove_item(food)
    amount = FOODS[food]
    game["energy"] = min(10, game["energy"] + amount)
    if food == "고기":
        say(f"\n고기를 구워 먹었다. 든든하다! (체력 +{amount})")
    else:
        say(f"\n열매를 먹었다. 달콤하다. (체력 +{amount})")


def rest():
    if game["place"] == "언덕":
        say("\n오두막에서 잠자리에 들었다.")
        recover = 10
    else:
        say("\n바닥에서 웅크리고 잠자리에 들었다.")
        recover = 7

    if has("횃불"):
        # 횃불이 있으면 반드시 모닥불을 피운다 (연기 덕분에 모기도 없다)
        say("횃불로 모닥불을 피웠다. 따뜻한 불빛 덕분에 푹 잤다. (회복량 +2)")
        recover += 2
    elif game["place"] != "언덕" and random.random() < 0.3:
        # 오두막 안에서는 모기가 없다
        say("밤새 모기가 앵앵거린다... 잠을 설쳤다. (회복량 -2)")
        recover -= 2
    next_day(min(10, recover))


# ===== 돌발 상황: 숨겨진 조건 =====
def try_escape():
    say("\n뗏목을 밀고 바다로 나아간다...")
    if game["buried"]:
        ending()
        return

    say("한참을 노 저었을 때, 갑자기 짙은 안개가 몰려왔다.")
    say("정신을 차려 보니... 다시 섬의 해변이다.")
    use_energy(3)
    if not game["running"]:
        return

    if not game["revealed"]:
        game["revealed"] = True
        say("\n" + "!" * 30)
        say(" 숨겨져 있던 조건이 드러났다")
        say("!" * 30)
        say("윤서: \"...역시. 나도 그랬어. 몇 번을 나가도 안개가 돌려보냈지.\"")
        say("윤서: \"이제야 알겠어. 이 섬은 묻히지 못한 자가 있는 한")
        say("       아무도 보내주지 않아. 그리고 그 묻히지 못한 자는...\"")
        say("윤서: \"나야. 내 몸은 아직 동굴 깊은 곳에 있어.\"")
        say("\n[새 목표] 동굴에서 윤서의 유골을 찾아 언덕에 묻어 주자.")
    else:
        say("윤서: \"내가 아직 묻히지 않았으니까... 미안해.\"")


def bury():
    remove_item("유골")
    game["buried"] = True
    say("\n오두막 앞, 바다가 보이는 자리에 윤서를 묻었다.")
    say("작은 돌을 쌓아 무덤을 만들자, 섬을 감싸던 안개가 천천히 걷힌다.")
    say("윤서: \"...따뜻하다. 이제 갈 수 있겠어. 너도, 나도.\"")
    if game["trust"] < MAX_TRUST:
        game["trust"] += 1
        say("(윤서와 한층 가까워졌다.)")
    use_energy(2)


# ===== 엔딩 =====
def ending():
    say("\n안개는 더 이상 오지 않았다. 수평선 너머로 배 한 척이 보인다.")
    if game["trust"] >= MAX_TRUST:
        say("뒤를 돌아보니, 해변에서 윤서가 손을 흔들고 있다.")
        say("윤서: \"잘 가. 그리고... 고마웠어, 친구.\"")
        say("윤서의 모습이 햇빛 속으로 부서지듯 사라졌다.")
        say(f"\n★ 진엔딩: 두 사람의 귀환 ({game['day']}일 만에 탈출)")
        show_image("ending_true.png", "진엔딩: 두 사람의 귀환")
    else:
        say("섬을 돌아보았지만, 윤서의 모습은 보이지 않았다.")
        say(f"\n☆ 엔딩: 홀로 떠난 섬 ({game['day']}일 만에 탈출)")
        show_image("ending_normal.png", "엔딩: 홀로 떠난 섬")
    game["running"] = False


def bad_ending():
    say("\n너무 오랜 시간이 흘렀다. 몸에 힘이 들어가지 않는다.")
    say("윤서: \"...이제 외롭진 않겠네.\"")
    say("\n✖ 배드엔딩: 섬의 두 번째 유령")
    show_image("ending_bad.png", "배드엔딩: 섬의 두 번째 유령")
    game["running"] = False


def show_image(filename, title):
    """엔딩 그림을 띄운다."""
    show_picture(filename, title)
    ui["ending_shown"] = True


# ===== 게임 창 =====
# 왼쪽: 장소 그림 / 오른쪽: 상태, 이야기, 선택 버튼
FONT = "맑은 고딕"
BG = "#1e2228"       # 창 배경
PANEL = "#2a2f37"    # 상태·이야기 칸 배경
TEXT = "#e8e6e3"     # 기본 글자
GHOST = "#9fc3ff"    # 윤서의 대사
ALERT = "#ff9a8a"    # 중요한 알림
MUTED = "#8a929c"    # 내가 고른 선택
BUTTON = "#3a414c"

ui = {"images": {}, "closed": False, "ending_shown": False}


def build_window():
    root = tk.Tk()
    root.title("유령의 섬")
    root.configure(bg=BG)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.bind("<Key>", on_key)  # 숫자 키로도 고를 수 있다
    ui["root"] = root
    ui["picked"] = tk.IntVar(value=-1)

    left = tk.Frame(root, bg=BG)
    left.pack(side="left", anchor="n", padx=(12, 6), pady=12)
    ui["picture"] = tk.Label(left, bg=BG)
    ui["picture"].pack()
    ui["caption"] = tk.Label(left, font=(FONT, 13, "bold"), bg=BG, fg=TEXT, pady=4)
    ui["caption"].pack()

    right = tk.Frame(root, bg=BG, width=430)
    right.pack(side="left", fill="y", padx=(6, 12), pady=12)
    ui["status"] = tk.Label(right, font=(FONT, 11, "bold"), bg=PANEL, fg=TEXT,
                            anchor="w", justify="left", padx=10, pady=8)
    ui["status"].pack(fill="x")

    log_frame = tk.Frame(right, bg=BG)
    log_frame.pack(fill="both", expand=True, pady=8)
    ui["log"] = tk.Text(log_frame, width=48, height=15, wrap="word", font=(FONT, 10),
                        bg=PANEL, fg=TEXT, relief="flat", padx=10, pady=8, state="disabled")
    scroll = tk.Scrollbar(log_frame, command=ui["log"].yview)
    ui["log"]["yscrollcommand"] = scroll.set
    ui["log"].pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    ui["log"].tag_config("ghost", foreground=GHOST)
    ui["log"].tag_config("alert", foreground=ALERT, font=(FONT, 10, "bold"))
    ui["log"].tag_config("choice", foreground=MUTED)

    ui["question"] = tk.Label(right, font=(FONT, 11, "bold"), bg=BG, fg=TEXT, anchor="w")
    ui["question"].pack(fill="x")
    ui["buttons"] = tk.Frame(right, bg=BG)
    ui["buttons"].pack(fill="x")
    ui["buttons"].columnconfigure(0, weight=1, uniform="col")
    ui["buttons"].columnconfigure(1, weight=1, uniform="col")


def say(text="", tag=None):
    """이야기 칸에 한 줄을 쓴다. 윤서의 대사와 중요한 알림은 색을 바꾼다."""
    if tag is None:
        stripped = text.strip()
        if stripped.startswith("윤서:"):
            tag = "ghost"
        elif stripped.startswith(("!", "★", "☆", "✖", "[새 목표]", "숨겨져")):
            tag = "alert"
    log = ui["log"]
    log.config(state="normal")
    log.insert("end", text + "\n", tag or ())
    log.config(state="disabled")
    log.see("end")


def update_status():
    hearts = "♥" * game["trust"] + "♡" * (MAX_TRUST - game["trust"])
    ui["status"].config(text=f"{game['day']}일째 (제한 {DAY_LIMIT}일)    체력 {game['energy']}/10\n"
                             f"위치: {game['place']}    윤서 신뢰도 {hearts}")


def load_image(filename):
    """그림 파일을 불러온다. 한 번 불러온 그림은 다시 쓴다. 없으면 None."""
    if filename not in ui["images"]:
        path = os.path.join(IMAGE_DIR, filename)
        image = None
        if os.path.exists(path):
            try:
                image = tk.PhotoImage(file=path)
                # 그림이 너무 크면 줄인다 (최대 가로 800, 세로 600 정도)
                shrink = max(1, -(-image.width() // 800), -(-image.height() // 600))
                image = image.subsample(shrink)
            except tk.TclError:
                say(f"({filename} 그림을 열 수 없습니다. PNG 파일인지 확인해 주세요.)")
        ui["images"][filename] = image
    return ui["images"][filename]


def show_picture(filename, caption):
    ui["picture"].config(image=load_image(filename) or "")
    ui["caption"].config(text=caption)


def on_key(event):
    if event.char.isdigit() and 1 <= int(event.char) <= len(ui.get("options", [])):
        ui["picked"].set(int(event.char) - 1)


def on_close():
    """창의 X 버튼: 기다리던 선택을 풀어 주고 게임을 끝낸다."""
    ui["closed"] = True
    game["running"] = False
    ui["picked"].set(-1)


# ===== 메인 루프 =====
def intro():
    say("폭풍우에 배가 뒤집혔다. 눈을 떠 보니 낯선 해변이다.")
    say("그때, 반투명한 사람이 당신을 내려다보고 있었다.")
    say(f"\n목표: {DAY_LIMIT}일 안에 이 섬을 탈출하라.", "alert")
    say("팁: 윤서와 매일 대화하면 힌트를 얻고 신뢰도가 올라갑니다.")


def main():
    build_window()
    intro()
    while game["running"]:
        show_status()
        options = [
            ("move", "다른 장소로 이동 (체력 1)"),
            ("search", "주변 탐색 (체력 1)"),
            ("talk", "유령 윤서와 대화"),
            ("craft", "물건 만들기"),
            ("bag", "가방 / 일지 보기"),
        ]
        for food, amount in FOODS.items():
            if has(food):
                options.append((food, f"{food} 먹기 (체력 +{amount})"))
        if game["place"] == "언덕" and has("유골"):
            options.append(("bury", "윤서의 유골 묻어 주기"))
        if game["place"] == "해변" and has("뗏목"):
            options.append(("escape", "뗏목을 타고 탈출 시도"))
        options.append(("rest", "잠자기 (다음 날로)"))
        options.append(("quit", "게임 종료"))

        action = choose("무엇을 할까?", options)
        if action is None or action == "quit":
            say("\n게임을 종료합니다.")
            break
        if action in FOODS:
            eat(action)
            continue

        actions = {
            "move": move, "search": search, "talk": talk, "craft": craft,
            "bag": view_bag, "bury": bury,
            "escape": try_escape, "rest": rest,
        }
        actions[action]()

    # 엔딩을 봤으면 창을 닫기 전에 그림을 감상할 수 있게 한다
    if ui["ending_shown"] and not ui["closed"]:
        choose("게임이 끝났습니다.", [("close", "창 닫기")])
    ui["root"].destroy()


if __name__ == "__main__":
    main()
