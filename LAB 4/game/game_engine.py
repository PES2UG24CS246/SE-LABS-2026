import random
import pygame


class GameEngine:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # -----------------------------
        # Basic game state
        # -----------------------------
        self.arm_position = 0.0
        self.target_limit = 100.0
        self.last_key = None

        self.stamina = 100.0
        self.max_stamina = 100.0

        self.winner = None
        self.game_state = "PLAYING"

        # -----------------------------
        # TASK 2: AI surge system
        # -----------------------------
        self.ai_strength = 0.18

        self.ai_state = "NORMAL"
        self.ai_timer = 0.0

        self.ai_normal_duration = 3.0
        self.ai_surge_duration = 2.0
        self.ai_cooldown_duration = 4.0

        # -----------------------------
        # TASK 3: Exhaustion
        # -----------------------------
        self.exhausted = False

        # -----------------------------
        # TASK 4: Counter-surge
        # -----------------------------
        self.counter_window = 0.0
        self.counter_window_duration = 1.5

        self.counter_surge_active = False
        self.counter_surge_timer = 0.0
        self.counter_surge_duration = 1.5

        self.normal_push_strength = 4.2
        self.counter_push_strength = 8.4

        # Stamina recovery
        self.normal_stamina_recovery = 0.08
        self.counter_stamina_recovery = 0.30

        # -----------------------------
        # Fonts
        # -----------------------------
        self.font_big = pygame.font.SysFont(None, 44)
        self.font_med = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

    # =========================================================
    # PLAYER INPUT
    # =========================================================

    def handle_event(self, event):

        # Rematch
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type != pygame.KEYDOWN:
            return

        # Player cannot push while exhausted
        if self.stamina <= 10:
            return

        # Only Left and Right affect the game
        if event.key not in (pygame.K_LEFT, pygame.K_RIGHT):
            return

        # -----------------------------------------------------
        # TASK 4:
        # Counter-surge opportunity immediately after AI surge
        # -----------------------------------------------------

        push_strength = self.normal_push_strength

        if (
            self.ai_state == "COOLDOWN"
            and self.counter_window > 0
        ):
            self.counter_surge_active = True
            self.counter_surge_timer = self.counter_surge_duration

            self.counter_window = 0.0

            # Double push strength
            push_strength = self.counter_push_strength

        # -----------------------------------------------------
        # TASK 1:
        # Player pushes toward negative arm position
        # -----------------------------------------------------

        if event.key == pygame.K_LEFT:

            if self.last_key != pygame.K_LEFT:

                self.arm_position -= push_strength

                self.stamina = max(
                    0.0,
                    self.stamina - 2.0
                )

                self.last_key = pygame.K_LEFT

        elif event.key == pygame.K_RIGHT:

            if self.last_key != pygame.K_RIGHT:

                self.arm_position -= push_strength

                self.stamina = max(
                    0.0,
                    self.stamina - 2.0
                )

                self.last_key = pygame.K_RIGHT

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        if self.game_state != "PLAYING":
            return

        # Game runs at 60 FPS
        dt = 1.0 / 60.0

        # =====================================================
        # TASK 2: AI STATE MACHINE
        # =====================================================

        self.ai_timer += dt

        # NORMAL -> SURGE
        if self.ai_state == "NORMAL":

            if self.ai_timer >= self.ai_normal_duration:

                self.ai_state = "SURGE"
                self.ai_timer = 0.0

        # SURGE -> COOLDOWN
        elif self.ai_state == "SURGE":

            if self.ai_timer >= self.ai_surge_duration:

                self.ai_state = "COOLDOWN"
                self.ai_timer = 0.0

                # Open counter-surge opportunity
                self.counter_window = (
                    self.counter_window_duration
                )

        # COOLDOWN -> NORMAL
        elif self.ai_state == "COOLDOWN":

            if self.ai_timer >= self.ai_cooldown_duration:

                self.ai_state = "NORMAL"
                self.ai_timer = 0.0
                self.counter_window = 0.0

        # =====================================================
        # TASK 4: COUNTER WINDOW
        # =====================================================

        if self.counter_window > 0:

            self.counter_window -= dt

            if self.counter_window < 0:
                self.counter_window = 0.0

        # =====================================================
        # TASK 4: COUNTER-SURGE TIMER
        # =====================================================

        if self.counter_surge_active:

            self.counter_surge_timer -= dt

            if self.counter_surge_timer <= 0:

                self.counter_surge_timer = 0.0
                self.counter_surge_active = False

        # =====================================================
        # TASK 2: AI FORCE
        # =====================================================

        ai_variance = random.uniform(0.3, 1.0)

        if self.ai_state == "NORMAL":

            ai_force = self.ai_strength

        elif self.ai_state == "SURGE":

            # High-power AI surge
            ai_force = self.ai_strength * 1.8

        else:

            # Reduced resistance during cooldown
            ai_force = self.ai_strength * 0.30

        self.arm_position += (
            ai_force * ai_variance
        )

        # =====================================================
        # STAMINA RECOVERY
        # =====================================================

        if self.stamina < self.max_stamina:

            recovery = self.normal_stamina_recovery

            # TASK 4:
            # Temporary recovery boost
            if self.counter_surge_active:
                recovery += self.counter_stamina_recovery

            self.stamina = min(
                self.max_stamina,
                self.stamina + recovery
            )

        # =====================================================
        # TASK 3: EXHAUSTION
        # =====================================================

        if self.stamina <= 10:
            self.exhausted = True
        else:
            self.exhausted = False

        # =====================================================
        # WIN / LOSS
        # =====================================================

        if self.arm_position <= -self.target_limit:

            self.winner = "PLAYER"
            self.game_state = "GAME_OVER"

        elif self.arm_position >= self.target_limit:

            self.winner = "COMPUTER"
            self.game_state = "GAME_OVER"

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.arm_position = 0.0
        self.stamina = 100.0

        self.last_key = None

        self.winner = None
        self.game_state = "PLAYING"

        # Reset AI
        self.ai_state = "NORMAL"
        self.ai_timer = 0.0

        # Reset exhaustion
        self.exhausted = False

        # Reset counter-surge
        self.counter_window = 0.0
        self.counter_surge_active = False
        self.counter_surge_timer = 0.0

    # =========================================================
    # RENDER
    # =========================================================

    def render(self, screen):

        screen.fill((25, 28, 35))

        # =====================================================
        # TITLE
        # =====================================================

        title_surf = self.font_big.render(
            "ARM WRESTLE SHOWDOWN",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                12
            )
        )

        # =====================================================
        # HEADERS
        # =====================================================

        player_header = self.font_med.render(
            "PLAYER",
            True,
            (80, 160, 255)
        )

        computer_header = self.font_med.render(
            "COMPUTER",
            True,
            (255, 100, 80)
        )

        screen.blit(
            player_header,
            (60, 55)
        )

        screen.blit(
            computer_header,
            (self.width - 150, 55)
        )

        # =====================================================
        # TABLE
        # =====================================================

        table_rect = pygame.Rect(
            40,
            100,
            self.width - 80,
            310
        )

        pygame.draw.rect(
            screen,
            (110, 50, 15),
            table_rect,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (70, 30, 8),
            table_rect,
            width=5,
            border_radius=14
        )

        pygame.draw.line(
            screen,
            (45, 18, 4),
            (self.width // 2, 100),
            (self.width // 2, 410),
            4
        )

        # =====================================================
        # HAND POSITION
        # =====================================================

        offset_x = (
            self.arm_position
            / self.target_limit
        ) * 95

        hand_x = (
            self.width // 2
        ) + int(offset_x)

        hand_y = 235

        # Player arm
        p_shoulder = (70, 330)
        p_elbow = (140, 215)

        pygame.draw.line(
            screen,
            (200, 145, 110),
            p_shoulder,
            p_elbow,
            32
        )

        pygame.draw.line(
            screen,
            (215, 160, 125),
            p_elbow,
            (hand_x, hand_y),
            26
        )

        pygame.draw.circle(
            screen,
            (185, 130, 95),
            p_elbow,
            18
        )

        # Computer arm
        c_shoulder = (
            self.width - 70,
            330
        )

        c_elbow = (
            self.width - 140,
            215
        )

        pygame.draw.line(
            screen,
            (170, 110, 85),
            c_shoulder,
            c_elbow,
            32
        )

        pygame.draw.line(
            screen,
            (185, 125, 95),
            c_elbow,
            (hand_x, hand_y),
            26
        )

        pygame.draw.circle(
            screen,
            (150, 95, 70),
            c_elbow,
            18
        )

        # Hands
        pygame.draw.circle(
            screen,
            (225, 175, 140),
            (hand_x, hand_y),
            24
        )

        pygame.draw.circle(
            screen,
            (160, 115, 85),
            (hand_x, hand_y),
            24,
            width=3
        )

        # =====================================================
        # STAMINA BAR
        # =====================================================

        stamina_label = self.font_med.render(
            "STAMINA",
            True,
            (220, 220, 220)
        )

        screen.blit(
            stamina_label,
            (40, 445)
        )

        stamina_bg = pygame.Rect(
            140,
            448,
            240,
            22
        )

        stamina_fill = pygame.Rect(
            140,
            448,
            int(
                240
                * (
                    self.stamina
                    / self.max_stamina
                )
            ),
            22
        )

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            stamina_bg,
            border_radius=6
        )

        if self.stamina > 25:
            bar_color = (60, 210, 100)
        else:
            bar_color = (220, 60, 60)

        pygame.draw.rect(
            screen,
            bar_color,
            stamina_fill,
            border_radius=6
        )

        # =====================================================
        # TASK 2: AI SURGE / COOLDOWN
        # =====================================================

        if self.ai_state == "SURGE":

            surge_text = self.font_med.render(
                "AI POWER SURGE!",
                True,
                (255, 80, 80)
            )

            screen.blit(
                surge_text,
                (
                    self.width // 2
                    - surge_text.get_width() // 2,
                    475
                )
            )

        elif self.ai_state == "COOLDOWN":

            cooldown_text = self.font_med.render(
                "AI COOLDOWN",
                True,
                (100, 200, 255)
            )

            screen.blit(
                cooldown_text,
                (
                    self.width // 2
                    - cooldown_text.get_width() // 2,
                    475
                )
            )

        # =====================================================
        # TASK 3: EXHAUSTION WARNING
        # =====================================================

        if self.exhausted:

            exhausted_text = self.font_med.render(
                "EXHAUSTED!",
                True,
                (255, 70, 70)
            )

            screen.blit(
                exhausted_text,
                (
                    self.width // 2
                    - exhausted_text.get_width() // 2,
                    510
                )
            )

        # =====================================================
        # TASK 4: COUNTER WINDOW
        # =====================================================

        if (
            self.ai_state == "COOLDOWN"
            and self.counter_window > 0
            and not self.counter_surge_active
        ):

            counter_ready_text = self.font_small.render(
                "COUNTER WINDOW - PUSH NOW!",
                True,
                (255, 220, 80)
            )

            screen.blit(
                counter_ready_text,
                (
                    self.width // 2
                    - counter_ready_text.get_width() // 2,
                    535
                )
            )

        # =====================================================
        # TASK 4: ACTIVE COUNTER SURGE
        # =====================================================

        if self.counter_surge_active:

            counter_text = self.font_med.render(
                "COUNTER SURGE!",
                True,
                (255, 220, 80)
            )

            screen.blit(
                counter_text,
                (
                    self.width // 2
                    - counter_text.get_width() // 2,
                    535
                )
            )

        # =====================================================
        # GAME OVER
        # =====================================================

        if self.game_state == "GAME_OVER":

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 200)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            if self.winner == "PLAYER":

                win_text = "PLAYER WINS THE MATCH!"
                color = (80, 240, 100)

            else:

                win_text = "COMPUTER WINS!"
                color = (240, 80, 80)

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2
                    - text_surf.get_width() // 2,
                    self.height // 2 - 45
                )
            )

            restart_surf = self.font_med.render(
                "Press [R] to Rematch",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )