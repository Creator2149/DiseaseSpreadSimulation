# ---------------------------------------------
# Disease Spread Simulation
# Created by Rishit Choudhary, 2025
# For educational purposes – modeling inequality and health outcomes
# ---------------------------------------------

import pygame
from sys import exit
from random import uniform, randint
import math

pygame.init()
pygame.font.init()

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.pos = [uniform(0, WIDTH - 32), uniform(0, HEIGHT - 32)]

        self.image = pygame.image.load("healthy.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (32, 32))
        self.rect = self.image.get_rect(center = (int(self.pos[0]), int(self.pos[1])))

        self.status = "healthy"
        self.recent_contacts = set()

        self.infection_radius = int(max(8, min(40, 1500 / (agent_count ** 0.75))))

        self.velocity = [0, 0]
        while self.velocity == [0, 0]:
            self.velocity = [uniform(-2.5, 2.5), uniform(-2.5, 2.5)]

        self.infection_timer = 0
        self.infection_duration = uniform(4, 6)

        self.velocity_timer = 0
        self.veloicty_duration = uniform(3, 6)

        self.rich = randint(1, 100) <= 30

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity[0] *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.velocity[1] *= -1

        if self.status == "infected":
            self.infection_timer += 1 / FPS
            if self.infection_timer >= self.infection_duration:
                if self.rich:
                    die_chance = 1
                else:
                    die_chance = 3

                if randint(1, 10) > die_chance:
                    self.change_status("recovered")
                else:
                    self.change_status("dead")

        
        if self.status == "dead":
            self.velocity = [0, 0]
            return

        self.velocity_timer += 1 / FPS
        if self.velocity_timer >= self.veloicty_duration:
            self.velocity = [0, 0]
            while self.velocity == [0, 0]:
                self.velocity = [uniform(-2.5, 2.5), uniform(-2.5, 2.5)]
            self.velocity_timer = 0

    def change_status(self, new_status):
        self.image = pygame.image.load(f"{new_status}.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=(int(self.pos[0]), int(self.pos[1])))
        self.status = new_status

def distance(agent1, agent2):
    x1 = agent1.pos[0]
    y1 = agent1.pos[1]
    x2 = agent2.pos[0]
    y2 = agent2.pos[1]

    dx = x1 - x2
    dy = y1 - y2

    distance = math.sqrt(dx * dx + dy * dy)
    return distance

WIDTH, HEIGHT, FPS = 800, 600, 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disease Spread Simulation")

icon_image = pygame.image.load("virus.png").convert_alpha()
pygame.display.set_icon(icon_image)

clock = pygame.time.Clock()

agents = pygame.sprite.Group()

spawn_flag = False
show_stats = False

font = pygame.font.Font("Roboto.ttf", 20)

agent_count = 100
num_infected_at_start = max(1, int(0.08 * agent_count + randint(0, 2)))
num_healthy_at_start = agent_count - num_infected_at_start

show_instructions = True

instructions_text = [
    "Disease Spread Simulation",
    "",
    "In this simulation, you will observe how a disease spreads",
    "through a population of 100 people, each moving independently.",
    "",
    "Socioeconomic inequality is modeled through two groups:",
    "",
    "- 30% of the population is considered rich.",
    "- Rich people have only a 10% chance of dying when infected.",
    "- Poor people have a 30% chance of dying.",
    "",
    "This reflects how economic status can affect health outcomes.",
    "",
    "COLOR KEY:",
    "  • White - Healthy",
    "  • Red - Infected",
    "  • Blue - Recovered (immune)",
    "  • Grey - Dead",
    "  • Gold ring - Person is rich",
    "",
    "CONTROLS:",
    "  • [SPACE] - Start simulation",
    "  • [T] - Toggle stats display",
]

simulation_over = False

restart_font = pygame.font.Font("Roboto.ttf", 24)
button_color = (100, 180, 255)
button_hover_color = (60, 140, 210)
button_text_color = "black"


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if show_instructions:
                    show_instructions = False

                if not spawn_flag:   
                    for i in range(num_infected_at_start):
                        infected_agent = Agent()
                        infected_agent.change_status("infected")
                        agents.add(infected_agent)
                    for _ in range(num_healthy_at_start):
                        agents.add(Agent())

                    spawn_flag = True
            
            if event.key == pygame.K_t:
                show_stats = not show_stats

    if show_instructions:
        screen.fill("lightgrey")
        font_big = pygame.font.Font("Roboto.ttf", 32)
        font_big.set_underline(True)
        font_small = pygame.font.Font("Roboto.ttf", 20)
        
        for idx, line in enumerate(instructions_text):
            if idx == 0:
                rendered = font_big.render(line, True, "black")
                screen.blit(rendered, (50, 15 + idx * 25))
                continue

            rendered = font_small.render(line, True, "black")
            screen.blit(rendered, (50, 15 + idx * 25))
        
        pygame.display.update()
        continue

    screen.fill("lightgrey")

    if not simulation_over:
        agents.update()

    for agent in agents:
        if agent.status == "infected":
            for healthy_agent in agents:
                if healthy_agent.status == "healthy":
                    if distance(agent, healthy_agent) < agent.infection_radius:
                        if healthy_agent not in agent.recent_contacts:
                            base = max(2, int(20 - agent_count * 0.1))
                            chance = base + (3 if not healthy_agent.rich else 0)

                            infect = randint(1, 100) <= chance

                            if infect:
                                healthy_agent.change_status("infected")

                            agent.recent_contacts.add(healthy_agent)
                    else:
                        if healthy_agent in agent.recent_contacts:
                            agent.recent_contacts.remove(healthy_agent)

    if not simulation_over and spawn_flag:
        infected_remaining = sum(1 for agent in agents if agent.status == "infected")
        if infected_remaining == 0:
            simulation_over = True

    agents.draw(screen)

    for agent in agents:
        if agent.rich:
            pygame.draw.circle(screen, "gold", agent.rect.center, 18, 2)


    healthy_count = sum(1 for agent in agents if agent.status == "healthy")
    infected_count = sum(1 for agent in agents if agent.status == "infected")
    recovered_count = sum(1 for agent in agents if agent.status == "recovered")
    dead_count = sum(1 for agent in agents if agent.status == "dead")

    small_font = pygame.font.Font("Roboto.ttf", 15)
    small_font.set_bold(True)

    healthy_rich = sum(1 for agent in agents if agent.status == "healthy" and agent.rich)
    infected_rich = sum(1 for agent in agents if agent.status == "infected" and agent.rich)
    recovered_rich = sum(1 for agent in agents if agent.status == "recovered" and agent.rich)
    dead_rich = sum(1 for agent in agents if agent.status == "dead" and agent.rich)

    def rich_percent_text(rich, total):
        if total == 0:
            return "(RICH: 0%)"
        percent = int((rich / total) * 100)
        return f"(RICH: {percent}%)"

    healthy_count_surface = font.render(f"Healthy: {healthy_count}", True, "darkgreen")
    infected_count_surface = font.render(f"Infected: {infected_count}", True, "red")
    recovered_count_surface = font.render(f"Recovered: {recovered_count}", True, "blue")
    dead_count_surface = font.render(f"Dead: {dead_count}", True, "black")

    rich_count_color = (184, 134, 11)

    healthy_rich_surface = small_font.render(rich_percent_text(healthy_rich, healthy_count), True, rich_count_color)
    infected_rich_surface = small_font.render(rich_percent_text(infected_rich, infected_count), True, rich_count_color)
    recovered_rich_surface = small_font.render(rich_percent_text(recovered_rich, recovered_count), True, rich_count_color)
    dead_rich_surface = small_font.render(rich_percent_text(dead_rich, dead_count), True, rich_count_color)

    x, y = 5, 5
    line_spacing = 5
    block_spacing = 10

    healthy_rect = healthy_count_surface.get_rect(topleft=(x, y))
    healthy_rich_rect = healthy_rich_surface.get_rect(topleft=(x, healthy_rect.bottom + line_spacing))

    infected_rect = infected_count_surface.get_rect(topleft=(x, healthy_rich_rect.bottom + block_spacing))
    infected_rich_rect = infected_rich_surface.get_rect(topleft=(x, infected_rect.bottom + line_spacing))

    recovered_rect = recovered_count_surface.get_rect(topleft=(x, infected_rich_rect.bottom + block_spacing))
    recovered_rich_rect = recovered_rich_surface.get_rect(topleft=(x, recovered_rect.bottom + line_spacing))

    dead_rect = dead_count_surface.get_rect(topleft=(x, recovered_rich_rect.bottom + block_spacing))
    dead_rich_rect = dead_rich_surface.get_rect(topleft=(x, dead_rect.bottom + line_spacing))

    if show_stats:
        screen.blit(healthy_count_surface, healthy_rect)
        screen.blit(healthy_rich_surface, healthy_rich_rect)

        screen.blit(infected_count_surface, infected_rect)
        screen.blit(infected_rich_surface, infected_rich_rect)

        screen.blit(recovered_count_surface, recovered_rect)
        screen.blit(recovered_rich_surface, recovered_rich_rect)

        screen.blit(dead_count_surface, dead_rect)
        screen.blit(dead_rich_surface, dead_rich_rect)


    if simulation_over:

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        box_width, box_height = 420, 280
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (240, 240, 240, 255), box_surface.get_rect(), border_radius = 20)
        pygame.draw.rect(box_surface, "black", box_surface.get_rect(), 3, border_radius = 20)


        title_font = pygame.font.Font("Roboto.ttf", 28)
        title_font.set_underline(True)
        stat_font = pygame.font.Font("Roboto.ttf", 20)
        small_font = pygame.font.Font("Roboto.ttf", 16)

        title_surface = title_font.render("Simulation Over", True, "black")
        box_surface.blit(title_surface, (box_width // 2 - title_surface.get_width() // 2, 20))

        stat_lines = [
            ("Healthy", healthy_count, healthy_rich),
            ("Infected", infected_count, infected_rich),
            ("Recovered", recovered_count, recovered_rich),
            ("Dead", dead_count, dead_rich)
        ]

        for i, (label, total, rich) in enumerate(stat_lines):
            stat_text = f"{label}: {total}"
            percent_text = rich_percent_text(rich, total)

            stat_surface = stat_font.render(stat_text, True, "black")
            percent_surface = small_font.render(percent_text, True, rich_count_color)

            stat_y = 70 + i * 40
            box_surface.blit(stat_surface, (30, stat_y))
            box_surface.blit(percent_surface, (220, stat_y + 5))

        screen.blit(box_surface, (WIDTH // 2 - box_width // 2, HEIGHT // 2 - box_height // 2))

        
        button_width, button_height = 140, 40
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 2 + box_height // 2 + 10
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        hovered = button_rect.collidepoint(mouse)
        pygame.draw.rect(screen, button_hover_color if hovered else button_color, button_rect, border_radius=8)

        text_surface = restart_font.render("Restart", True, button_text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        if hovered and click[0]:
            show_instructions = True
            simulation_over = False
            spawn_flag = False

            agents.empty()


    pygame.display.update()
    clock.tick(FPS)
