"""

!apt-get update
!apt-get install -y ffmpeg freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev libpng-dev libjpeg-dev libcairo2-dev libpango1.0-dev texlive-latex-base texlive-fonts-recommended texlive-latex-extra dvisvgm xvfb

!apt-get install -y texlive-lang-other

!pip install gtts

!pip install manim manim-voiceover arcade

"""
import os
import random
import time
import numpy as np
import networkx as nx

import gtts
import manim_voiceover.services.gtts

# Force the library to correctly recognize the gTTS class and gTTSError to fix a bug in manim-voiceover
manim_voiceover.services.gtts.gTTS = gtts.gTTS
manim_voiceover.services.gtts.gTTSError = gtts.gTTSError

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

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

############################################################################################
## Scene 1
############################################################################################

##############################################
### Mobjects
##############################################
def create_intro_mobject():
    # Use Tex for standard 3b1b font style
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
        # r"Nguyễn Lê Tuấn Khải \& Nguyễn Văn Phúc",
        r"Nguyễn Lê Tuấn Khải",
        font_size=28,
        color=B3B1B.DARK_GRAY,
        tex_template=get_vn_template()
    )

    return VGroup(line1, line2, names).arrange(DOWN, buff=0.8)

##############################################
### Actions"""
##############################################

def play_intro_sequence(scene):
    intro = create_intro_mobject()
    # 3b1b signature FadeIn + shift effect
    # speech_doc = "Chào thầy và các bạn. Hôm nay, chúng mình, nhóm một, gồm Nguyễn Lê Tuấn Khải và Nguyễn Văn Phúc xin được trình bày về hệ thống b2biers"
    speech_doc = "Chào thầy và các bạn. Hôm nay, chúng mình, nhóm một, gồm Nguyễn Lê Tuấn Khải hôm nay xin được trình bày cùng thầy và các bạn về hệ thống b2biers"
    
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(
            FadeIn(intro, shift=UP * 0.3, lag_ratio=0.1),
            run_time=2
        )
        remaining_time = 0.5 if tracker.duration < 2 else tracker.duration - 2
        scene.wait(remaining_time)

    scene.play(FadeOut(intro, shift=UP * 0.2))

##############################################
## Chef Mascot
##############################################

##############################################
### Mobjects
##############################################
def create_chef(body_color=B3B1B.RED, accent_color=B3B1B.DARKER_GRAY, scale_factor=1.0):
    body = RoundedRectangle(
        corner_radius=0.4, height=2.5, width=1.4, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1
    )

    # Hat
    hat_neck = Rectangle(width=0.5, height=0.7, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(body.get_top() + UP*0.3)
    hat_top = VGroup(*[
        Circle(radius=0.3, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + LEFT*0.3),
        Circle(radius=0.35, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + UP*0.2),
        Circle(radius=0.3, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + RIGHT*0.3),
    ])

    # Eyes & Nose
    eyes = VGroup(
        Ellipse(width=0.4, height=0.15, color=accent_color, fill_color=accent_color, fill_opacity=1),
        Ellipse(width=0.4, height=0.15, color=accent_color, fill_color=accent_color, fill_opacity=1)
    ).arrange(RIGHT, buff=0.15).move_to(body.get_center() + UP*0.7)

    nose = Rectangle(width=0.3, height=0.15, color=accent_color, fill_opacity=1).move_to(body.get_center() + UP*0.2)

    # Sad Mouth
    mouth = Arc(
        radius=0.4,
        start_angle=PI/3,
        angle=PI/3,
        color=accent_color,
        stroke_width=6
    ).move_to(body.get_center() + DOWN*0.4)

    # Workaround for Cairo Render
    all_parts = [body, hat_neck, hat_top, eyes, nose, mouth]

    chef = VGroup()
    for part in all_parts:
        chef.add(part)

    chef.scale(scale_factor)
    chef.mouth = chef[-1]

    return chef

##############################################
### Actions"""
##############################################
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
    if hasattr(chef, "original_mouth_points"):
        chef.mouth.set_points(chef.original_mouth_points)

##############################################
## Store
##############################################

##############################################
### Mobjects
##############################################
def create_store_mobject(scale_factor=.5):
    # 1. Store Body
    wall = Rectangle(width=5, height=3, fill_opacity=1, color="#F3E5AB") # Cream color
    wall.set_stroke(WHITE, 2)

    # 2. Awning
    awning_strips = VGroup(*[
        Rectangle(width=0.5, height=1, fill_opacity=1, color=res)
        for res in [B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE, B3B1B.RED, B3B1B.WHITE]
    ]).arrange(RIGHT, buff=0)
    awning_strips.next_to(wall.get_top(), DOWN, buff=0)

    # 3. Doors
    door = Rectangle(width=1, height=1.5, fill_opacity=1, color="#8B4513") # Wood color
    door.align_to(wall, DOWN).shift(LEFT * 1)

    # 4. Windows
    window = Square(side_length=1, fill_opacity=1, color=BLUE_B)
    window.set_stroke(WHITE, 2)
    window.shift(RIGHT * 1.2 + DOWN * 0.4)

    cross_h = Line(window.get_left(), window.get_right())
    cross_v = Line(window.get_top(), window.get_bottom())
    window_panes = VGroup(window, cross_h, cross_v)

    # 5. Sign
    sign_board = Rectangle(width=3, height=0.7, fill_opacity=1, color=B3B1B.DARK_GRAY)
    sign_board.next_to(wall, UP, buff=0.1)
    sign_text = Text("STORE", font_size=24, color=B3B1B.WHITE).move_to(sign_board)
    shop_sign = VGroup(sign_board, sign_text)

    store = VGroup(wall, awning_strips, door, window_panes, shop_sign).scale(scale_factor)
    return store

def create_sell_mobject(store_mobject, image_path="gomugomu.svg"):
    try:
        gomu_image = SVGMobject(image_path)
    except FileNotFoundError:
        gomu_image = VGroup(
            Square(side_length=1, color=B3B1B.RED, fill_opacity=0.5),
            Text("File ảnh\nlỗi!", font_size=16, color=B3B1B.WHITE).scale(0.5)
        )
        print(f"Error: Image file not found at {image_path}. Please check again.")

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

    bubble_frame.next_to(store_mobject.get_top(), UR, buff=0.05)
    gomu_image.move_to(speech_bubble_body.get_center())

    return bubble_frame, gomu_image

##############################################
### Actions"""
##############################################
def store_appear(scene, x=None, y=None, wait_time=1):
    if x is None and y is None:
        pos = ORIGIN
    else:
        pos = np.array([x, y, 0])

    store = create_store_mobject(scale_factor=.3)
    store.move_to(pos)

    scene.play(FadeIn(store, shift=DOWN*0.5))
    scene.wait(wait_time)

    return store

def sell_gomu_gomu_png(scene, store_mobject, image_path="gomugomu.svg", wait_times=[1,2]):
    bubble_frame, gomu_image = create_sell_mobject(store_mobject, image_path)

    scene.play(
        FadeIn(bubble_frame, scale=0.1, target_position=store_mobject),
        run_time=wait_times[0]
    )
    scene.add(gomu_image)

    scene.wait(wait_times[1])
    return bubble_frame, gomu_image

############################################################################################
## Scene 2
############################################################################################

##############################################
### Mobjects
##############################################
def get_layered_nodes(nx_graph, start_node):
    """
    Returns a list of lists.
    Each sublist contains nodes at the same distance from start_node.
    """
    layers = []
    visited = {start_node}
    current_layer = [start_node]

    while current_layer:
        layers.append(current_layer)
        next_layer = []
        for node in current_layer:
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

    # Mobjects
    graph_mobject = Graph(
        list(so_graph.nodes),
        list(so_graph.edges),
        layout="spring", # Spring layout helps the graph look natural
        layout_scale=4,  # Scale up the graph into a wider space
        labels=False,
        vertex_config={
            "radius": 0.08,
            "color": B3B1B.DARK_GRAY, # Most nodes are gray
            "fill_opacity": 0.6,
            "stroke_width": 0
        },
        edge_config={
            "stroke_width": 0.5,
            "stroke_opacity": 0.3,
            "color": B3B1B.LIGHT_GRAY
        }
    )

    store_node = graph_mobject.vertices[store_node_index]
    store_node.set_color(B3B1B.BLUE).set_fill(opacity=1).set_stroke(width=2, color=B3B1B.WHITE).scale(1.1)

    other_vertices = VGroup(*[graph_mobject.vertices[i] for i in graph_mobject.vertices if i != store_node_index])
    edges = VGroup(*graph_mobject.edges.values())

    top_5_vertices = VGroup(*[graph_mobject.vertices[i] for i in top_5_kols])

    layers_store = get_layered_nodes(so_graph, store_node_index)
    the_big_kol = top_5_kols[0]
    layers_kol = get_layered_nodes(so_graph, the_big_kol)

    return graph_mobject, store_node, other_vertices, top_5_vertices, edges, layers_store, layers_kol

##############################################
### Actions"""
##############################################
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

# Propagation
def promote_by_store(scene, graph_mobject, layers_store):
    for layer in layers_store[:2]:
        nodes = [graph_mobject.vertices[n] for n in layer]
        scene.play(
            *[n.animate.set_fill(B3B1B.BLUE, opacity=0.8) for n in nodes],
            run_time=1.8
        )
        
def promote_via_kol(scene, graph_mobject, layers_kol):
    for layer in layers_kol:
        nodes = [graph_mobject.vertices[n] for n in layer]
        # Exponentially faster
        scene.play(
            *[n.animate.set_fill(B3B1B.RED, opacity=1).scale(1.1) for n in nodes],
            run_time=max(0.05, 0.5 * (0.7**layers_kol.index(layer)))
        )

# Reset
def reset_graph_colors(scene, graph_mobject):
    all_vertices = graph_mobject.vertices
    animations = []

    for idx, v in all_vertices.items():
        animations.append(v.animate.set_fill(B3B1B.DARK_GRAY, opacity=0.6).scale(1))

    for edge in graph_mobject.edges.values():
        animations.append(edge.animate.set_stroke(color=B3B1B.LIGHT_GRAY, width=0.5, opacity=0.3))

    scene.play(*animations, run_time=0.5)

def impress_node(scene, node, type_='store'):
    if type_ == 'store':
        animation = Indicate(node, color=B3B1B.BLUE, scale_factor=1.2)
    if type_ == 'kol':
        animation = Indicate(node, color=B3B1B.GOLD, scale_factor=1.2)

    scene.play(animation, run_time=2)

# Delete
def shrink_to_store(scene, graph_mobject, store_node):
    # Get the current on-screen coordinates of the store node
    target_point = store_node.get_center()

    scene.play(
        # The entire graph shrinks to the position of the store node
        graph_mobject.animate.scale(0.001).move_to(target_point),
        run_time=1.5,
        rate_func=rate_functions.ease_in_back # Slight bounce effect creates a sucking-in feel
    )
    # Remove completely from render memory
    scene.remove(graph_mobject)

def play_context_sequence(scene, wait_times=[1.5,3]):
    # Intro scene
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

    # Graph scene
    graph_mobject, store_node, other_vertices, top_5_vertices, edges, layers_store, layers_kol = create_so_graph()
    graph_mobject.move_to(RIGHT*2.5)
    
    chef_talk(chef)
    speech_doc = "Vậy! Sao chúng ta không nhìn nhận thế giới này như một đồ thị? Dù là thông qua mạng truyền thông, hay mạng xã hội đi chăng nữa. Chúng ta cũng chỉ là một node của đồ thị."
    with scene.voiceover(text=speech_doc) as tracker:
        store_node = store_node_appear(scene, store_node)
        scene.wait(tracker.duration)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Chúng ta liên kết với các node khác bởi các quan hệ. Và nhu cầu của chúng ta không gì khác ngoài lan truyền tin tức kẹo Gomu Gomu đi càng xa càng tốt trong đồ thị."
    with scene.voiceover(text=speech_doc) as tracker:
        other_vertices, edges = rest_graph_appear(scene, other_vertices, edges)
        for _ in range(2):
            impress_node(scene, store_node, type_='store')
            promote_by_store(scene, graph_mobject, layers_store)
            scene.wait(tracker.duration/2)
            reset_graph_colors(scene, graph_mobject)
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Nhưng vì bạn là một cửa hàng nhỏ, và chúng tôi giả định bạn cũng chỉ là một người bình thường. Và như vậy bạn không có ảnh hưởng lớn trong mạng đồ thị này. Thế nên có vẻ như thông điệp bạn lan truyền vẫn như cũ, khó có thể mà lan xa như kỳ vọng."
    with scene.voiceover(text=speech_doc) as tracker:
        for _ in range(4):
            impress_node(scene, store_node, type_='store')
            promote_by_store(scene, graph_mobject, layers_store)
            scene.wait(tracker.duration/4)
            reset_graph_colors(scene, graph_mobject)
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
            promote_via_kol(scene, graph_mobject, layers_kol)
            scene.wait(tracker.duration/3)
            reset_graph_colors(scene, graph_mobject)

    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Nhưng khoan đã. Bạn có chắc đây là việc làm đúng đắn chứ?"
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    shrink_to_store(scene, graph_mobject, store_node)

    chef_talk(chef)
    speech_doc = "Hãy xem lại túi tiền của mình nào!"
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    # clean
    scene.play(
        FadeOut(store), 
        FadeOut(graph_elements),
        FadeOut(speech_bubble),
        run_time=1.5
    )

    return chef
    


############################################################################################
## Scene 3: The b2biers Solution (Brand Collaboration)
############################################################################################

##############################################
### Mobjects
##############################################
def create_recolored_store(scale_factor=.25, wall_color=None, awning_color=None, sign_text=None):
    # create store
    store = create_store_mobject(scale_factor=scale_factor)
    
    # change wall color (idx 0)
    if wall_color:
        store[0].set_fill(color=wall_color)
        
    # change awning color (idx 1)
    if awning_color:
        # awning has 10 strips (red - white alternating)
        # we will change the color of each strip
        for i, strip in enumerate(store[1]):
            if i % 2 == 0: 
                strip.set_fill(color=awning_color)
                
    # change shop sign (idx 4)
    if sign_text:
        # store[4][0] is the board, store[4][1] is the text
        old_text = store[4][1]
        new_text_obj = Text(sign_text, font_size=24 * (scale_factor/0.5), color=WHITE)
        new_text_obj.move_to(old_text.get_center())
        store[4].remove(old_text)
        store[4].add(new_text_obj)
        
    return store

def create_kols_mobject():
    kols = VGroup(*[
        VGroup(Circle(radius=0.3, color=GOLD, fill_opacity=1), 
               Star(color=WHITE, fill_opacity=1).scale(0.1)) 
        for _ in range(3)
    ]).arrange(RIGHT, buff=1).move_to(UP * 2 + RIGHT * 2)
    
    return kols

def create_money_bag():
    # Create money bag
    money_bag = VGroup(
        Circle(radius=0.5, color=B3B1B.GREEN, fill_opacity=0.8),
        Text("$", color=WHITE).scale(1.2)
    )

    return money_bag

def create_b2b_graph():
    # Create b2b graph
    num_nodes = 150
    seed = 88
    random.seed(seed)
    b2b_graph = nx.barabasi_albert_graph(num_nodes, 2, seed=seed)
    
    # Choose 3 node with high centrality (representing small stores)
    centrality = nx.degree_centrality(b2b_graph)
    sorted_nodes = sorted(centrality, key=centrality.get)
    
    brand_1 = sorted_nodes[15] # Gomu 
    brand_2 = sorted_nodes[30] # Bakery (Tiệm bánh)
    brand_3 = sorted_nodes[45] # Coffee Shop (Quán cà phê)
    brand_nodes_indices = [brand_1, brand_2, brand_3]

    graph_mobject = Graph(
        list(b2b_graph.nodes),
        list(b2b_graph.edges),
        layout="spring",
        layout_scale=4,
        labels=False,
        vertex_config={
            "radius": 0.08, 
            "color": B3B1B.DARK_GRAY, 
            "fill_opacity": 0.6, 
            "stroke_width": 0
        },
        edge_config={
            "stroke_width": 0.5, 
            "stroke_opacity": 0.3, 
            "color": B3B1B.LIGHT_GRAY
        }
    )

    # Highlight brand nodes
    node_colors = [B3B1B.BLUE, B3B1B.GREEN, B3B1B.ORANGE]
    brand_vertices = VGroup()
    for i, idx in enumerate(brand_nodes_indices):
        v = graph_mobject.vertices[idx]
        v.set_color(node_colors[i]).set_fill(opacity=1).set_stroke(width=2, color=B3B1B.WHITE).scale(1.5)
        brand_vertices.add(v)

    # Calc propagate layers if start from brand nodes at the same time
    layers = []
    visited = set(brand_nodes_indices)
    current_layer = list(brand_nodes_indices)

    while current_layer:
        layers.append(current_layer)
        next_layer = []
        for node in current_layer:
            for neighbor in b2b_graph.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_layer.append(neighbor)
        current_layer = next_layer

    return graph_mobject, brand_vertices, layers

##############################################
### Actions"""
##############################################
def play_b2b_sequence(scene, chef):
    
    # Stage 1: Khẳng định hàng rào chi phí
    money_bag = create_money_bag()
    kols = create_kols_mobject()
    money_bag.next_to(kols, DOWN, buff=.5)

    chef_talk(chef)
    speech_doc = "Như bạn thấy, việc liên tục thuê các nhà sáng tạo nội dung K-O-L đòi hỏi một ngân sách quảng cáo khổng lồ. Đây là rào cản rất lớn đối với các thương hiệu vừa và nhỏ như Gomu Gomu."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(FadeIn(kols, shift=UP), run_time=1)
        scene.play(FadeIn(money_bag, scale=0.5), run_time=1)
        # Highlight money bag
        scene.play(Indicate(money_bag, color=RED), run_time=1)
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # Stage 2: Giới thiệu khái niệm b2b
    chef_talk(chef)
    speech_doc = "Và đó cũng chính là lúc Konstantinos Theocharidis cùng cộng sự đề xuất ra hệ thống b2biers. Chữ b-2-b ở đây mang ý nghĩa Brand-to-Brand, tức là sự hợp tác trực tiếp giữa các thương hiệu với nhau."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
        scene.play(FadeOut(kols, shift=UP), run_time=1)
        scene.play(FadeOut(money_bag, scale=0.5), run_time=1)
    chef_silent(chef)

    # Render b2b graph
    graph_mobject, brand_vertices, combined_layers = create_b2b_graph()
    graph_mobject.move_to(RIGHT*2.5)

    # Stage 3: Hợp tác chéo
    chef_talk(chef)
    store_gomu = create_recolored_store(scale_factor=0.2, sign_text="GOMU")
    store_bakery = create_recolored_store(scale_factor=0.2, wall_color="#FFB6C1", awning_color=PURPLE, sign_text="BAKERY")
    store_cafe = create_recolored_store(scale_factor=0.2, wall_color="#D2B48C", awning_color=B3B1B.GREEN, sign_text="CAFE")
    
    stores = VGroup(store_gomu, store_bakery, store_cafe).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=1.5).shift(UP * 0.5)
    speech_doc = "Thay vì trả tiền cho K-O-L, thì tại sao cửa hàng kẹo Gomu của chúng ta lại không bắt tay hợp tác chéo với một tiệm bánh ngọt ở đối diện và một quán cà phê ở cuối góc phố."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(FadeIn(graph_mobject), run_time=1.5)
        for i in range(3):
            scene.play(
                FadeIn(stores[i], shift=RIGHT * 0.3),
                Indicate(brand_vertices[i], scale_factor=1.5),
                run_time=1.2
            )
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # Stage 4: Sức mạnh lan truyền gộp
    chef_talk(chef)
    speech_doc = "Bằng cách cùng nhau xuất hiện trong một bài đăng, tệp khách hàng có sẵn của cả ba sẽ được gộp lại. Nó tạo ra một bệ phóng lan truyền rộng lớn không thua kém gì K-O-L, mà lại hoàn toàn tối ưu về mặt chi phí."
    with scene.voiceover(text=speech_doc) as tracker:
        # Remove store for enough space
        scene.play(FadeOut(stores), run_time=0.5)

        # Create the triangle links for the cooperation
        b1, b2, b3 = brand_vertices
        link1 = Line(b1.get_center(), b2.get_center(), color=B3B1B.YELLOW, stroke_width=3)
        link2 = Line(b2.get_center(), b3.get_center(), color=B3B1B.YELLOW, stroke_width=3)
        link3 = Line(b3.get_center(), b1.get_center(), color=B3B1B.YELLOW, stroke_width=3)
        
        scene.play(Create(VGroup(link1, link2, link3)), run_time=1)
        
        # Simulate the wave propagation from 3 nodes
        for layer in combined_layers[1:4]: # Propagate from layer 1 to 3 around the triangle
            nodes = [graph_mobject.vertices[n] for n in layer]
            scene.play(
                *[n.animate.set_fill(B3B1B.YELLOW, opacity=0.9).set_stroke(B3B1B.GOLD, 0.5) for n in nodes],
                run_time=0.7
            )
        scene.wait(max(0, tracker.duration - 3.1))
    chef_silent(chef)

    # Stage 5: Dẫn dắt sang Scene 4 (Hệ thống kiến trúc)
    chef_talk(chef)
    speech_doc = "Nhưng câu hỏi đặt ra là: Làm sao để hệ thống có thể tự động chọn ra những người bạn đồng hành hoàn hảo nhất từ hàng ngàn cửa hàng? Đó chính là nhiệm vụ của trái tim hệ thống: Post Decision Engine."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)
    
    # Clean to next scene
    scene.play(FadeOut(graph_mobject), FadeOut(VGroup(link1, link2, link3)))

    return chef

############################################################################################
## Scene 4: The b2biers Solution (Brand Collaboration)
############################################################################################

##############################################
### Mobjects
##############################################
def create_scientific_box(label, color, width=3.5):
    rect = Rectangle(width=width, height=1.2, fill_color=color, fill_opacity=0.2, stroke_color=color)
    title = Text(label, font_size=20, color=color, weight=BOLD)
    return VGroup(rect, title)

def create_feedback_loop():
    # Vòng tròn đại diện cho cơ chế Semi-Bandit Feedback
    arc = CurvedArrow(start_point=RIGHT*2, end_point=LEFT*2, angle=-TAU/3, color=B3B1B.GOLD)
    label = Text("Semi-Bandit Feedback", font_size=18, color=B3B1B.GOLD)
    return VGroup(arc, label)

##############################################
### Actions"""
##############################################

def play_sys_architecture(scene, chef):
    # Define architecture layers
    units_layer = VGroup(
        create_scientific_box("Data Units", B3B1B.PURPLE),
        Text("Similarity Join | Network Stats", font_size=14, color=B3B1B.LIGHT_GRAY)
    ).arrange(DOWN, buff=0.1).move_to(DOWN * 2)

    ops_layer = VGroup(
        create_scientific_box("Operations", B3B1B.BLUE),
        Text("Influence Opt | Subscription Opt", font_size=14, color=B3B1B.LIGHT_GRAY)
    ).arrange(DOWN, buff=0.1).move_to(ORIGIN)

    pde_layer = VGroup(
        create_scientific_box("Post Decision Engine", B3B1B.RED),
        Text("Exploration vs Exploitation", font_size=14, color=B3B1B.LIGHT_GRAY)
    ).arrange(DOWN, buff=0.1).move_to(UP * 2)

    # Stage 1: Problem
    chef_talk(chef)
    speech_doc = "Dưới góc nhìn của nhà khoa học dữ liệu, b2biers không chỉ là một ứng dụng, mà là một hệ thống giải quyết bài toán tối ưu hóa tổ hợp CAIM đầy thách thức."
    with scene.voiceover(text=speech_doc) as tracker:
        formula = MathTex(r"\arg\max_{S \subseteq \mathcal{F}, |S|=k} \sigma(S)", color=B3B1B.YELLOW).shift(RIGHT * 3)
        scene.play(Write(formula))
        scene.wait(max(0, tracker.duration - 2))
    chef_silent(chef)

    # Stage 2: Units
    chef_talk(chef)
    speech_doc = "Mà tại tầng thấp nhất, chính là các Units, chúng đóng vai trò là các Data Operators. Chúng thực hiện các phép tính k-N-N Join và tính toán cấu trúc đồ thị để tạo ra Feature Space."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(FadeIn(units_layer, shift=UP))
        scene.wait(max(0, tracker.duration - 1.5))
    chef_silent(chef)

    # Stage 3: Operations
    chef_talk(chef)
    speech_doc = "Tiếp đó là tầng Operations sử dụng các mô hình lan truyền như Independent Cascade để định nghĩa hàm mục tiêu. Đây là nơi các thuật toán Greedy hoặc Heuristic bắt đầu làm việc."
    with scene.voiceover(text=speech_doc) as tracker:
        arrow1 = Arrow(units_layer.get_top(), ops_layer.get_bottom(), color=WHITE, buff=0.1)
        scene.play(FadeIn(ops_layer, shift=UP), GrowArrow(arrow1))
        scene.wait(max(0, tracker.duration - 2))
    chef_silent(chef)

    # Stage 4: PDE
    chef_talk(chef)
    speech_doc = "Cuối cùng, P-D-E đóng vai trò là động cơ, hay trái tim của hệ thống. Nó giải quyết bài toán thiếu hụt dữ liệu thực tế bằng cơ chế Semi-Bandit. Nó liên tục cân bằng giữa việc khai thác những kết quả tốt đã biết và khám phá các tổ hợp thương hiệu mới."
    with scene.voiceover(text=speech_doc) as tracker:
        arrow2 = Arrow(ops_layer.get_top(), pde_layer.get_bottom(), color=WHITE, buff=0.1)
        scene.play(FadeIn(pde_layer, shift=UP), GrowArrow(arrow2))
        
        # Tạo vòng lặp hồi tiếp (Feedback)
        feedback = CurvedArrow(pde_layer.get_right(), units_layer.get_right(), angle=-TAU/4, color=B3B1B.GOLD)
        fb_label = Text("Semi-Bandit Feedback", font_size=16, color=B3B1B.GOLD).next_to(feedback, RIGHT)
        
        scene.play(Create(feedback), Write(fb_label))
        scene.play(Indicate(pde_layer, color=B3B1B.RED), run_time=1.5)
        scene.wait(max(0, tracker.duration - 3.5))
    chef_silent(chef)

    # Stage 5: Conclusion
    chef_talk(chef)
    speech_doc = "Sự phối hợp chặt chẽ giữa ba tầng này giúp b2biers vượt qua sự bùng nổ tổ hợp và đạt được hiệu suất lan truyền tối ưu trong mạng xã hội."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    # Clean
    scene.play(FadeOut(VGroup(units_layer, ops_layer, pde_layer, arrow1, arrow2, feedback, fb_label, formula)))

    return chef

############################################################################################
## Scene 5: Data Processing Units (U1 to U5)
############################################################################################

##############################################
### Mobjects
##############################################
def create_venn_diagram(radius=1.2, shift_amount=0.8, color_left=B3B1B.BLUE, color_right=B3B1B.GREEN, label_left="Brand A", label_right="Brand B"):
    circle_left = Circle(radius=radius, color=color_left, fill_opacity=0.3).shift(LEFT * shift_amount)
    circle_right = Circle(radius=radius, color=color_right, fill_opacity=0.3).shift(RIGHT * shift_amount)
    intersection = Intersection(circle_left, circle_right, color=B3B1B.YELLOW, fill_opacity=0.8)
    text_left = Text(label_left, font_size=20, color=color_left).next_to(circle_left, UP)
    text_right = Text(label_right, font_size=20, color=color_right).next_to(circle_right, UP)
    return VGroup(circle_left, circle_right), intersection, VGroup(text_left, text_right)

def create_concept_mobject():
    doc = Rectangle(height=1.5, width=1.2, color=B3B1B.LIGHT_GRAY, fill_opacity=0.2)
    kw1 = Text("#keyword1", font_size=16, color=B3B1B.YELLOW).move_to(doc.get_center() + UP*0.3)
    kw2 = Text("#concept", font_size=16, color=B3B1B.BLUE).move_to(doc.get_center())
    kw3 = Text("#tag3", font_size=16, color=B3B1B.GREEN).move_to(doc.get_center() + DOWN*0.3)
    return VGroup(doc, kw1, kw2, kw3)

def create_unit_title(text):
    return Text(text, font_size=24, color=B3B1B.WHITE, weight=BOLD)

##############################################
### Actions
##############################################
def play_units_sequence(scene, chef):
    # --- Stage 1: TỔNG QUAN 5 UNITS ---
    chef_talk(chef)
    speech_doc = "Để hệ thống b2biers có thể hoạt động, Konstantinos đề xuất 5 Data Units độc lập để xử lý dữ liệu mạng xã hội. Nên chúng ta hãy cùng đi sâu vào từng Unit một."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)

    # Stage 2: U1 - FEATURE SIMILARITY ---
    title_u1 = create_unit_title("U1. Feature Similarity").to_edge(UP)
    circles, inter, labels = create_venn_diagram(label_left="Thương hiệu A", label_right="Thương hiệu B")
    vg_u1 = VGroup(circles, labels).move_to(ORIGIN)

    chef_talk(chef)
    speech_doc = "Unit đầu tiên là Feature Similarity. Nó đo lường độ tương đồng giữa hai thương hiệu bất kỳ dựa trên phần giao thoa trong tệp khách hàng của họ."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(title_u1))
        scene.play(FadeIn(vg_u1))
        scene.play(FadeIn(inter), run_time=1)
        scene.play(Indicate(inter, color=B3B1B.YELLOW), run_time=1.5)
        scene.wait(max(0, tracker.duration - 3.5))
    chef_silent(chef)
    
    scene.play(FadeOut(vg_u1), FadeOut(inter), FadeOut(title_u1))

    # Stage 3: U2 & U3 - CONTENT JOINS ---
    title_u23 = create_unit_title("U2 & U3. Content Joins").to_edge(UP)
    
    user_node = Circle(radius=0.4, color=B3B1B.RED, fill_opacity=1).shift(LEFT*3)
    user_label = Text("User", font_size=20).next_to(user_node, DOWN)
    
    post1 = Rectangle(height=0.8, width=0.8, color=B3B1B.BLUE, fill_opacity=0.5).shift(RIGHT*2 + UP*1.5)
    post2 = Rectangle(height=0.8, width=0.8, color=B3B1B.GREEN, fill_opacity=0.5).shift(RIGHT*2 + DOWN*1.5)
    
    arrow1 = Arrow(user_node.get_right(), post1.get_left(), color=B3B1B.BLUE)
    arrow2 = Arrow(user_node.get_right(), post2.get_left(), color=B3B1B.GREEN)
    
    lbl1 = Text("Identical Content (U2)", font_size=18, color=B3B1B.BLUE).next_to(post1, RIGHT)
    lbl2 = Text("Exploration Content (U3)", font_size=18, color=B3B1B.GREEN).next_to(post2, RIGHT)

    chef_talk(chef)
    speech_doc = "Tiếp theo là U 2 và U 3: Content Joins. U 2 tìm kiếm các bài đăng có nội dung trùng khớp với sở thích của người dùng. Trong khi đó, U 3 làm nhiệm vụ khám phá, tìm các bài đăng khác biệt để mở rộng không gian tương tác."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(title_u23))
        scene.play(FadeIn(user_node), FadeIn(user_label))
        scene.play(GrowArrow(arrow1), FadeIn(post1), Write(lbl1))
        scene.play(GrowArrow(arrow2), FadeIn(post2), Write(lbl2))
        scene.wait(max(0, tracker.duration - 4))
    chef_silent(chef)

    scene.play(FadeOut(VGroup(title_u23, user_node, user_label, post1, post2, arrow1, arrow2, lbl1, lbl2)))

    # Stage 4: U4 - POST CONCEPT ---
    title_u4 = create_unit_title("U4. Post Concept").to_edge(UP)
    concept_doc = create_concept_mobject().scale(2).move_to(ORIGIN)

    chef_talk(chef)
    speech_doc = "Unit thứ tư là Post Concept. Thuật toán sẽ phân tích dữ liệu và trích xuất ra các từ khóa cốt lõi nhất, giúp máy tính định lượng được nội dung của một bài đăng cụ thể."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(title_u4))
        scene.play(FadeIn(concept_doc[0])) # Hiện hình chữ nhật (bài đăng)
        scene.play(Write(concept_doc[1:]), run_time=1.5) # Các từ khóa bay ra
        scene.play(Indicate(concept_doc[1:]))
        scene.wait(max(0, tracker.duration - 3.5))
    chef_silent(chef)

    scene.play(FadeOut(title_u4), FadeOut(concept_doc))

    # Stage 5: U5 - POST COHERENCE ---
    title_u5 = create_unit_title("U5. Post Coherence").to_edge(UP)
    
    docA = Rectangle(height=1.2, width=0.8, color=B3B1B.YELLOW, fill_opacity=0.5).shift(LEFT*2.5)
    docB = Rectangle(height=1.2, width=0.8, color=B3B1B.PURPLE, fill_opacity=0.5).shift(RIGHT*2.5)
    
    link = DoubleArrow(docA.get_right(), docB.get_left(), color=B3B1B.WHITE)
    check_mark = Text("✔ Tính Nhất Quán (Coherent)", font_size=24, color=B3B1B.GREEN).next_to(link, UP)

    chef_talk(chef)
    speech_doc = "Cuối cùng là U 5: Post Coherence. Khi hệ thống quyết định gộp nhiều thương hiệu vào chung một quảng cáo, U 5 sẽ kiểm tra chéo các từ khóa để đảm bảo chúng có tính nhất quán và không mâu thuẫn với nhau."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(title_u5))
        scene.play(FadeIn(docA), FadeIn(docB))
        scene.play(GrowArrow(link))
        scene.play(Write(check_mark))
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # Stage 6: KẾT LUẬN ---
    chef_talk(chef)
    speech_doc = "Cả 5 Units này tạo thành một tầng xử lý dữ liệu mạnh mẽ, cung cấp thông tin đầu vào chuẩn xác để các Operations giải quyết bài toán."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Circumscribe(check_mark, color=B3B1B.GREEN))
        scene.wait(max(0, tracker.duration - 1))
    chef_silent(chef)

    scene.play(FadeOut(VGroup(title_u5, docA, docB, link, check_mark)))

    return chef


############################################################################################
## Scene 6: The Operations Layer.
############################################################################################

##############################################
### Mobjects
##############################################
def create_op_icon(label, subtext=""):
    box = RoundedRectangle(corner_radius=0.1, width=4, height=1.2, fill_color=B3B1B.BLUE, fill_opacity=0.8, stroke_color=WHITE)
    main_text = Text(label, font_size=20, color=WHITE, weight=BOLD)
    if subtext:
        st = Text(subtext, font_size=14, color=B3B1B.LIGHT_GRAY).next_to(main_text, DOWN, buff=0.1)
        return VGroup(box, main_text, st)
    return VGroup(box, main_text)

def create_strategy_visual(type="influence"):
    if type == "influence":
        center = Dot(color=B3B1B.YELLOW)
        lines = VGroup(*[Line(ORIGIN, [np.cos(a), np.sin(a), 0], color=B3B1B.YELLOW) for a in np.linspace(0, TAU, 8)])
        return VGroup(center, lines).scale(0.5)
    elif type == "diversity":
        return VGroup(Triangle(), Square(), Circle()).scale(0.3).arrange(RIGHT, buff=0.2).set_color(B3B1B.GOLD)
    elif type == "sub":
        person = Circle(radius=0.2, color=WHITE)
        plus = Text("+", color=B3B1B.GREEN).scale(0.5).next_to(person, UR, buff=-0.1)
        return VGroup(person, plus).scale(0.8)

##############################################
### Actions
##############################################
def play_operations_sequence(scene, chef):
    # --- NHỊP 1: GIỚI THIỆU TẦNG OPERATIONS ---
    chef_talk(chef)
    speech_doc = "Bây giờ, chúng ta sẽ bước vào tầng Operations. Đây là nơi b2biers cung cấp 8 dịch vụ chiến lược khác nhau, chia làm 3 nhóm chính."
    with scene.voiceover(text=speech_doc) as tracker:
        title = Text("Tầng Operations: 8 Chiến lược cốt lõi", font_size=30, color=B3B1B.BLUE).to_edge(UP)
        scene.play(Write(title))
        scene.wait(max(0, tracker.duration - 1.5))
    chef_silent(chef)

    # --- NHỊP 2: NHÓM 1 - TỐI ƯU ẢNH HƯỞNG (O1, O2, O4) ---
    group1_title = Text("1. Nhóm Tối ưu Ảnh hưởng", font_size=24, color=B3B1B.YELLOW).shift(UP*1.5 + LEFT*3)
    o1 = create_op_icon("O1. Influential User Post Join", "Kết nối KOL").scale(0.7)
    o2 = create_op_icon("O2. Influential Paths Extension", "Mở rộng đường dẫn").scale(0.7)
    o4 = create_op_icon("O4. Influential Post Diversity", "Đa dạng hóa nội dung").scale(0.7)
    g1_ops = VGroup(o1, o2, o4).arrange(DOWN, buff=0.3).next_to(group1_title, DOWN, buff=0.5)

    chef_talk(chef)
    speech_doc = "Nhóm đầu tiên tập trung vào Ảnh hưởng. O 1 kết nối thương hiệu với người dùng quyền lực. O 2 mở rộng tầm phủ qua các đường dẫn tiềm năng. Và O 4 đảm bảo nội dung lan truyền luôn đa dạng, tránh gây nhàm chán."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(group1_title))
        visual_inf = create_strategy_visual("influence").next_to(group1_title, RIGHT, buff=0.5)
        scene.play(FadeIn(g1_ops, shift=RIGHT), FadeIn(visual_inf))
        scene.play(Indicate(o4))
        scene.wait(max(0, tracker.duration - 4))
    chef_silent(chef)

    # --- NHỊP 3: NHÓM 2 - TƯƠNG TÁC & ĐĂNG KÝ (O3, O5) ---
    group2_title = Text("2. Nhóm Tương tác & Đăng ký", font_size=24, color=B3B1B.GREEN).shift(UP*1.5 + RIGHT*3)
    o3 = create_op_icon("O3. Subscribers Engagement", "Tăng tương tác").scale(0.7)
    o5 = create_op_icon("O5. Adaptive Subscription Max", "Tối ưu hóa thích nghi").scale(0.7)
    g2_ops = VGroup(o3, o5).arrange(DOWN, buff=0.5).next_to(group2_title, DOWN, buff=0.5)

    chef_talk(chef)
    speech_doc = "Nhóm thứ hai là Tương tác và Đăng ký. O 3 tối ưu hóa sự gắn kết của những người đã theo dõi. Trong khi O 5 là một cơ chế thích nghi, giúp tối đa hóa lượng người đăng ký mới theo thời gian thực."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(group2_title))
        visual_sub = create_strategy_visual("sub").next_to(group2_title, RIGHT, buff=0.5)
        scene.play(FadeIn(g2_ops, shift=LEFT), FadeIn(visual_sub))
        scene.play(Indicate(o5))
        scene.wait(max(0, tracker.duration - 4))
    chef_silent(chef)

    # Dọn dẹp để hiện GSM
    scene.play(FadeOut(g1_ops), FadeOut(g2_ops), FadeOut(group1_title), FadeOut(group2_title), FadeOut(visual_inf), FadeOut(visual_sub))

    # --- NHỊP 4: NHÓM 3 - GLOBAL SUBSCRIPTION MAXIMIZATION (O6.1, O6.2, O6.3) ---
    gsm_title = Text("3. Nhóm GSM (Global Subscription Maximization)", font_size=24, color=B3B1B.RED).shift(UP*1.5)
    o6_1 = create_op_icon("O6.1. GSM: (k, m)-query", "Tối ưu k hiệu năng trên m ngân sách").scale(0.7)
    o6_2 = create_op_icon("O6.2. GSM: k-query", "Tối ưu k hiệu năng").scale(0.7)
    o6_3 = create_op_icon("O6.3. GSM: m-query", "Tối ưu trên m ngân sách").scale(0.7)
    gsm_ops = VGroup(o6_1, o6_2, o6_3).arrange(DOWN, buff=0.3).next_to(gsm_title, DOWN, buff=0.5)

    chef_talk(chef)
    speech_doc = "Cuối cùng là nhóm G S M, hay Tối ưu hóa đăng ký toàn cục. Đây là các truy vấn cấp cao: O 6.1 cân bằng giữa số lượng tính năng k và ngân sách m. O 6.2 và 6.3 tập trung chuyên biệt vào từng biến số đơn lẻ."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Write(gsm_title))
        scene.play(FadeIn(gsm_ops, shift=UP))
        # Hoạt ảnh minh họa k và m
        formula_gsm = MathTex("f(k, m) \\rightarrow \\max", color=B3B1B.RED).next_to(gsm_ops, RIGHT, buff=1)
        scene.play(Write(formula_gsm))
        scene.wait(max(0, tracker.duration - 5))
    chef_silent(chef)

    # --- NHỊP 5: KẾT LUẬN ---
    chef_talk(chef)
    speech_doc = "Tám nhà vận hành này cho phép b2biers đáp ứng mọi nhu cầu của nhà quảng cáo, từ một cửa hàng nhỏ cho đến một tập đoàn lớn."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(Indicate(gsm_ops))
        scene.wait(max(0, tracker.duration - 2))
    chef_silent(chef)

    scene.play(FadeOut(VGroup(gsm_ops, gsm_title, formula_gsm, title)))

    return chef

############################################################################################
## Scene 7: The PDE.
############################################################################################

##############################################
### Mobjects
##############################################
def create_pde_math_mobjects():
    # 1. Khung Bài đăng (Post Box)
    post_box = RoundedRectangle(width=4.5, height=1.5, fill_color=B3B1B.DARK_GRAY, fill_opacity=0.5, stroke_color=B3B1B.WHITE)
    post_title = Text("Bài đăng (k = 3 features)", font_size=20, color=B3B1B.WHITE).next_to(post_box, UP)
    
    # 3 Features bên trong
    feat_A = Circle(radius=0.35, fill_color=B3B1B.BLUE, fill_opacity=1).move_to(post_box.get_center() + LEFT*1.3)
    feat_B = Circle(radius=0.35, fill_color=B3B1B.GREEN, fill_opacity=1).move_to(post_box.get_center())
    feat_C = Circle(radius=0.35, fill_color=B3B1B.ORANGE, fill_opacity=1).move_to(post_box.get_center() + RIGHT*1.3)
    
    lbl_A = Text("A", font_size=20).move_to(feat_A)
    lbl_B = Text("B", font_size=20).move_to(feat_B)
    lbl_C = Text("C", font_size=20).move_to(feat_C)
    
    features = VGroup(VGroup(feat_A, lbl_A), VGroup(feat_B, lbl_B), VGroup(feat_C, lbl_C))
    post_group = VGroup(post_box, post_title, features)
    
    # 2. Biểu đồ cột thể hiện điểm Conceptual Clicks
    bar_A = Rectangle(width=0.6, height=2.0, fill_color=B3B1B.BLUE, fill_opacity=0.8).next_to(feat_A, DOWN, buff=1)
    bar_B = Rectangle(width=0.6, height=1.2, fill_color=B3B1B.GREEN, fill_opacity=0.8).next_to(feat_B, DOWN, buff=1).align_to(bar_A, DOWN)
    bar_C = Rectangle(width=0.6, height=0.3, fill_color=B3B1B.ORANGE, fill_opacity=0.8).next_to(feat_C, DOWN, buff=1).align_to(bar_A, DOWN)
    
    txt_click = Text("Conceptual Clicks (Điểm ước lượng)", font_size=20, color=B3B1B.YELLOW).next_to(bar_A, LEFT, buff=0.5).align_to(bar_A, DOWN).shift(UP*1)
    bars = VGroup(bar_A, bar_B, bar_C, txt_click)
    
    # 3. Đồ thị luồng TRIM_E
    node_b = Circle(radius=0.4, fill_color=B3B1B.GREEN, fill_opacity=1).shift(LEFT*2.5)
    node_c = Circle(radius=0.4, fill_color=B3B1B.ORANGE, fill_opacity=1).move_to(ORIGIN)
    node_a = Circle(radius=0.4, fill_color=B3B1B.BLUE, fill_opacity=1).shift(RIGHT*2.5)
    
    t_b = Text("B", font_size=20).move_to(node_b)
    t_c = Text("C", font_size=20).move_to(node_c)
    t_a = Text("A", font_size=20).move_to(node_a)
    
    arr1 = Arrow(node_b.get_right(), node_c.get_left(), buff=0.1)
    arr2 = Arrow(node_c.get_right(), node_a.get_left(), buff=0.1)
    
    trime_graph = VGroup(VGroup(node_b, t_b), arr1, VGroup(node_c, t_c), arr2, VGroup(node_a, t_a))
    
    return post_group, bars, trime_graph

##############################################
### Actions
##############################################
def play_pde_sequence(scene):
    chef = chef_appear(scene, x=-6, y=-2.5, direction=UP)
    
    post_group, bars, trime_graph = create_pde_math_mobjects()
    post_group.move_to(UP*2)
    
    # --- NHỊP 1: ĐỊNH NGHĨA PDE & TRIM_E ---
    chef_talk(chef)
    speech_doc = "Giờ chúng ta sẽ đi sâu vào bộ não P-D-E. Về mặt toán học, đây là một hệ thống Học tăng cường dựa trên thuật toán cốt lõi có tên là TRIM E. Mục tiêu của nó là tối đa hóa tổng số lượt tương tác qua nhiều vòng lặp."
    with scene.voiceover(text=speech_doc) as tracker:
        title = Text("Cơ chế thuật toán TRIM_E", font_size=30, color=B3B1B.RED).to_edge(UP)
        scene.play(Write(title))
        scene.wait(max(0, tracker.duration - 1))
    chef_silent(chef)

    # --- NHỊP 2: BƯỚC CHỌN K FEATURE ---
    chef_talk(chef)
    speech_doc = "Bước 1: Hệ thống chọn ra k thương hiệu, giả sử k bằng 3 gồm A, B và C, để hợp nhất thành một bài đăng chung."
    with scene.voiceover(text=speech_doc) as tracker:
        post_group.next_to(title, DOWN, buff=0.5)
        scene.play(FadeIn(post_group, shift=UP))
        scene.wait(max(0, tracker.duration - 1.5))
    chef_silent(chef)
    
    # --- NHỊP 3: BƯỚC TÍNH TOÁN CONCEPTUAL CLICKS ---
    chef_talk(chef)
    speech_doc = "Bước 2: Tính toán Conceptual Clicks. Khi bài đăng nhận được hàng ngàn lượt Thích từ thực tế, hệ thống không chia đều thành tích. Nó sử dụng hàm ước lượng để đánh giá xem chính xác tính năng nào đã thu hút người dùng, và cộng điểm độc lập cho riêng tính năng đó."
    with scene.voiceover(text=speech_doc) as tracker:
        # Tạo icon Thích bay vào
        likes = VGroup(*[Text("👍").scale(0.8).move_to(post_group.get_top() + UP*0.5 + RIGHT*random.uniform(-2,2)) for _ in range(4)])
        scene.play(LaggedStart(*[FadeIn(l, shift=DOWN*0.5) for l in likes], lag_ratio=0.2), run_time=1.5)
        scene.play(FadeOut(likes))
        
        # Hiện biểu đồ
        bars.next_to(post_group, DOWN, buff=0.5).shift(RIGHT*1.2)
        scene.play(FadeIn(bars[3])) # Hiện chữ Conceptual Clicks
        scene.play(GrowFromBottom(bars[0]), GrowFromBottom(bars[1]), GrowFromBottom(bars[2]), run_time=2)
        scene.wait(max(0, tracker.duration - 5.5))
    chef_silent(chef)
    
    # --- NHỊP 4: LOẠI BỎ (ELIMINATION) ---
    chef_talk(chef)
    speech_doc = "Bước 3: Loại bỏ thích nghi. Dựa vào biểu đồ, tính năng C có điểm Conceptual Clicks quá thấp so với A và B. Thuật toán TRIM E sẽ lập tức ra quyết định loại bỏ C khỏi tập hợp tiềm năng."
    with scene.voiceover(text=speech_doc) as tracker:
        cross = Cross(post_group[2][2], stroke_color=B3B1B.RED, stroke_width=6) # Gạch chéo C
        scene.play(Create(cross))
        scene.play(Indicate(bars[2], color=B3B1B.RED))
        scene.wait(max(0, tracker.duration - 2.5))
    chef_silent(chef)
    
    # --- NHỊP 5: XỬ LÝ NÚT ẨN (INTERMEDIATE NODES) - ĐIỂM ĐẶC BIỆT CỦA BÀI BÁO ---
    chef_talk(chef)
    speech_doc = "Tuy nhiên, sức mạnh thực sự của TRIM E nằm ở việc ghi nhớ đường dẫn. Dù bị loại bỏ, C không biến mất hoàn toàn mà chuyển thành một 'nút ẩn trung gian'. Điều này giúp hệ thống lưu giữ được các cấu trúc liên kết mạng ban đầu, đảm bảo luồng lan truyền không bị đứt gãy."
    with scene.voiceover(text=speech_doc) as tracker:
        # Dọn dẹp để hiện luồng đồ thị
        scene.play(FadeOut(post_group), FadeOut(bars), FadeOut(cross))
        
        trime_graph.move_to(DOWN*0.5)
        scene.play(FadeIn(trime_graph, shift=UP), run_time=1)
        
        # Biến đổi C thành nút ẩn (Dashed mờ)
        hidden_c = DashedVMobject(Circle(radius=0.4, color=B3B1B.DARK_GRAY, fill_opacity=0.2)).move_to(trime_graph[2][0])
        t_c_hidden = Text("C", font_size=20, color=B3B1B.DARK_GRAY).move_to(hidden_c)
        
        scene.play(
            FadeOut(trime_graph[2]), 
            FadeIn(VGroup(hidden_c, t_c_hidden)),
            run_time=1.5
        )
        # Sáng lên luồng truyền đi xuyên qua C
        scene.play(Indicate(trime_graph[1]), Indicate(trime_graph[3]), color=B3B1B.YELLOW, run_time=1.5)
        
        scene.wait(max(0, tracker.duration - 5.5))
    chef_silent(chef)
    
    # --- KẾT LUẬN ---
    chef_talk(chef)
    speech_doc = "Quá trình này lặp đi lặp lại liên tục, giúp PDE ngày càng thông minh hơn và chỉ giữ lại những nhóm đối tác mang lại lợi nhuận lan truyền cao nhất."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.wait(tracker.duration)
    chef_silent(chef)
    
    # Dọn dẹp
    scene.play(
        FadeOut(VGroup(trime_graph[0], trime_graph[1], trime_graph[3], trime_graph[4])),
        FadeOut(hidden_c), FadeOut(t_c_hidden), FadeOut(title)
    )

    return chef

############################################################################################
## Scene 7: The PDE.
############################################################################################

##############################################
### Mobjects
##############################################

def create_platform_card(title, color, bullets):
    # Khung thẻ
    card = RoundedRectangle(corner_radius=0.2, width=3.5, height=4, fill_color=color, fill_opacity=0.15, stroke_color=color, stroke_width=4)
    
    # Tiêu đề nền tảng
    t_title = Text(title, font_size=28, color=color, weight=BOLD).next_to(card.get_top(), DOWN, buff=0.3)
    
    # Danh sách các kỹ thuật quảng cáo
    bullet_group = VGroup()
    for item in bullets:
        bullet = Text(f"• {item}", font_size=18, color=B3B1B.WHITE)
        bullet_group.add(bullet)
    
    bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(t_title, DOWN, buff=0.5).shift(LEFT*0.2)
    
    return VGroup(card, t_title, bullet_group)

##############################################
### Actions
##############################################
def play_industry_techniques_sequence(scene, chef):
    # Khởi tạo 3 thẻ đại diện cho 3 nền tảng
    fb_bullets = ["Đa dạng hóa nội dung", "Quảng cáo trả phí (Ads)", "Hợp tác chéo", "Quản lý ngân sách"]
    yt_bullets = ["Tối ưu từ khóa (SEO)", "Đa dạng thể loại Video", "Kêu gọi hành động (CTA)"]
    ig_bullets = ["Tiếp thị Influencer", "Nội dung người dùng tạo", "Tổ chức Giveaways"]
    
    card_fb = create_platform_card("Facebook", B3B1B.BLUE, fb_bullets)
    card_yt = create_platform_card("YouTube", B3B1B.RED, yt_bullets)
    card_ig = create_platform_card("Instagram", B3B1B.PURPLE, ig_bullets)
    
    cards = VGroup(card_fb, card_yt, card_ig).arrange(RIGHT, buff=0.5).move_to(UP*0.5).scale(0.8)

    # --- NHỊP 1: ĐẶT VẤN ĐỀ ---
    chef_talk(chef)
    speech_doc = "Để làm rõ định vị của mình, bài báo đã phân tích bức tranh toàn cảnh về các kỹ thuật quảng cáo hiện tại trên mạng xã hội, dựa trên chia sẻ của chuyên gia hàng đầu Neil Patel."
    with scene.voiceover(text=speech_doc) as tracker:
        title = Text("Kỹ thuật Quảng cáo trong ngành Công nghiệp MXH", font_size=28, color=B3B1B.YELLOW).to_edge(UP)
        scene.play(Write(title))
        scene.wait(max(0, tracker.duration - 1.5))
    chef_silent(chef)

    # --- NHỊP 2: LƯỚT QUA 3 NỀN TẢNG ---
    chef_talk(chef)
    speech_doc = "Trên Facebook, nhà quảng cáo tối ưu hóa thông qua các loại nội dung đa dạng, công cụ nhắm mục tiêu và hợp tác chéo. Với YouTube, chiến lược xoay quanh tối ưu từ khóa S E O và đa dạng thể loại video. Còn Instagram là vùng đất của các Influencers và các chiến dịch tặng quà Giveaways."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(FadeIn(card_fb, shift=UP*0.5), run_time=1)
        scene.play(FadeIn(card_yt, shift=UP*0.5), run_time=1)
        scene.play(FadeIn(card_ig, shift=UP*0.5), run_time=1)
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # --- NHỊP 3: CHỐT LẠI GIÁ TRỊ CỦA B2BIERS ---
    chef_talk(chef)
    speech_doc = "Điểm mấu chốt ở đây là: b2biers không hề dẫm chân, cũng không cố gắng thay thế các kỹ thuật của ngành công nghiệp hiện tại."
    with scene.voiceover(text=speech_doc) as tracker:
        # Cảnh báo không dẫm chân
        scene.play(cards.animate.set_opacity(0.4), run_time=1.5)
        scene.wait(max(0, tracker.duration - 1.5))
    chef_silent(chef)

    chef_talk(chef)
    speech_doc = "Ngược lại, nó đứng như một lớp dịch vụ hoàn toàn mới. Các thương hiệu vẫn có thể dùng Facebook Ads hay thuê Influencer trên Instagram, nhưng giờ đây họ có thêm b2biers để tự tạo ra mạng lưới lan truyền của riêng mình một cách tự nhiên và tiết kiệm nhất."
    with scene.voiceover(text=speech_doc) as tracker:
        # Vẽ một vòng cung lớn bao bọc cả 3 nền tảng
        b2b_layer = RoundedRectangle(corner_radius=0.5, width=12, height=5, color=B3B1B.YELLOW, stroke_width=6).move_to(cards.get_center())
        b2b_label = Text("The b2biers Services", font_size=32, color=B3B1B.YELLOW, weight=BOLD).next_to(b2b_layer, UP, buff=0.2)
        
        scene.play(Create(b2b_layer), Write(b2b_label), run_time=2)
        # Làm sáng lại các thẻ bên trong để cho thấy sự hoạt động song song
        scene.play(cards.animate.set_opacity(1), run_time=1)
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # Dọn dẹp chuyển sang Scene 9
    scene.play(FadeOut(cards), FadeOut(b2b_layer), FadeOut(b2b_label), FadeOut(title), run_time=1.5)

    return chef

############################################################################################
## Scene 9: THE GSM SYSTEM
############################################################################################

##############################################
### Mobjects
##############################################

def create_platform_card(title, color, bullets):
    # Khung thẻ
    card = RoundedRectangle(corner_radius=0.2, width=3.5, height=4, fill_color=color, fill_opacity=0.15, stroke_color=color, stroke_width=4)
    
    # Tiêu đề nền tảng
    t_title = Text(title, font_size=28, color=color, weight=BOLD).next_to(card.get_top(), DOWN, buff=0.3)
    
    # Danh sách các kỹ thuật quảng cáo
    bullet_group = VGroup()
    for item in bullets:
        bullet = Text(f"• {item}", font_size=18, color=B3B1B.WHITE)
        bullet_group.add(bullet)
    
    bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(t_title, DOWN, buff=0.5).shift(LEFT*0.2)
    
    return VGroup(card, t_title, bullet_group)

##############################################
### Actions
##############################################

def play_conclusion_sequence(scene, chef):
    # 1. Chef xuất hiện và tóm tắt nhanh
    chef_talk(chef)
    speech_doc = "Tóm lại, hệ thống b2biers là một giải pháp đột phá, kết hợp giữa toán học tối ưu tổ hợp và thực tiễn kinh doanh quảng cáo, giúp các thương hiệu nhỏ tự tạo ra sức mạnh lan truyền của riêng mình."
    with scene.voiceover(text=speech_doc) as tracker:
        summary_title = Text("Tóm tắt giá trị cốt lõi", font_size=32, color=B3B1B.YELLOW).to_edge(UP)
        
        # Hiện lại 3 trụ cột ở dạng mini để nhắc bài
        p1 = Text("• Tối ưu chi phí", font_size=24).next_to(summary_title, DOWN, buff=0.5).shift(RIGHT*2)
        p2 = Text("• Lan truyền tự nhiên", font_size=24).next_to(p1, DOWN, buff=0.3).align_to(p1, LEFT)
        p3 = Text("• Công nghệ thích nghi", font_size=24).next_to(p2, DOWN, buff=0.3).align_to(p1, LEFT)
        
        scene.play(Write(summary_title))
        scene.play(FadeIn(VGroup(p1, p2, p3), shift=LEFT*0.3), run_time=2)
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # 2. Thông tin về chương trình hỗ trợ (Theo Acknowledgements trong bài báo)
    chef_talk(chef)
    speech_doc = "Dự án nghiên cứu này cũng nhận được sự hỗ trợ từ Quỹ Nghiên cứu Quốc gia Singapore, thông qua chương trình A-I Singapore."
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(FadeOut(summary_title), FadeOut(VGroup(p1, p2, p3)))
        
        support_txt = Text("Supported by:\nNational Research Foundation, Singapore\nAI Singapore Programme", 
                          font_size=20, color=B3B1B.LIGHT_GRAY, t2c={"AI Singapore": B3B1B.GOLD}).move_to(RIGHT*2)
        scene.play(Write(support_txt))
        scene.wait(max(0, tracker.duration - 2))
    chef_silent(chef)

    # 3. Lời cảm ơn - Đưa Chef ra giữa màn hình
    scene.play(FadeOut(support_txt))
    
    # Di chuyển Chef ra trung tâm và phóng lớn một chút
    scene.play(
        chef.animate.move_to(ORIGIN).scale(1.5),
        run_time=1.5
    )

    chef_talk(chef)
    speech_doc = "Cảm ơn thầy và các bạn đã dành thời gian theo dõi bài thuyết trình của nhóm một về hệ thống b2biers. Chúc mọi người một ngày học tập và làm việc thật hiệu quả!"
    with scene.voiceover(text=speech_doc) as tracker:
        thanks_text = Text("CẢM ƠN THẦY VÀ CÁC BẠN!", font_size=48, color=B3B1B.YELLOW, weight=BOLD).next_to(chef, UP, buff=1)
        names = Text("Nhóm 01: Tuấn Khải & Văn Phúc", font_size=24, color=B3B1B.LIGHT_GRAY).next_to(chef, DOWN, buff=0.8)
        
        scene.play(Write(thanks_text), run_time=1.5)
        scene.play(FadeIn(names, shift=UP*0.3))
        
        # Hiệu ứng Chef nhún nhảy hoặc nháy mắt (Indicate) để chào
        scene.play(Indicate(chef, scale_factor=1.1, color=B3B1B.YELLOW))
        scene.wait(max(0, tracker.duration - 3))
    chef_silent(chef)

    # Kết thúc video: Mờ dần
    scene.play(FadeOut(scene.mobjects))


############################################################################################
## Run (The Orchestrator)"""
############################################################################################

class FullPresentation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="vi"))

        self.camera.background_color = B3B1B.BLACK

        footer = create_footer()
        self.add(footer)

        # --- SCENE 1: INTRODUCTION ---
        self.next_section("Introduction")
        play_intro_sequence(self)

        # --- SCENE 2: CONTEXT & MOTIVATION ---
        self.next_section("Context & Motivation")
        chef = play_context_sequence(self, wait_times=[0.5,3])

        # --- SCENE 3: THE B2BIERS SOLUTION ---
        self.next_section("The b2biers Solution")
        chef = play_b2b_sequence(self, chef)

        # --- SCENE 4: THE B2BIERS SYSTEM ---
        self.next_section("The b2biers System")
        chef = play_sys_architecture(self, chef)

        # --- SCENE 5: DATA UNITS ---
        self.next_section("Data Processing Units")
        chef = play_units_sequence(self, chef)

        # --- SCENE 6: THE GSM SYSTEM ---
        self.next_section("The GSM System")
        chef = play_gsm_sequence(self, chef)

        # --- SCENE 7: PDE ---
        self.next_section("PDE")
        chef = play_pde_sequence(self, chef)

        # --- SCENE 8: THE B2BIERS PLATFORM ---
        self.next_section("The b2biers Platform")
        chef = play_platform_sequence(self, chef)

        # --- SCENE 9: CONCLUSION ---
        self.next_section("Conclusion")
        play_conclusion_sequence(self, chef)

        self.wait(1)
