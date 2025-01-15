import json
import os
from collections import deque

from src.game.grid.cell_player import PlayerCell
from src.game.grid.cell_barrier import BarrierCell
from src.game.grid.cell import Cell


class Grid:
    def __init__(self):
        self.tab = []
        self.barrier_size = ""

        self.player_victory_area = {}

        self.init_tab()
        # For printing purpose
        self.first_line = ""
        self.last_line = ""
        self.init_output_first_last_line()


    def init_tab(self):
        config_path = os.path.join(os.getcwd(), "configuration/config.json")
        with open(config_path, 'r') as file:
            data = json.load(file)
        self.barrier_size = data['barrier_size']

        size = data['grid_size'] + data['grid_size'] - 1
        for i in range(size):
            self.tab.append([])
            for j in range(size):
                if i % 2 == 0 and j % 2 == 0:
                    self.tab[i].append(Cell(i, j))
                else:
                    self.tab[i].append(BarrierCell(i, j, " "))

    def init_output_first_last_line(self):
        self.first_line, _, self.last_line = self.grid_to_display()


    def get_player(self, id):
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if isinstance(self.tab[i][j], PlayerCell) and self.tab[i][j].id == id:
                    return self.tab[i][j]
        raise ValueError(f"Player with id {id} not found.")

    def init_players(self, ids):
        size = len(self.tab)
        starting_positions = {
            2: [(0, size // 2), (size - 1, size // 2)],  # 2 players
            3: [(0, size // 2), (size - 1, size // 2), (size // 2, 0)],  # 3 players
            4: [(0, size // 2), (size - 1, size // 2), (size // 2, 0), (size // 2, size - 1)]  # 4 players
        }

        if len(ids) not in starting_positions:
            raise ValueError("The number of players must be 2, 3, or 4.")

        positions = starting_positions[len(ids)]
        winning_areas = {
            1: len(self.tab) - 1,  # Player 1 wins when reaching the last row
            2: 0,  # Player 2 wins when reaching the first row
            3: len(self.tab) - 1,  # Player 3 wins when reaching the last column
            4: 0  # Player 4 wins when reaching the first column
        }

        for i, player_id in enumerate(ids):
            x, y = positions[i]
            cell = PlayerCell(player_id, x, y)
            self.add_playerCell(cell)

            self.player_victory_area[player_id] = winning_areas[player_id]

    def get_cell(self, x, y):
        return self.tab[x][y]


    def grid_to_display(self):
        output = ""
        for i, row in enumerate(self.tab):
            # Adding number to the left
            if i % 2 == 0:
                number = i // 2 + 1
                output += f" {number} | " if number < 10 else f"{number} | "
            else:
                output += f"   | "
            # Adding sign cell
            for j, cell in enumerate(row):
                output += f"{cell.sign}"
            ## Adding number to the right
            if i % 2 == 1:
                number = i // 2 + 1
                output += f" | {number}\n"
            else:
                output += " |\n"

        # Adding number to the top
        parts = output.splitlines()[0].split('|')[1].strip()
        first_line = "     "
        counter = 1
        for i in range(len(parts)):
            if parts[i] == " ":
                first_line += f"{counter}"
                counter += 1
            else:
                first_line += " "
        first_line += "\n"

        # Adding number to the bottom
        last_line = "    "
        line = output.splitlines()[len(self.tab) - 1].split("|")[1]
        counter = 1
        for i in range(len(line)):
            if line[i] == " ":
                last_line += " "
            else:
                last_line += f"{counter}"
                counter += 1

        return first_line, output, last_line


    def add_playerCell(self, cell_player):
        self.tab[cell_player.x][cell_player.y] = cell_player


    def remove_playerCell(self, cell_player):
        self.tab[cell_player.x][cell_player.y] = Cell(cell_player.x, cell_player.y)


    def play_action(self, cell, action):
        action = action.split(" ")
        print(action)
        if action[0] == "block":
            return self.block(action[1:])

        if action[0] == "moove":
            return self.moove(cell, action[1])

        print(f"Error: Invalid action type '{action[0]}'.")
        return False


    def block(self, action):
        # Check size of the action
        # Example :
        #   action = ['x', '8', '9', 'y', '3']
        #   size_barrier_action = 5 - 2 - 1 = 2
        #   self.barrier_size = 2
        size_barrier_action = len(action) - 2 - 1  # x, y, et taille
        if size_barrier_action != self.barrier_size:
            print(f"Bad Size Barrier: {size_barrier_action} instead of {self.barrier_size}")
            return False

        x_values = []
        y_values = []
        current_label = None
        for item in action:
            if item == 'x':
                current_label = 'x'
            elif item == 'y':
                current_label = 'y'
            elif current_label == 'x':
                x_values.append(int(item))
            elif current_label == 'y':
                y_values.append(int(item))

        x_values = sorted(x_values)
        y_values = sorted(y_values)

        # print(f"x_values: {x_values}")
        # print(f"y_values: {y_values}")

        # Validation of data consistency
        if len(x_values) != 1 and len(y_values) != 1:
            print("Error: Only one axis should have multiple values for a valid barrier.")
            return False

        # Barrier placement -> Vertical barrier
        if len(x_values) == self.barrier_size:
            if self.are_numbers_consecutive(x_values, int(self.barrier_size) - 1):
                y_start = 2 * y_values[0] - 1

                # Part to check if a barrier is already active or not
                for x in x_values:
                    grid_x = 2 * (x - 1)
                    if self.tab[grid_x][y_start].active:
                        print(f"Error: A barrier is already active at [{grid_x}, {y_start}].")
                        return False

                for x in x_values[-1:0:-1]:
                    x_between = 2 * (x - 1) - 1
                    if self.tab[x_between][y_start].active:
                        print(f"Error: A barrier is already active at [{grid_x}, {y_start}].")
                        return False

                # Add Barrier
                for x in x_values:
                    grid_x = 2 * (x - 1)
                    if 0 <= grid_x < len(self.tab) and 0 <= y_start < len(self.tab[0]):
                        print(f"Placing horizontal barrier at [{grid_x}, {y_start}]")
                        self.tab[grid_x][y_start].set_active(True)
                        self.tab[grid_x][y_start].set_sign("|")
                    else:
                        print(f"Error: Coordinates [{grid_x}, {y_start}] are out of bounds.")
                        return False

                if self.is_player_have_winning_path():
                    for x in x_values:
                        grid_x = 2 * (x - 1)
                        self.tab[grid_x][y_start].set_active(False)
                        self.tab[grid_x][y_start].set_sign(" ")
                    return False
                else:
                    # Add barrier between 'x's selected
                    for x in x_values[-1:0:-1]:
                        x_between = 2 * (x - 1) - 1
                        print(x_between)
                        self.tab[x_between][y_start].set_active(True)
                        self.tab[x_between][y_start].set_sign("|")

                    # Add 'end' barrier(s)
                    self.add_end_x_barrier(x_values, y_start)

                    return True

            else:
                print(f"Error number barrier, gap between position {x_values} more than {int(self.barrier_size) - 1}")
                return False

        # Barrier placement -> Horizontal barrier
        elif len(y_values) == self.barrier_size:
            if self.are_numbers_consecutive(x_values, int(self.barrier_size) - 1):
                x_start = 2 * x_values[0] - 1
                # Part to check if a barrier is already active or not
                for y in y_values:
                    grid_y = 2 * (y - 1)
                    if self.tab[x_start][grid_y].active:
                        print(f"Error: A barrier is already active at [{x_start}, {grid_y}].")
                        return False

                for y in y_values[-1:0:-1]:
                    y_between = 2 * (y - 1) - 1
                    if self.tab[x_start][y_between].active:
                        print(f"Error: A barrier is already active at [{x_start}, {grid_y}].")
                        return False

                # Add Barrier
                for y in y_values:
                    grid_y = 2 * (y - 1)
                    if 0 <= x_start < len(self.tab) and 0 <= grid_y < len(self.tab[0]):
                        print(f"Placing vertical barrier at [{x_start}, {grid_y}]")
                        self.tab[x_start][grid_y].set_active(True)
                        self.tab[x_start][grid_y].set_sign("-")
                    else:
                        print(f"Error: Coordinates [{x_start}, {grid_y}] are out of bounds.")
                        return False

                if self.is_player_have_winning_path():
                    for y in y_values:
                        grid_y = 2 * (y - 1)
                        self.tab[x_start][grid_y].set_active(False)
                        self.tab[x_start][grid_y].set_sign(" ")
                    return False
                else:
                    # Add barrier between 'y's selected
                    for y in y_values[-1:0:-1]:
                        y_between = 2 * (y - 1) - 1
                        self.tab[x_start][y_between].set_active(True)
                        self.tab[x_start][y_between].set_sign("-")

                    # Add 'end' barrier(s)
                    self.add_end_y_barrier(x_start, y_values)

                    return True
            else:
                print(f"Error number barrier, gap between position {y_values} more than {int(self.barrier_size) - 1}")
                return False
        else:
            print("Error: Invalid barrier size.")
            return False

        # TODO: Not needed anymore, If-Else conditions have a return
        return True

    def add_end_x_barrier(self, x_values, y):
        x_left = 2 * (x_values[0] - 1) - 1
        x_previous_barrier = x_left - 1

        x_right = 2 * x_values[len(x_values) - 1] - 1
        x_next_barrier = x_right + 1

        if 0 < x_left < len(self.tab):
            if 0 <= x_previous_barrier < len(self.tab):
                if self.tab[x_previous_barrier][y].active and self.tab[x_previous_barrier][y].sign == "|":
                    self.tab[x_left][y].set_active(True)
                    self.tab[x_left][y].set_sign("|")

        if 0 < x_right < len(self.tab):
            if 0 <= x_next_barrier < len(self.tab):
                if self.tab[x_next_barrier][y].active and self.tab[x_next_barrier][y].sign == "|":
                    self.tab[x_next_barrier][y].set_active(True)
                    self.tab[x_next_barrier][y].set_sign("|")

    def add_end_y_barrier(self, x, y_values):
        y_left = 2 * (y_values[0] - 1) - 1
        y_previous_barrier = y_left - 1

        y_right = 2 * y_values[len(y_values) - 1] - 1
        y_next_barrier = y_right + 1

        if 0 < y_left < len(self.tab):
            if 0 <= y_previous_barrier < len(self.tab):
                if self.tab[x][y_previous_barrier].active and self.tab[x][y_previous_barrier].sign == "-":
                    self.tab[x][y_left].set_active(True)
                    self.tab[x][y_left].set_sign("-")

        if 0 < y_right < len(self.tab):
            if 0 <= y_next_barrier < len(self.tab):
                if self.tab[x][y_next_barrier].active and self.tab[x][y_next_barrier].sign == "-":
                    self.tab[x][y_right].set_active(True)
                    self.tab[x][y_right].set_sign("-")


    def is_player_have_winning_path(self):
            for player_id, victory_area in self.player_victory_area.items():
                if self.is_player_isolated(player_id, victory_area):
                    print(f"Error: Player {player_id} isolated, no winning path found")
                    return True
            return False


    def is_player_isolated(self, player_id, victory_area):
        # Retrieve the player's current position
        cell_player = self.get_player(player_id)
        start_x, start_y = cell_player.x, cell_player.y

        # Initialize visited set to track visited cells
        visited = set()
        visited.add((start_x, start_y))

        # Define the possible movements (top, bottom, left, right)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        # Breadth-First Search (BFS) to explore paths
        queue = deque([(start_x, start_y)])
        while queue:
            current_x, current_y = queue.popleft()

            # Check if we have reached a victory position -> player is not isolated
            if player_id in [1, 2] and current_x == victory_area:
                return False
            if player_id in [3, 4] and current_y == victory_area:
                return False

            # Explore all valid movements
            for dx, dy in directions:
                next_x, next_y = current_x + dx, current_y + dy

                # Check if the next cell is within bounds
                if not (0 <= next_x < len(self.tab) and 0 <= next_y < len(self.tab)):
                    continue

                # Check if there's a barrier blocking the path
                barrier_x, barrier_y = current_x + dx // 2, current_y + dy // 2
                if isinstance(self.get_cell(barrier_x, barrier_y), BarrierCell) and self.get_cell(barrier_x, barrier_y).active:
                    continue

                # Check if the next cell has not been visited and is passable
                if (next_x, next_y) not in visited and isinstance(self.tab[next_x][next_y], Cell):
                    visited.add((next_x, next_y))
                    queue.append((next_x, next_y))

        # If we exit the loop without finding a victory position, the player is isolated
        return True


    # Checks if all numbers in the list are consecutive, meaning there is a gap of 1 between each pair of adjacent numbers.
    def are_numbers_consecutive(self, numbers, expected_gap):
        # Sort the numbers to check for the closest values
        sorted_numbers = sorted(numbers)

        # Check the gaps between consecutive numbers
        for i in range(len(sorted_numbers) - 1):
            if sorted_numbers[i + 1] - sorted_numbers[i] != expected_gap:
                return False
        return True


    def moove(self, cell_player, movement):
        directions = {
            "top": (-2, 0),
            "bottom": (2, 0),
            "left": (0, -2),
            "right": (0, 2),
        }

        specific_directions = {
            "top_left": (-2, -2),
            "top_right": (-2, 2),
            "bottom_left": (2, -2),
            "bottom_right": (2, 2)
        }

        if movement in directions:
            dx, dy = directions[movement]
            new_x, new_y = cell_player.x + dx, cell_player.y + dy

            # Check if the target position is out of bounds
            if not (0 <= new_x < len(self.tab) and 0 <= new_y < len(self.tab[0])):
                print(f"Error: Movement {movement} at [{new_x}, {new_y}] is out of bounds.")
                return False

            # Check the barrier cell between the initial position and the new position
            barrier_x, barrier_y = cell_player.x + dx // 2, cell_player.y + dy // 2
            barrier_cell = self.get_cell(barrier_x, barrier_y)

            if isinstance(barrier_cell, BarrierCell) and barrier_cell.active:
                print(f"Error: Barrier at ({barrier_x}, {barrier_y}) is active. Movement blocked.")
                return False

            # Check if the target cell is occupied by another player
            if isinstance(self.tab[new_x][new_y], PlayerCell):
                # TODO: Very specific case (should be optimized for cleanliness, especially when using `cell_player.x + dx` everywhere)
                cell = self.get_cell(cell_player.x + dx, cell_player.y + dy)
                if (cell_player.x + dx, cell_player.y + dy) in self.get_winning_positions(cell_player.id) and cell.id != cell_player.id:
                    self.remove_playerCell(cell_player)
                    self.add_playerCell(PlayerCell(cell.id, cell_player.x, cell_player.y))
                    cell_player.set_x(cell_player.x + dx)
                    cell_player.set_y(cell_player.y + dy)
                    self.add_playerCell(cell_player)

                    return True

                # Attempt to jump
                jump_x, jump_y = new_x + dx, new_y + dy

                # Checks if the jump is possible (within bounds)
                if not (0 <= jump_x < len(self.tab) and 0 <= jump_y < len(self.tab[0])):
                    print(f"Error: Cannot jump {movement}, out of bounds.")
                    return False

                # TODO: Normally, this case should always be true
                # Checks if the cell after the jump is free
                if not isinstance(self.tab[jump_x][jump_y], Cell):
                    print(f"Error: Cannot jump {movement}, target is not free.")
                    return False

                # Checks if the jump lands on a winning position for another player
                for player_id in range(1, len(self.tab) + 1):  # Parcourt les joueurs
                    winning_positions = self.get_winning_positions(player_id)
                    if (jump_x, jump_y) in winning_positions and player_id != cell_player.id:
                        print(f"Error: Cannot jump to a winning position of player {player_id}.")
                        return False

                # Performs the jump
                self.remove_playerCell(cell_player)
                cell_player.set_x(jump_x)
                cell_player.set_y(jump_y)
                self.add_playerCell(cell_player)

                return True

            # Checks if the target cell is free for a normal move
            if isinstance(self.tab[new_x][new_y], Cell):
                # Perform the normal movement
                self.remove_playerCell(cell_player)
                cell_player.set_x(new_x)
                cell_player.set_y(new_y)
                self.add_playerCell(cell_player)

                return True

            print(f"Error: Movement {movement} blocked.")
            return False

        # Diagonal case
        elif movement in specific_directions:
            if self.is_diagonal_moove(movement, cell_player.x, cell_player.y):
                dx, dy = specific_directions[movement]
                new_x, new_y = cell_player.x + dx, cell_player.y + dy
                self.remove_playerCell(cell_player)
                cell_player.set_x(new_x)
                cell_player.set_y(new_y)
                self.add_playerCell(cell_player)

                return True
        else:
            print(f"Error: Invalid movement '{movement}'.")
            return False



    def is_diagonal_moove(self, movement, x, y):
        movement1, movement2 = movement.split('_')
        directions = { "top": (-2, 0), "bottom": (2, 0), "left": (0, -2), "right": (0, 2) }

        dx_movement1, dy_movement1 = directions[movement1]
        dx_movement2, dy_movement2 = directions[movement2]

        if isinstance(self.tab[x + dx_movement1][y + dy_movement1], PlayerCell) and not self.tab[x + dx_movement1 // 2][y + dy_movement1 // 2].active:
            if isinstance(self.tab[x + dx_movement2 // 2][y + dy_movement2 // 2], BarrierCell) and self.tab[x + dx_movement2 // 2][y + dy_movement2 // 2].active:
                x_barrier = x + dx_movement1 + dx_movement2 // 2
                y_barrier = y + dy_movement1 + dy_movement2 // 2
                if not self.tab[x_barrier][y_barrier].active:
                    return True

        if isinstance(self.tab[x + dx_movement2][y + dy_movement2], PlayerCell) and not self.tab[x + dx_movement2 // 2][y + dy_movement2 // 2].active:
            if isinstance(self.tab[x + dx_movement1 // 2][y + dy_movement1 // 2], BarrierCell) and self.tab[x + dx_movement1 //2][y + dy_movement1 // 2].active:
                x_barrier = x + dx_movement2 + dx_movement1 // 2
                y_barrier = y + dy_movement2 + dy_movement1 // 2
                if not self.tab[x_barrier][y_barrier].active:
                    return True

        # if isinstance(self.tab[x + dx_movement1][y + dy_movement1], PlayerCell) and not self.tab[x + dx_movement1 // 2][y + dy_movement1 // 2].active:
        #     if isinstance(self.tab[x + dx_movement1 + dx_movement2 // 2][y + dy_movement1 + dy_movement2 // 2], BarrierCell) and self.tab[x + dx_movement1 + dx_movement2 // 2][y + dy_movement1 + dy_movement2 // 2].active:
        #         x_barrier = x + dx_movement2 + dx_movement1 // 2
        #         y_barrier = y + dy_movement2 + dy_movement1 // 2
        #         if not self.tab[x_barrier][y_barrier].active:
        #             return True

        # if isinstance(self.tab[x + dx_movement2][y + dy_movement2], PlayerCell) and not self.tab[x + dx_movement2 // 2][y + dy_movement2 // 2].active:
        #     if isinstance(self.tab[x + dx_movement2 + dx_movement1 // 2][y + dy_movement2 + dy_movement1 // 2], BarrierCell) and self.tab[x + dx_movement2 + dx_movement1 //2][y + dy_movement2 + dy_movement1 // 2].active:
        #         x_barrier = x + dx_movement1 + dx_movement2 // 2
        #         y_barrier = y + dy_movement1 + dy_movement2 // 2
        #         if not self.tab[x_barrier][y_barrier].active:
        #             return True

        return False

    # Returns the winning positions for a given player based on their ID.
    def get_winning_positions(self, player_id):
        size = len(self.tab)
        winning_positions = {
            1: [(size - 1, y) for y in range(0, size, 2)],  # Bottom line
            2: [(0, y) for y in range(0, size, 2)],  # Top line
            3: [(x, size - 1) for x in range(0, size, 2)],  # Right Column
            4: [(x, 0) for x in range(0, size, 2)]  # Left Column
        }
        return winning_positions.get(player_id, [])


    def __str__(self):
        _, output, _ = self.grid_to_display()

        return self.first_line + output + self.last_line