from Cell.Tiles import *
from Cell.Hexagon import Hexagon
from Player_Data.Player import PlayerData
from Units.Units import *
from random import choice, randint
from math import ceil
import pygame


class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.start_cell_size = cell_size
        self.cell_size = cell_size
        self.diagonal = cell_size * (3 ** 0.5)
        self.start_diagonal = self.diagonal
        self.rendering = True
        self.fps = 60
        self.board = [[Hexagon((j, i), (ceil(cell_size + cell_size * 1.5 * j),
                                        ceil(self.diagonal // 2 + self.diagonal * i + (
                                            self.diagonal // 2 if not j % 2 else 0))),
                               tuple(map(lambda x: (x[0] + cell_size * 1.5 * j,
                                                    x[1] + self.diagonal * i + (
                                                        self.diagonal // 2 if not bool(j % 2) else 0)),
                                         (
                                             (cell_size // 2, 0),
                                             (cell_size // 2 + cell_size, 0),
                                             (cell_size * 2, self.diagonal // 2),
                                             (cell_size // 2 + cell_size, self.diagonal),
                                             (cell_size // 2, self.diagonal),
                                             (0, self.diagonal // 2)
                                         ))))
                       for j in range(int(self.width // (cell_size * 3)) * 2 - 1)]
                      for i in range(int(self.height // (cell_size * (3 ** 0.5))) - 2)]
        self.one_d_board = [i for j in self.board for i in j]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.chosen_unit = None
        self.hexagons_to_move = {}
        self.hexagons_to_attack = {}
        self.chosen_spell = None
        self.hexagon_to_cast = []
        self.hexagons_to_stay = []
        self.changing_camera_pos = False
        self.camera_zooming = 0
        self.camera_pos = [0, 0]
        self.camera_data = [self.cell_size, self.diagonal]
        self.change_hexagons_pos(((self.width - (self.board[-1][-1].center[0] + self.cell_size)) // 2,
                                  ((self.height - (self.board[-1][-1].center[1] + self.diagonal // 2)) // 2)))
        self.health_bars = []
        self.turn = 0
        self.throne_0 = []
        self.throne_1 = []
        self.throne_menu_enable = False
        self.need_to_light_units = False
        self.players = [PlayerData(), PlayerData()]
        self.list_of_units = [i.__name__ for i in BaseUnit.__subclasses__()]\
                             + ['' for i in range(10 - len(BaseUnit.__subclasses__()))]
        self.color_of_unit_to_buy = None
        self.middle_hex = int(self.height // (cell_size * (3 ** 0.5))) - 2
        self.generate()

    def generate(self):
        self.throne_0 += [
            self.board[len(self.board) // 2 - 1][0],
            self.board[len(self.board) // 2][0],
            self.board[len(self.board) // 2 + 1][0],
            self.board[len(self.board) // 2][1],
            self.board[len(self.board) // 2 + 1][1]
        ]
        self.throne_1 += [
            self.board[len(self.board) // 2 - 1][-1],
            self.board[len(self.board) // 2][-1],
            self.board[len(self.board) // 2 + 1][-1],
            self.board[len(self.board) // 2][-2],
            self.board[len(self.board) // 2 + 1][-2]
        ]
        for elm in self.throne_0:
            elm.set_tile(Throne(0))
        for elm in self.throne_1:
            elm.set_tile(Throne(1))
        for _ in range(20):
            tile = choice(self.board[randint(0, len(self.board)) - 1]).tile
            if tile.useful and not any(tile.resources):
                tile.resources[randint(0, 2)] += randint(1, 3)

    def change_hexagons_size(self, cell_size, m_p):
        diagonal = cell_size * (3 ** 0.5)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].change_points(
                    tuple(map(lambda x: (x[0] + cell_size * 1.5 * j,
                                         x[1] + diagonal * i + (
                                             diagonal // 2 if not bool(j % 2) else 0)),
                              (
                                  (cell_size // 2, 0),
                                  (cell_size // 2 + cell_size, 0),
                                  (cell_size * 2, diagonal // 2),
                                  (cell_size // 2 + cell_size, diagonal),
                                  (cell_size // 2, diagonal),
                                  (0, diagonal // 2)
                              )))
                )
                self.board[i][j].change_center(
                    (round(cell_size + cell_size * 1.5 * j),
                     round(diagonal // 2 + diagonal * i + (
                         diagonal // 2 if not j % 2 else 0)))
                )
        new_x = ((m_p[0] + self.camera_pos[0]) / self.camera_data[0]) * cell_size
        new_y = ((m_p[1] + self.camera_pos[1]) / self.camera_data[1]) * diagonal
        self.change_hexagons_pos((-(round(new_x) - m_p[0]), -(round(new_y) - m_p[1])))
        self.cell_size = cell_size
        self.diagonal = diagonal

    def change_hexagons_pos(self, pos):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].change_points(tuple(map(lambda x: (x[0] + pos[0], x[1] + pos[1]),
                                                         self.board[i][j].points)))
                self.board[i][j].change_center((self.board[i][j].center[0] + pos[0],
                                                self.board[i][j].center[1] + pos[1]))

    def draw_display(self):
        pygame.draw.rect(self.screen, pygame.Color("black"), (0, 0, self.width, self.start_diagonal))
        wood = f"{self.players[self.turn].wood()} + {self.players[self.turn].buff[0]}"
        iron = f"{self.players[self.turn].iron()} + {self.players[self.turn].buff[1]}"
        gold = f"{self.players[self.turn].gold()} + {self.players[self.turn].buff[2]}"
        data = pygame.font.Font(None, 26).render(
            f"Дерево: {wood}    Железо: {iron}    Золото: {gold}", True, (255, 255, 255))
        self.screen.blit(data, (10, data.get_height() // 2, data.get_width(), data.get_height()))
        pygame.draw.rect(self.screen, pygame.Color("green"), (self.width / 26 * 24,
                                                              self.height / 26 * 23,
                                                              50, 50))
        pygame.draw.rect(self.screen, pygame.Color("yellow"), (self.width / 26 * 24 - 60,
                                                               self.height / 26 * 23,
                                                               50, 50))
        can_move = pygame.font.Font(None, 46).render(
            f"{len(list(filter(lambda x: x.unit and x.unit.player == self.turn and x.unit.moved, self.one_d_board)))}",
            True, (0, 0, 0))
        self.screen.blit(can_move, (self.width / 26 * 24 - 60 + 25 - can_move.get_rect().center[0],
                                    self.height / 26 * 23 + 25 - can_move.get_rect().center[1],
                                    50, 50))
        player = pygame.font.Font(None, 45).render(f"Ходит игрок {self.turn + 1}", True, (255, 255, 255))
        self.screen.blit(player, (self.width - player.get_width(), 0, player.get_width(), player.get_height()))

    def draw_hex_map(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if not self.board[i][j].tile.fill:
                    pygame.draw.polygon(self.screen, self.board[i][j].tile.color, self.board[i][j].points,
                                        ceil(2 * (self.cell_size / self.start_cell_size))
                                        if self.board[i][j] == self.chosen_unit else 1)
                else:
                    pygame.draw.polygon(self.screen, self.board[i][j].tile.color, self.board[i][j].points)

    def draw_units_to_go(self):
        if self.need_to_light_units:
            for elm in self.one_d_board:
                if elm.unit and elm.unit.player == self.turn and elm.unit.moved:
                    pygame.draw.polygon(self.screen, pygame.Color("orange"), elm.points, 3)

    def draw_units(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]:
                    if not self.board[i][j].unit is None:
                        self.board[i][j].unit.draw(self.screen, self.board[i][j],
                                                   self.cell_size, self.diagonal)

    def draw_throne_window(self):
        start_pos = (20 if self.turn else self.width - 60 - (self.height - 40) // 5 * 2, 20)
        a = (self.height - 80) // 5
        if self.throne_menu_enable:
            pygame.draw.rect(self.screen, Color("black"),
                             (start_pos[0], start_pos[1], a * 2 + 40, self.height - 40))
            pygame.draw.rect(self.screen, Color("white"),
                             (start_pos[0], start_pos[1], a * 2 + 40, self.height - 40), 3)
            for i in range(5):
                for j in range(2):
                    if self.list_of_units[i * 2: i * 2 + 2][j]:
                        help_unit = eval(f'eval(self.list_of_units[i * 2: i * 2 + 2][j])({self.turn}, 1)')
                        if all(help_unit.cost[n] <= self.players[self.turn].resources[n] for n in range(3)):
                            pygame.draw.rect(self.screen, help_unit.color,
                                             (start_pos[0] + 20 + a * j, start_pos[1] + 20 + a * i, a, a))
                        else:
                            pygame.draw.rect(self.screen, Color('Gray'),
                                             (start_pos[0] + 20 + a * j, start_pos[1] + 20 + a * i, a, a))
                    pygame.draw.rect(self.screen, Color("white"),
                                     (start_pos[0] + 20 + a * j, start_pos[1] + 20 + a * i, a, a), 3)

    def draw_chosen_unit(self):
        def add_to_hexagons_to_move(hexagon, num_):
            next_ = []
            pos = hexagon.index
            helper_1, helper_2 = (0, -1) if pos[0] % 2 else (1, 0)
            for j in range(pos[0] - 1, pos[0] + 2):
                for i in range(pos[1] - 1 + helper_1 - (1 if j == pos[0] and helper_1 else 0),
                               pos[1] + 2 + helper_2 + (1 if j == pos[0] and helper_2 else 0)):
                    try:
                        if not any([i < 0, i >= len(self.board),
                                    j < 0 or j >= len(self.board[0]),
                                    pos == (j, i),
                                    not self.board[i][j].tile.can_move,
                                    self.board[i][j] == self.chosen_unit]):
                            if self.board[i][j] not in union_dict:
                                union_dict[self.board[i][j]] = num_
                                if self.board[i][j] not in next_:
                                    next_ += [self.board[i][j]]
                    except IndexError:
                        pass
            return next_

        if self.chosen_unit and self.chosen_unit.unit:
            if not self.hexagons_to_move:
                to_do = [self.chosen_unit]
                union_dict = {}
                for num in range(max(self.chosen_unit.unit.moved, self.chosen_unit.unit.attack_range)):
                    new = []
                    for elm in to_do:
                        if not (elm.unit and elm.unit != self.chosen_unit.unit):
                            new += add_to_hexagons_to_move(elm, num + 1)
                    to_do = new[:]
                for elm in union_dict.keys():
                    if self.chosen_unit.unit.moved >= union_dict[elm]:
                        self.hexagons_to_move[elm] = union_dict[elm]
                    if elm.unit and elm.unit.player != self.turn \
                            and self.chosen_unit.unit.attack_range >= union_dict[elm]:
                        self.hexagons_to_attack[elm] = union_dict[elm]
            if self.chosen_spell:
                to_do = [self.chosen_unit]
                union_dict = {}
                for num in range(self.chosen_spell.range):
                    new = []
                    for elm in to_do:
                        if not (elm.unit and elm.unit != self.chosen_unit.unit):
                            new += add_to_hexagons_to_move(elm, num + 1)
                    to_do = new[:]
                self.hexagon_to_cast = list(union_dict.keys())
                if self.chosen_spell.use_on_himself:
                    self.hexagon_to_cast += [self.chosen_unit]

            for elm in self.hexagons_to_move.keys():
                if elm.unit is None:
                    pygame.draw.circle(self.screen, pygame.Color("white"),
                                       self.board[elm.index[1]][elm.index[0]].center, 2, 5)
            for elm in self.hexagons_to_attack.keys():
                pygame.draw.circle(self.screen, pygame.Color("red"),
                                   self.board[elm.index[1]][elm.index[0]].center, 2, 5)
                pygame.draw.polygon(self.screen, pygame.Color("red"), elm.points, 3)
            for elm in self.hexagon_to_cast:
                if elm.unit and self.chosen_spell and self.chosen_spell.can_cast(self, elm.unit):
                    pygame.draw.polygon(self.screen, pygame.Color("yellow"), elm.points, 3)

        if self.throne_menu_enable:
            union_dict = {}
            if self.turn == 0:
                for elm in self.throne_0:
                    add_to_hexagons_to_move(elm, 1)
                self.hexagons_to_stay = list(set(union_dict.keys()))
                empty_hexagons = []
                for i in self.hexagons_to_stay:
                    if not i.unit:
                        empty_hexagons.append(i)
                self.hexagons_to_stay = empty_hexagons
                for elm in union_dict:
                    if elm.unit is None:
                        pygame.draw.circle(self.screen, pygame.Color("White"),
                                           self.board[elm.index[1]][elm.index[0]].center, 2, 5)
            else:
                for elm in self.throne_1:
                    add_to_hexagons_to_move(elm, 1)
                self.hexagons_to_stay = list(set(union_dict.keys()))
                empty_hexagons = []
                for i in self.hexagons_to_stay:
                    if not i.unit:
                        empty_hexagons.append(i)
                self.hexagons_to_stay = empty_hexagons
                for elm in union_dict:
                    if elm.unit is None:
                        pygame.draw.circle(self.screen, pygame.Color("White"),
                                           self.board[elm.index[1]][elm.index[0]].center, 2, 5)

    def draw_double_bar(self, colors: tuple, pos: tuple, per_cent: int, shift: int):
        new_pos = list(pos)
        new_pos[2] *= per_cent / 100
        pygame.draw.rect(self.screen, pygame.Color(colors[0]), new_pos)
        pygame.draw.rect(self.screen, pygame.Color(colors[1]), (*map(lambda x: x - shift, pos[:2]),
                                                                *map(lambda x: x + shift, pos[2:])), shift)

    def chose_hexagon(self, pos):
        obj = min(self.one_d_board, key=lambda x: ((x.center[0] - pos[0]) ** 2 + (x.center[1] - pos[1]) ** 2) ** 0.5)
        if ((obj.center[0] - pos[0]) ** 2 + (obj.center[1] - pos[1]) ** 2) ** 0.5 > self.diagonal // 2:
            return None
        else:
            return obj

    def chose_unit(self, hexagon):
        self.clear_chosen_unit()
        if not hexagon or hexagon.unit is None or hexagon.unit.player != self.turn:
            self.chosen_unit = None
        else:
            self.chosen_unit = hexagon
            hexagon.unit.update()

    def chose_tile(self, pos):
        hexagon = self.chose_hexagon(pos)
        if not hexagon or hexagon.tile.__class__ == BaseTile or hexagon.tile.player != self.turn:
            return None
        return hexagon

    def move_unit(self, to_hexagon):
        if to_hexagon in self.hexagons_to_move:
            if not self.chosen_unit == to_hexagon:
                if self.chosen_unit in self.health_bars:
                    self.health_bars.remove(self.chosen_unit)
                    self.health_bars += [to_hexagon]
                self.chosen_unit.unit.hexagon = to_hexagon
                self.chosen_unit.unit.move(self.hexagons_to_move[to_hexagon])
                self.board[to_hexagon.index[1]][to_hexagon.index[0]].unit = self.chosen_unit.unit
                self.chosen_unit.unit = None
                self.chosen_unit = self.board[to_hexagon.index[1]][to_hexagon.index[0]]
                self.hexagons_to_move = {}
                self.hexagons_to_attack = {}
        elif to_hexagon in self.hexagons_to_stay:
            if self.chosen_unit == self.board[self.middle_hex // 2][-1 * self.turn]:
                if all(self.chosen_unit.unit.cost[i] <= self.players[self.turn].resources[i] for i in range(3)):
                    self.chosen_unit.unit.change_color(self.color_of_unit_to_buy)
                    self.chosen_unit.unit.hexagon = to_hexagon
                    self.board[to_hexagon.index[1]][to_hexagon.index[0]].unit = self.chosen_unit.unit
                    self.chosen_unit.unit.update()
                    self.chosen_unit.unit = None
                    self.chosen_unit = self.board[to_hexagon.index[1]][to_hexagon.index[0]]
                    self.hexagons_to_move = {}
                    self.hexagons_to_attack = {}
                    self.throne_menu_enable = False
                    self.hexagons_to_stay = []
                    for i in range(3):
                        self.players[self.turn].resources[i] -= self.chosen_unit.unit.cost[i]
                else:
                    self.board[self.middle_hex // 2][-1 * self.turn].unit = None
                    self.clear_chosen_unit()
        else:
            self.clear_chosen_unit()

    def click_in_throne_menu(self, pos):
        x = 20 if self.turn else self.width - 60 - (self.height - 40) // 5 * 2
        return x <= pos[0] <= x + 40 + (self.height - 40) // 5 * 2 and 20 <= pos[1] <= self.height - 20

    def click_in_hud(self, pos):
        start_pos = (0, 4 * (self.height / 5))
        hud_width = 6 * (self.width / 12)
        return start_pos[0] <= pos[0] <= hud_width and start_pos[1] <= pos[1] <= self.height

    def click_in_buttons(self, pos):
        if self.width / 26 * 24 <= pos[0] <= self.width / 26 * 24 + 50 \
                and self.height / 26 * 23 <= pos[1] <= self.height / 26 * 23 + 50:
            return 1
        if self.width / 26 * 24 - 60 <= pos[0] <= self.width / 26 * 24 - 60 + 50 \
                and self.height / 26 * 23 <= pos[1] <= self.height / 26 * 23 + 50:
            return 2
        return 0

    def clear_chosen_unit(self):
        self.chosen_unit = None
        self.hexagons_to_move = {}
        self.hexagons_to_attack = {}

    def use_throne_menu(self, pos):
        start_pos = (20 if self.turn else self.width - 60 - (self.height - 40) // 5 * 2, 20)
        a = (self.height - 80) // 5
        x, y = pos[0] - start_pos[0] - 20, pos[1] - 40
        if 0 <= x <= a * 2 and 0 <= y <= a * 5:
            unit_to_buy_name = self.list_of_units[y // a * 2:y // a * 2 + 2][x // a]
            i, j = self.middle_hex // 2, -1 * self.turn
            if unit_to_buy_name:
                eval(f"self.board[{i}][{j}].set_unit({unit_to_buy_name}({self.turn}, self.board[{i}][{j}]))")
                self.chosen_unit = self.board[i][j]
                self.color_of_unit_to_buy = self.board[i][j].unit.get_color()
                self.board[i][j].unit.change_color(Color("yellow"))
            else:
                self.board[self.middle_hex // 2][-1 * self.turn].unit = None
                self.clear_chosen_unit()

    def health_bar(self):
        for hexagon in self.health_bars:
            pygame.draw.rect(self.screen, Color("black"),
                             (hexagon.center[0] - self.cell_size,
                              hexagon.center[1] - self.diagonal // 2 - self.diagonal / 6,
                              self.cell_size * 2, self.diagonal / 6))
            health_per_cent = (hexagon.unit.health / hexagon.unit.full_health) * 100
            if 0 <= health_per_cent <= 25:
                color = Color("red")
            elif 25 <= health_per_cent <= 50:
                color = Color("orange")
            elif 50 <= health_per_cent <= 75:
                color = Color("yellow")
            else:
                color = Color("green")
            pygame.draw.rect(self.screen, Color("black"),
                             (hexagon.center[0] - self.cell_size,
                              hexagon.center[1] - self.diagonal // 2 - self.diagonal / 6,
                              self.cell_size * 2, self.diagonal / 6))
            pygame.draw.rect(self.screen, color,
                             (hexagon.center[0] - self.cell_size,
                              hexagon.center[1] - self.diagonal // 2 - self.diagonal / 6,
                              self.cell_size * 2 * (health_per_cent / 100), self.diagonal / 6))
            pygame.draw.rect(self.screen, Color("white"),
                             (hexagon.center[0] - self.cell_size,
                              hexagon.center[1] - self.diagonal // 2 - self.diagonal / 6,
                              self.cell_size * 2, self.diagonal / 6), 1)

    def hud(self):
        if self.chosen_unit:
            start_pos = (0, 4 * (self.height / 5))
            hud_width = 6 * (self.width / 12)
            hud_height = self.height - 4 * (self.height / 5)
            indent = hud_height // 15
            text_x = hud_height
            bar_width = hud_width - indent - text_x
            pygame.draw.rect(self.screen, pygame.Color("black"),
                             (*start_pos, hud_width, hud_height))
            pygame.draw.rect(self.screen, pygame.Color("white"),
                             (*start_pos, hud_width, hud_height), 3)
            pygame.draw.circle(self.screen, pygame.Color("white"),
                               (start_pos[0] + hud_height // 2, start_pos[1] + hud_height // 2),
                               hud_height // 2 - hud_height // 15, 2)
            char_class = pygame.font.Font(None, 30).render(str(self.chosen_unit.unit), True, (255, 255, 255))
            self.screen.blit(char_class, ((text_x + (bar_width - char_class.get_width()) // 2),
                                          start_pos[1] + indent))
            text = f"{self.chosen_unit.unit.moved}/{self.chosen_unit.unit.moves_per_round}"
            attack = pygame.font.Font(
                None, 26).render(
                f"АТК: {self.chosen_unit.unit.damage}    ХОД: {text}", True, (255, 255, 255))
            self.screen.blit(attack, ((text_x + (bar_width - attack.get_width()) // 2),
                                      start_pos[1] + (2 * indent) // 2 + char_class.get_height()))
            self.draw_double_bar(("red", "white"), (text_x, start_pos[1] + 2 * indent + attack.get_height()
                                                    + char_class.get_height(), bar_width, 1.3 * indent),
                                 self.chosen_unit.unit.health / (self.chosen_unit.unit.full_health / 100), 1)
            if self.chosen_unit.unit.mana:
                self.draw_double_bar(("blue", "white"), (text_x, start_pos[1] + 4 * indent + attack.get_height()
                                                         + char_class.get_height(), bar_width, 1.3 * indent),
                                     self.chosen_unit.unit.mana / (self.chosen_unit.unit.full_mana / 100), 1)
            count_spells = len(list(filter(lambda x: x, self.chosen_unit.unit.spells)))
            spell_box_side = self.height - (start_pos[1] + 6 * indent + 2 * attack.get_height()) - indent
            top_tab = start_pos[1] + (6.3 if self.chosen_unit.unit.mana else 5) * indent + 2 * attack.get_height()
            tab = (bar_width - 4 * spell_box_side) / 3
            left_tab = ((4 * spell_box_side + 3 * tab) - (count_spells * spell_box_side + (count_spells - 1) * tab)) / 2
            for num in range(count_spells):
                pygame.draw.rect(self.screen, pygame.Color("white"),
                                 (left_tab + text_x + (spell_box_side + tab) * num,
                                  top_tab, spell_box_side, spell_box_side), 1)

    def refresh_everything(self):
        self.chosen_unit = None
        self.hexagons_to_move = {}
        self.hexagons_to_attack = {}
        self.hexagon_to_cast = []
        self.throne_menu_enable = False
        self.need_to_light_units = False
        self.players[self.turn].update()
        for elm in self.one_d_board:
            if elm.unit and elm.unit.player == self.turn:
                elm.unit.refresh()
                for spell in elm.unit.spells:
                    if spell:
                        spell.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rendering = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    chosen_hexagon = self.chose_hexagon(event.pos)
                    if not self.click_in_buttons(event.pos):
                        if chosen_hexagon:
                            if not self.chosen_spell or chosen_hexagon not in self.hexagon_to_cast:
                                self.chosen_spell = None
                                if not self.hexagons_to_move:
                                    if ((not self.turn and self.chose_tile(event.pos) in self.throne_0)
                                            or (self.turn and self.chose_tile(event.pos) in self.throne_1)):
                                        self.chosen_unit = None
                                        self.throne_menu_enable = not self.throne_menu_enable
                                        self.board[self.middle_hex // 2][-1 * self.turn].unit = None
                                    elif self.throne_menu_enable and self.click_in_throne_menu(event.pos):
                                        self.use_throne_menu(event.pos)
                                    elif self.throne_menu_enable and self.click_in_throne_menu(event.pos):
                                        self.use_throne_menu(event.pos)
                                    elif self.chosen_unit and self.throne_menu_enable and\
                                            not self.click_in_throne_menu(event.pos) and self.hexagons_to_stay:
                                        self.move_unit(chosen_hexagon)
                                    elif self.chosen_unit and self.click_in_hud(event.pos):
                                        self.use_hud(event.pos)
                                    elif self.chosen_unit:
                                        if chosen_hexagon.unit:
                                            if chosen_hexagon.unit.player == self.turn:
                                                if chosen_hexagon == self.chosen_unit:
                                                    self.clear_chosen_unit()
                                                else:
                                                    self.chose_unit(chosen_hexagon)
                                            else:
                                                self.clear_chosen_unit()
                                        else:
                                            self.clear_chosen_unit()
                                    elif chosen_hexagon.unit:
                                        self.chose_unit(chosen_hexagon)
                                    else:
                                        self.chosen_unit = None
                                else:
                                    if self.throne_menu_enable and self.click_in_throne_menu(event.pos):
                                        self.use_throne_menu(event.pos)
                                    elif self.click_in_hud(event.pos):
                                        pass
                                    elif self.chosen_unit:
                                        if chosen_hexagon.unit is None:
                                            self.move_unit(chosen_hexagon)
                                        elif chosen_hexagon.unit.player == self.turn:
                                            if chosen_hexagon == self.chosen_unit:
                                                self.clear_chosen_unit()
                                            else:
                                                self.chose_unit(chosen_hexagon)
                                        elif chosen_hexagon in self.hexagons_to_attack:
                                            attack = self.chosen_unit.unit.attack(
                                                self.hexagons_to_attack[chosen_hexagon],
                                                chosen_hexagon.unit)
                                            if attack[0]:
                                                if self.chosen_unit not in self.health_bars:
                                                    self.health_bars += [self.chosen_unit]
                                                if chosen_hexagon not in self.health_bars:
                                                    self.health_bars += [chosen_hexagon]
                                                if attack[1]:
                                                    if self.chosen_unit.unit.attack_range == 1:
                                                        self.health_bars.remove(self.chosen_unit)
                                                        chosen_hexagon.unit = self.chosen_unit.unit
                                                        self.chosen_unit.unit = None
                                                    else:
                                                        self.health_bars.remove(chosen_hexagon)
                                                        chosen_hexagon.unit = None
                                                self.clear_chosen_unit()
                                        else:
                                            self.clear_chosen_unit()
                            else:
                                self.chosen_spell.cast(self, chosen_hexagon)
                                self.chosen_spell = None
                        elif not self.click_in_throne_menu(event.pos):
                            if not self.click_in_hud(event.pos):
                                self.clear_chosen_unit()
                            else:
                                pass
                        else:
                            self.use_throne_menu(event.pos)
                    else:
                        if self.click_in_buttons(event.pos) == 2:
                            self.need_to_light_units = not self.need_to_light_units
                        else:
                            self.turn = 0 if self.turn else 1
                            self.refresh_everything()
                elif event.button == 2:
                    self.changing_camera_pos = True
                elif event.button == 4:
                    if self.camera_zooming + 1 <= 3:
                        self.change_hexagons_size(self.cell_size + 5, event.pos)
                        self.camera_zooming += 1
                elif event.button == 5:
                    if self.camera_zooming - 1 >= -1:
                        self.change_hexagons_size(self.cell_size - 5, event.pos)
                        self.camera_zooming -= 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.changing_camera_pos = False
            elif event.type == pygame.MOUSEMOTION:
                if self.changing_camera_pos:
                    e = event.rel
                    if e[0] > 0:
                        if self.board[0][0].center[0] - 5 * self.cell_size < 0:
                            self.camera_pos[0] -= event.rel[0]
                            self.change_hexagons_pos((event.rel[0], 0))
                    elif e[0] < 0:
                        if self.board[0][-1].center[0] + 5 * self.cell_size > self.width:
                            self.camera_pos[0] -= event.rel[0]
                            self.change_hexagons_pos((event.rel[0], 0))
                    if e[1] > 0:
                        if self.board[0][0].center[1] - self.diagonal - 4 * self.cell_size < 0:
                            self.camera_pos[1] -= event.rel[1]
                            self.change_hexagons_pos((0, event.rel[1]))
                    elif e[1] < 0:
                        if self.board[-1][-1].center[1] + self.diagonal + 4 * self.cell_size > self.height:
                            self.camera_pos[1] -= event.rel[1]
                            self.change_hexagons_pos((0, event.rel[1]))
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r] and self.chosen_unit:
                    spell = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r].index(event.key)
                    if self.chosen_unit.unit.spells[spell] and self.chosen_unit.unit.spells[spell].casted:
                        if self.chosen_unit and self.chosen_unit.unit.spells[spell].is_activated(self):
                            if not self.chosen_unit.unit.spells[spell].casting:
                                self.chosen_unit.unit.spells[spell].cast(self)
                                self.hexagons_to_move = {}
                                self.hexagons_to_attack = {}
                            elif self.chosen_spell:
                                self.chosen_spell = None
                            else:
                                self.chosen_spell = self.chosen_unit.unit.spells[spell]

    def draw_resources(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if any(self.board[i][j].tile.resources):
                    index = self.board[i][j].tile.resources.index(list(filter(lambda x: x,
                                                                              self.board[i][j].tile.resources))[0])
                    pygame.draw.circle(self.screen, {0: Color("brown"),
                                                     1: Color("gray"),
                                                     2: Color("yellow")}[index],
                                       (self.board[i][j].center[0],
                                        self.board[i][j].center[1] + self.diagonal / 3 + self.diagonal / 24),
                                       self.diagonal / 7)

    def render(self):
        self.board[0][0].set_unit(BaseUnit(0, self.board[0][0]))
        self.board[0][4].set_unit(Worker(0, self.board[0][4]))
        self.board[0][5].set_unit(Warrior(0, self.board[0][5]))
        self.board[1][5].set_unit(Warrior(0, self.board[1][5]))
        self.board[1][4].set_unit(Warrior(1, self.board[1][4]))
        self.board[2][4].set_unit(Wizard(0, self.board[2][4]))
        self.board[3][3].set_tile(Mount())
        pygame.init()
        clock = pygame.time.Clock()
        while self.rendering:
            self.screen.fill((0, 0, 0))
            self.draw_hex_map()
            self.draw_units()
            self.draw_chosen_unit()
            self.draw_resources()
            self.draw_units_to_go()
            self.health_bar()
            self.hud()
            self.draw_display()
            self.draw_throne_window()
            self.update()
            pygame.display.flip()
            clock.tick(self.fps)


#test = Board(1080, 720, 20)
#test.render()
