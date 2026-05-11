"""

!apt-get update
!apt-get install -y ffmpeg freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev libpng-dev libjpeg-dev libcairo2-dev libpango1.0-dev texlive-latex-base texlive-fonts-recommended texlive-latex-extra dvisvgm xvfb

!apt-get install -y texlive-lang-other

!pip install gtts

!pip install manim manim-voiceover arcade

"""## Import & Setup GPU headless display"""

import os
import random
import networkx as nx

import gtts
import manim_voiceover.services.gtts

# Ép thư viện nhận diện đúng class gTTS và lỗi gTTSError
manim_voiceover.services.gtts.gTTS = gtts.gTTS
manim_voiceover.services.gtts.gTTSError = gtts.gTTSError

from manim import *
from manim.opengl import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

display_port = random.randint(100, 500)
os.system(f"Xvfb :{display_port} -screen 0 1920x1080x24 -ac &")
time.sleep(2)
os.environ["DISPLAY"] = f":{display_port}"
# os.system("Xvfb :1 -screen 0 1024x768x24 &")
# os.environ["DISPLAY"] = ":1"

"""## Globals"""

# --- COLORS ---
class B3B1B:
    BLUE = "#58C4DD"
    GREEN = "#83C167"
    YELLOW = "#FFFF00"
    GOLD = "#C59911"
    RED = "#FC6255"
    MAROON = "#C55F73"
    PURPLE = "#9472AF"
    TEAL = "#5CD0B3"
    ORANGE = "#FF862F"
    LIGHT_GRAY = "#BBBBBB"
    DARK_GRAY = "#888888"
    DARKER_GRAY = "#444444"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    PEACH = "#FF6B6B"

def get_vn_template():
    return TexTemplate(preamble=r"\usepackage[T5]{fontenc} \usepackage[utf8]{inputenc}")

# --- CONSTANTS ---
MAIN_FONT = "Liberation Sans"

# --- HELPERS ---

def get_colors():
    return {"primary": B3B1B.BLUE, "secondary": B3B1B.GOLD, "text": B3B1B.LIGHT_GRAY}

def create_footer():
    # Grant uses small, subtle grey text for footers
    return Tex(
        r"Nhóm 01 - Khoa học dữ liệu ứng dụng",
        font_size=18,
        color=B3B1B.DARK_GRAY,
        tex_template=get_vn_template()
    ).to_edge(DR)

"""## Scene 1

### mo_objs
"""

def create_intro_moobj():
    # Sử dụng Tex để có font chữ 3b1b chuẩn
    line1 = Tex(
        r"The b2biers System:",
        color=get_colors()["secondary"],
        tex_template=get_vn_template()
    )
    line2 = Tex(
        r"A Context-based Perspective",
        font_size=34,
        tex_template=get_vn_template()
    )
    names = Tex(
        r"Nguyễn Lê Tuấn Khải \& Nguyễn Văn Phúc",
        font_size=28,
        color=B3B1B.DARK_GRAY,
        tex_template=get_vn_template()
    )

    return VGroup(line1, line2, names).arrange(DOWN, buff=0.8)

"""### actions"""

def play_intro_sequence(scene):
    intro = create_intro_moobj()
    # Hiệu ứng FadeIn + shift đặc trưng 3b1b
    speech_doc = "Chào thầy và các bạn. Hôm nay, chúng mình, nhóm một, gồm Nguyễn Lê Tuấn Khải và Nguyễn Văn Phúc xin được trình bày về hệ thống b2biers"
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(
            FadeIn(intro, shift=UP * 0.3, lag_ratio=0.1),
            run_time=2
        )
        remaining_time = 0.5 if tracker.duration < 2 else tracker.duration - 2
        scene.wait(remaining_time)

    scene.play(FadeOut(intro, shift=UP * 0.2))

"""## Chef mascot

### mo_objs
"""

def create_chef(body_color=B3B1B.RED, color=B3B1B.DARKER_GRAY, scale_factor=1.0):
    body = RoundedRectangle(
        corner_radius=0.4, height=2.5, width=1.4, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1
    )

    # Mũ
    hat_neck = Rectangle(width=0.5, height=0.7, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(body.get_top() + UP*0.3)
    hat_top = VGroup(*[
        Circle(radius=0.3, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + LEFT*0.3),
        Circle(radius=0.35, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + UP*0.2),
        Circle(radius=0.3, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + RIGHT*0.3),
    ])

    # Mắt & Mũi
    eyes = VGroup(
        Ellipse(width=0.4, height=0.15, color=color, fill_color=color, fill_opacity=1),
        Ellipse(width=0.4, height=0.15, color=color, fill_color=color, fill_opacity=1)
    ).arrange(RIGHT, buff=0.15).move_to(body.get_center() + UP*0.7)

    nose = Rectangle(width=0.3, height=0.15, color=color, fill_opacity=1).move_to(body.get_center() + UP*0.2)

    # Miệng buồn
    mouth = Arc(
        radius=0.4,
        start_angle=PI/3,
        angle=PI/3,
        color=color,
        stroke_width=6
    ).move_to(body.get_center() + DOWN*0.4)

    # --- GIẢI PHÁP SỬA LỖI TẠI ĐÂY ---
    # Chúng ta bỏ tất cả vào một danh sách
    all_parts = [body, hat_neck, hat_top, eyes, nose, mouth]

    # Tạo một Group "trống" trước
    chef = Group()

    # Ép kiểu từng bộ phận theo renderer hiện tại của máy bạn
    for part in all_parts:
        chef.add(part)

    chef.scale(scale_factor)

    chef.mouth = chef[-1]

    return chef

"""### actions"""

def chef_appear(scene, x=None, y=None, direction=DOWN, wait_time=0.3):
    if x is None and y is None:
        pos = ORIGIN
    else:
        pos = np.array([x, y, 0])

    chef = create_chef(scale_factor=0.4)
    chef.move_to(pos)

    scene.play(
        FadeIn(chef, shift=direction * 0.5),
        run_time=0.8
    )

    scene.wait(wait_time)
    return chef

def chef_talk(chef, speed=10):
    if not hasattr(chef, "original_mouth_points"):
        chef.original_mouth_points = chef.mouth.points.copy()

    def update_mouth(m, dt):
        if not hasattr(m, "talking_time"):
            m.talking_time = 0
        m.talking_time += dt

        oscillation = np.sin(m.talking_time * speed)
        scale_val = 0.9 + 0.6 * oscillation

        m.set_points(chef.original_mouth_points)

        m.stretch(scale_val, dim=1, about_point=m.get_center())

    chef.mouth.clear_updaters()
    chef.mouth.add_updater(update_mouth)

def chef_silent(chef):
    chef.mouth.clear_updaters()
    if hasattr(chef, "original_mouth_path"):
        chef.mouth.set_points(chef.original_mouth_path)

"""## Store

### mo_objs
"""

def create_store_moobj(scale_factor=.5):
    # 1. Thân cửa hàng
    wall = Rectangle(width=5, height=3, fill_opacity=1, color="#F3E5AB") # Màu kem
    wall.set_stroke(WHITE, 2)

    # 2. Awning (Mái che)
    # Red and white striped awnings
    awning_strips = VGroup(*[
        Rectangle(width=0.5, height=1, fill_opacity=1, color=res)
        for res in [B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE]
    ]).arrange(RIGHT, buff=0)
    awning_strips.next_to(wall.get_top(), DOWN, buff=0)

    # 3. Doors
    door = Rectangle(width=1, height=1.5, fill_opacity=1, color="#8B4513") # Màu gỗ
    door.align_to(wall, DOWN).shift(LEFT * 1)

    # 4. Windows
    window = Square(side_length=1, fill_opacity=1, color=BLUE_B)
    window.set_stroke(WHITE, 2)
    window.shift(RIGHT * 1.2 + DOWN * 0.4)

    # Window panes (divided into 4)
    cross_h = Line(window.get_left(), window.get_right())
    cross_v = Line(window.get_top(), window.get_bottom())
    window_panes = VGroup(window, cross_h, cross_v)

    # 5. Sign (Biển hiệu)
    sign_board = Rectangle(width=3, height=0.7, fill_opacity=1, color=B3B1B.DARK_GRAY)
    sign_board.next_to(wall, UP, buff=0.1)
    sign_text = Text("STORE", font_size=24, color=B3B1B.WHITE).move_to(sign_board)
    shop_sign = VGroup(sign_board, sign_text)

    # Group them all as "Storefront"
    store = VGroup(wall, awning_strips, door, window_panes, shop_sign).scale(scale_factor)

    return store

def create_sell_obj(store_mobject, image_path="gomugomu.svg"):
    try:
        gomu_image = SVGMobject(image_path)
    except FileNotFoundError:
        gomu_image = VGroup(
            Square(side_length=1, color=B3B1B.RED, fill_opacity=0.5),
            Text("File ảnh\nlỗi!", font_size=16, color=B3B1B.WHITE).scale(0.5)
        )
        print(f"Lỗi: Không tìm thấy file ảnh tại {image_path}. Vui lòng kiểm tra lại.")

    gomu_image.scale(0.2)

    # 2. Create Speech Bubble
    speech_bubble_body = Ellipse(
        width=gomu_image.width + 1,
        height=gomu_image.height + .6,
        stroke_color=B3B1B.PEACH,
        stroke_width=4,
        fill_color=B3B1B.WHITE,
        fill_opacity=1,
    )

    # Create Bubble tail
    bubble_tail = VGroup(*[
        Circle(radius=0.2, fill_color=B3B1B.WHITE, fill_opacity=1,).scale(0.5**i).set_stroke(B3B1B.PEACH, 4-i)
        for i in range(3)
    ])
    bubble_tail.arrange(DOWN+LEFT, buff=0.05)
    bubble_tail.next_to(speech_bubble_body, DOWN + LEFT, buff=-0.05).shift(LEFT * 0.2)

    bubble_frame = VGroup(speech_bubble_body, bubble_tail)

    # Put gomu fruit into bubble
    bubble_frame.next_to(store_mobject.get_top(), UR, buff=0.05)
    gomu_image.move_to(speech_bubble_body.get_center())

    return bubble_frame, gomu_image

"""### actions"""

def store_appear(scene, x=None, y=None, wait_time=1):
    if x is None and y is None:
        pos = ORIGIN
    else:
        pos = np.array([x, y, 0])

    store = create_store_moobj(scale_factor=.3)
    store.move_to(pos)

    scene.play(FadeIn(store, shift=DOWN*0.5))
    scene.wait(wait_time)

    return store

def sell_gomu_gomu_png(scene, store_mobject, image_path="gomugomu.svg", wait_times=[1,2]):
    bubble_frame, gomu_image = create_sell_obj(store_mobject, image_path)

    # Chat bubble effect shooting out from behind the shop
    scene.play(
        FadeIn(bubble_frame, scale=0.1, target_position=store_mobject),
        run_time=wait_times[0]
    )
    scene.add(gomu_image)

    scene.wait(wait_times[1])

    return bubble_frame, gomu_image

"""## Sence 2

### mo_objs
"""

def get_layered_nodes(nx_graph, start_node):
    """
    Trả về một danh sách các danh sách.
    Mỗi danh sách con chứa các node ở cùng một khoảng cách tính từ start_node.
    """
    layers = []
    visited = {start_node}
    current_layer = [start_node]

    while current_layer:
        layers.append(current_layer)
        next_layer = []
        for node in current_layer:
            # nx_graph.neighbors lấy tất cả những node kết nối trực tiếp
            for neighbor in nx_graph.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_layer.append(neighbor)
        current_layer = next_layer
    return layers

def create_so_graph():
    num_nodes = 150
    seed = 42
    random.seed(seed)

    so_graph = nx.barabasi_albert_graph(num_nodes, 2, seed=seed)
    centrality = nx.degree_centrality(so_graph)
    top_5_kols = sorted(centrality, key=centrality.get, reverse=True)[:5]

    remaining_nodes = [n for n in so_graph.nodes if n not in top_5_kols]
    store_node_index = random.choice(remaining_nodes)

    # Mo_objs
    graph_mo_obj = Graph(
        list(so_graph.nodes),
        list(so_graph.edges),
        layout="spring", # Bố cục lò xo giúp đồ thị trông tự nhiên
        layout_scale=4, # Phóng to đồ thị ra không gian rộng hơn
        labels=False,
        vertex_config={
            "radius": 0.08,
            "color": B3B1B.DARK_GRAY, # Đa số các node có màu xám
            "fill_opacity": 0.6,
            "stroke_width": 0
        },
        edge_config={
            "stroke_width": 0.5,
            "stroke_opacity": 0.3,
            "color": B3B1B.LIGHT_GRAY
        }
    )

    store_node = graph_mo_obj.vertices[store_node_index]
    store_node.set_color(B3B1B.BLUE).set_fill(opacity=1).set_stroke(width=2, color=B3B1B.WHITE).scale(1.1)

    other_vertices = VGroup(*[graph_mo_obj.vertices[i] for i in graph_mo_obj.vertices if i != store_node_index])
    edges = VGroup(*graph_mo_obj.edges.values())

    top_5_vertices = VGroup(*[graph_mo_obj.vertices[i] for i in top_5_kols])

    layers_store = get_layered_nodes(so_graph, store_node_index)
    the_big_kol = top_5_kols[0]
    layers_kol = get_layered_nodes(so_graph, the_big_kol)

    return graph_mo_obj, store_node, other_vertices, top_5_vertices, edges, layers_store, layers_kol

"""### actions"""

def store_node_appear(scene, store_node):
    scene.play(FadeIn(store_node), run_time=1)
    scene.wait(0.5)
    return store_node

def rest_graph_appear(scene, other_vertices, edges):
    scene.play(
        FadeIn(other_vertices, lag_ratio=0.01),
        FadeIn(edges, lag_ratio=0.01),
        run_time=2
    )
    scene.wait(0.5)
    return other_vertices, edges

def show_top_5(scene, top_5_vertices):
    def blink(mobj, dt):
        if not hasattr(mobj, "t"): mobj.t = 0
        mobj.t += dt
        new_opacity = 0.4 + 0.6 * np.abs(np.sin(mobj.t * 5))
        mobj.set_fill(color=B3B1B.GOLD, opacity=new_opacity)
        mobj.set_stroke(color=B3B1B.WHITE, width=2, opacity=new_opacity)

    for v in top_5_vertices:
        v.add_updater(blink)

    return top_5_vertices

def stop_top_5_blink(top_5_vertices):
    for v in top_5_vertices:
        v.clear_updaters()

    top_5_vertices[0].set_fill(opacity=1)
    top_5_vertices[0].set_stroke(width=0)
    for v in top_5_vertices[1:]:
        v.set_fill(color=B3B1B.DARK_GRAY, opacity=0.6)
        v.set_stroke(width=0)

# lan truyền
def promote_by_store(scene, graph_mo_obj, layers_store):
    for layer in layers_store[:2]:
        nodes = [graph_mo_obj.vertices[n] for n in layer]
        scene.play(
            *[n.animate.set_fill(BLUE, opacity=0.8) for n in nodes],
            run_time=1.8
        )
def promote_via_kol(scene, graph_mo_obj, layers_kol):
    for layer in layers_kol:
        nodes = [graph_mo_obj.vertices[n] for n in layer]
        # Tốc độ nhanh dần đều (exponentially faster)
        scene.play(
            *[n.animate.set_fill(RED, opacity=1).scale(1.1) for n in nodes],
            run_time=max(0.05, 0.5 * (0.7**layers_kol.index(layer)))
        )

# reset
def reset_graph_colors(scene, graph_mo_obj):
    all_vertices = graph_mo_obj.vertices
    animations = []

    for idx, v in all_vertices.items():
        animations.append(v.animate.set_fill(B3B1B.DARK_GRAY, opacity=0.6).scale(1))

    for edge in graph_mo_obj.edges.values():
        animations.append(edge.animate.set_stroke(color=B3B1B.LIGHT_GRAY, width=0.5, opacity=0.3))

    scene.play(*animations, run_time=0.5)

def impress_node(scene, node, type_='store'):
    if type_ == 'store':
        animation = Indicate(node, color=B3B1B.BLUE, scale_factor=1.2)
    if type_ == 'kol':
        animation = Indicate(node, color=B3B1B.GOLD, scale_factor=1.2)

    scene.play(animation, run_time=2)

# delete
def shrink_to_store(scene, graph_mo_obj, store_node):
    # Lấy tọa độ hiện tại của store node trên màn hình
    target_point = store_node.get_center()

    scene.play(
        # Toàn bộ đồ thị co cụm về vị trí của store node
        graph_mo_obj.animate.scale(0.001).move_to(target_point),
        run_time=1.5,
        rate_func=rate_functions.ease_in_back # Hiệu ứng nảy nhẹ tạo cảm giác bị hút vào
    )
    # Xóa hoàn toàn khỏi bộ nhớ render
    scene.remove(graph_mo_obj)

def play_context_sequence(scene, wait_times=[1.5,3]):
    # intro scene
    chef = chef_appear(scene, x=-6, y=-2, direction=RIGHT)

    chef_talk(chef)
    speech_doc = "Giả sử. Chúng ta bắt đầu với một cửa hàng bán kẹo trái cây nhỏ."
    with scene.voiceover(text=speech_doc) as tracker:
        store = store_appear(scene, x=-4,y=-1, wait_time=tracker.duration)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Và hiễn nhiên, mục tiêu của chúng ta là bán càng nhiều càng tốt. Vì vậy, chúng ta phải bắt đầu quảng bá nó."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Thông thường, chúng ta sẽ bắt đầu treo biển và hô bán tương tự những gì thị trường nguyên thủy."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Chúng ta hô bán, kẹo Gomu Gomu đây. Có ai mua nó không? Và kỳ vọng người khác nghe thấy và tới mua chúng."
    with scene.voiceover(text=speech_doc) as tracker:
        first_period = 1 if tracker.duration > 1 else 0.5
        remaining_time = 0.5 if tracker.duration < first_period else tracker.duration - first_period
        speech_bubble = sell_gomu_gomu_png(scene, store, wait_times=[first_period,remaining_time])
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Nhưng có vẻ cách này không mang lại hiệu quả cao cho lắm nếu bạn muốn bán được nhiều hơn."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    # graph scene
    graph_mo_obj, store_node, other_vertices, top_5_vertices, edges, layers_store, layers_kol = create_so_graph()
    graph_mo_obj.move_to(RIGHT*2.5)
    chef_talk(chef)
    speech_doc = "Vậy! Sao chúng ta không nhìn nhận thế giới này như một đồ thị? Dù là thông qua mạng truyền thông, hay mạng xã hội đi chăng nữa. Chúng ta cũng chỉ là một node của đồ thị."
    with scene.voiceover(text=speech_doc) as tracker:
        store_node= store_node_appear(scene, store_node)
        scene.wait(tracker.duration)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Chúng ta liên kết với các node khác bởi các quan hệ. Và nhu cầu của chúng ta không gì khác ngoài lan truyền tin tức kẹo Gomu Gomu đi càng xa càng tốt trong đồ thị."
    with scene.voiceover(text=speech_doc) as tracker:
        other_vertices, edges = rest_graph_appear(scene, other_vertices, edges)
        for _ in range(2):
            impress_node(scene, store_node, type_='store')
            promote_by_store(scene, graph_mo_obj, layers_store)
            scene.wait(tracker.duration/2)
            reset_graph_colors(scene, graph_mo_obj)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Nhưng vì bạn là một cửa hàng nhỏ, và chúng tôi giả định bạn cũng chỉ là một người bình thường. Và như vậy bạn không có ảnh hưởng lớn trong mạng đồ thị này. Thế nên có vẻ như thông điệp bạn lan truyền vẫn như cũ, khó có thể mà lan xa như kỳ vọng."
    with scene.voiceover(text=speech_doc) as tracker:
        for _ in range(4):
            impress_node(scene, store_node, type_='store')
            promote_by_store(scene, graph_mo_obj, layers_store)
            scene.wait(tracker.duration/4)
            reset_graph_colors(scene, graph_mo_obj)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Và đột nhiên, bạn liền nghĩ ra một ý tưởng rất thuận tự nhiên. Bạn sẽ thuê những người có ảnh hưởng để làm việc đó thay bạn. Chính xác hơn chính là thuê họ để họ dùng cái sự ảnh hưởng của mình mà lan truyền thông điệp của bạn đến tai mắt của khách hàng."
    with scene.voiceover(text=speech_doc) as tracker:
        show_top_5(scene, top_5_vertices)
        scene.wait(tracker.duration)
    chef_silent(chef)

    stop_top_5_blink(top_5_vertices)


    chef_talk(chef)
    speech_doc = "Tất nhiên điều đó vô cùng hiệu quả. Các nhà tạo ảnh hưởng, miễn là họ có đủ lợi ích, thông điệp của bạn sẽ truyền đi rất nhanh, thậm chí tạo thành điểm nhấn."
    with scene.voiceover(text=speech_doc) as tracker:
        for _ in range(2):
            impress_node(scene, top_5_vertices[0], type_='kol')
            promote_via_kol(scene, graph_mo_obj, layers_kol)
            scene.wait(tracker.duration/3)
            reset_graph_colors(scene, graph_mo_obj)

    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Nhưng khoan đã. Bạn có chắc đây là việc làm đúng đắn chứ?"
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    shrink_to_store(scene, graph_mo_obj, store_node)

    chef_talk(chef)
    speech_doc = "Hãy xem lại túi tiền của mình nào!"
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

"""## Run (The Orchestrator)"""

class FullPresentation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="vi"))

        # Grant Sanderson dùng nền đen tuyền
        self.camera.background_color = B3B1B.BLACK

        # Thêm Footer tinh tế
        footer = create_footer()
        self.add(footer)

        # --- SCENE 1: GIỚI THIỆU ---
        self.next_section("Introduction")
        play_intro_sequence(self)

        # --- SCENE 2: BỐI CẢNH ---
        self.next_section("Context & Motivation")
        play_context_sequence(self, wait_times=[0.5,3])

        self.wait(1)

"""## BUILD"""

# Commented out IPython magic to ensure Python compatibility.
# Render command (change -qm to -qh for high quality)
# %manim -qh --renderer=opengl --write_to_movie --disable_caching FullPresentation
