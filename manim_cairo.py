import os
import random
import time
import networkx as nx
import numpy as np

import gtts
import manim_voiceover.services.gtts
# Vá lỗi gTTS cho voiceover
manim_voiceover.services.gtts.gTTS = gtts.gTTS
manim_voiceover.services.gtts.gTTSError = gtts.gTTSError

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

"## Globals & Helpers"""
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

def get_colors():
    return {"primary": B3B1B.BLUE, "secondary": B3B1B.GOLD, "text": B3B1B.LIGHT_GRAY}

def create_footer():
    return Tex(
        r"Nhóm 01 - Khoa học dữ liệu ứng dụng",
        font_size=18,
        color=B3B1B.DARK_GRAY,
        tex_template=get_vn_template()
    ).to_edge(DR)

"""## Chef Mascot (Sửa để tương thích Cairo)"""
def create_chef(body_color=B3B1B.RED, color=B3B1B.DARKER_GRAY, scale_factor=1.0):
    body = RoundedRectangle(
        corner_radius=0.4, height=2.5, width=1.4, color=body_color, 
        stroke_width=6, fill_color=body_color, fill_opacity=1
    )

    # Mũ
    hat_neck = Rectangle(width=0.5, height=0.7, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(body.get_top() + UP*0.3)
    hat_top = VGroup(*[
        Circle(radius=0.3, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + LEFT*0.3),
        Circle(radius=0.35, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + UP*0.2),
        Circle(radius=0.3, color=body_color, stroke_width=6, fill_color=body_color, fill_opacity=1).move_to(hat_neck.get_top() + RIGHT*0.3),
    ])

    eyes = VGroup(
        Ellipse(width=0.4, height=0.15, color=color, fill_color=color, fill_opacity=1),
        Ellipse(width=0.4, height=0.15, color=color, fill_color=color, fill_opacity=1)
    ).arrange(RIGHT, buff=0.15).move_to(body.get_center() + UP*0.7)

    nose = Rectangle(width=0.3, height=0.15, color=color, fill_opacity=1).move_to(body.get_center() + UP*0.2)

    mouth = Arc(
        radius=0.4, start_angle=PI/3, angle=PI/3, color=color, stroke_width=6
    ).move_to(body.get_center() + DOWN*0.4)

    # Sử dụng VGroup cho Cairo renderer
    chef = VGroup(body, hat_neck, hat_top, eyes, nose, mouth)
    chef.scale(scale_factor)
    chef.mouth = mouth # Gán trực tiếp để dễ truy cập
    return chef

def chef_talk(chef, speed=10):
    # Lưu lại trạng thái gốc của miệng
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

    chef.mouth.add_updater(update_mouth)

def chef_silent(chef):
    chef.mouth.clear_updaters()
    if hasattr(chef, "original_mouth_points"):
        chef.mouth.set_points(chef.original_mouth_points)

"""## Các hàm phụ trợ khác (Giữ nguyên logic)"""
# ... (Giữ nguyên các hàm create_store_moobj, create_so_graph, v.v. từ code cũ của bạn) ...
# Lưu ý: Trong hàm create_so_graph, đảm bảo Graph sử dụng các tham số chuẩn của Manim.

def create_intro_moobj():
    line1 = Tex(r"The b2biers System:", color=get_colors()["secondary"], tex_template=get_vn_template())
    line2 = Tex(r"A Context-based Perspective", font_size=34, tex_template=get_vn_template())
    names = Tex(r"Nguyễn Lê Tuấn Khải \& Nguyễn Văn Phúc", font_size=28, color=B3B1B.DARK_GRAY, tex_template=get_vn_template())
    return VGroup(line1, line2, names).arrange(DOWN, buff=0.8)

def play_intro_sequence(scene):
    intro = create_intro_moobj()
    speech_doc = "Chào thầy và các bạn. Hôm nay, chúng mình, nhóm một, gồm Nguyễn Lê Tuấn Khải và Nguyễn Văn Phúc xin được trình bày về hệ thống b2biers"
    with scene.voiceover(text=speech_doc) as tracker:
        scene.play(FadeIn(intro, shift=UP * 0.3, lag_ratio=0.1), run_time=2)
        scene.wait(max(0.1, tracker.duration - 2))
    scene.play(FadeOut(intro, shift=UP * 0.2))

# --- Copy lại toàn bộ logic các hàm Scene 2, Store, v.v. từ bản cũ vào đây ---
# Chỉ cần đảm bảo không dùng các class từ .opengl

"""## Orchestrator Scene"""
class FullPresentation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="vi"))
        self.camera.background_color = B3B1B.BLACK
        
        footer = create_footer()
        self.add(footer)

        # SCENE 1
        self.next_section("Introduction")
        play_intro_sequence(self)

        # SCENE 2
        self.next_section("Context & Motivation")
        # Gọi play_context_sequence(self) ở đây - đảm bảo bạn đã định nghĩa nó phía trên
        # play_context_sequence(self) 

        self.wait(1)

