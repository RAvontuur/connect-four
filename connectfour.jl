"""
# module connectfour

- Julia version: 
- Author: ravontuur
- Date: 2021-11-24

# Examples

```jldoctest
julia>
```
"""
module connectfour

    export WIN_REWARD, ILLEGAL_MOVE_PENALTY, NOT_LOSS
    export Environment
    export create_env, move

    const WIN_REWARD = 1
    const ILLEGAL_MOVE_PENALTY = -1
    const NOT_LOSS = 0

    mutable struct Environment
        player
        state
        last_action
        reward
        terminated
        illegal_action
        move_count
        connect_four_count
    end

    function create_env()
        return Environment(1, zeros(Int8, 7, 6), 0, 0, false, false, 0, 0)
    end

    function finish(self, result, terminate = false, illegal = false)
        self.illegal_action = illegal
        self.terminated = terminate
        self.player = -self.player
        self.reward = -result
        self.move_count += 1
        return self
    end

    function apply_move(self, action)
        for row in range(1, length = 6)
            if self.state[action, row] == 0
                self.state[action, row] = self.player
                return self
            end
        end
    end

    function is_winning_action(self, player, action, row_offset=0)

        action_row = 1
        while action_row <= 6
            if self.state[action, action_row] == 0
                break
            end
            action_row += 1
        end

        action_row += row_offset
        if action_row > 6
            # illegal move
            return false
        end

        left = 1
        right = 1
        up = 1
        down = 1
        left_up = 1
        left_down = 1
        right_up = 1
        right_down = 1

        col = action - 1
        while col >= 1
            if self.state[col, action_row] == player
                left += 1
                col -= 1
            else
                break
            end
        end

        col = action + 1
        while col <= 7
            if self.state[col, action_row] == player
                right += 1
                col += 1
            else
                break
            end
        end

        row = action_row - 1
        while row >= 1
            if self.state[action, row] == player
                down += 1
                row -= 1
            else
                break
            end
        end

        col = action - 1
        row = action_row - 1
        while row >= 1 && col >= 1
            if self.state[col, row] == player
                left_down += 1
                col -= 1
                row -= 1
            else
                break
            end
        end

        col = action + 1
        row = action_row + 1
        while row <= 6 && col <= 7
            if self.state[col, row] == player
                right_up += 1
                col += 1
                row += 1
            else
                break
            end
        end

        col = action - 1
        row = action_row + 1
        while row <= 6 && col >= 1
            if self.state[col, row] == player
                left_up += 1
                col -= 1
                row += 1
            else
                break
            end
        end

        col = action + 1
        row = action_row - 1
        while row >= 1 && col <= 7
            if self.state[col, row] == player
                right_down += 1
                col += 1
                row -= 1
            else
                break
            end
        end

        if left + right + 1 >= 4
            left_pos = action - left + (7 * action_row)
#             self.connect_four.append(left_pos)
#             self.connect_four.append(left_pos + 1)
#             self.connect_four.append(left_pos + 2)
#             self.connect_four.append(left_pos + 3)
            self.connect_four_count+=1
            if left + right + 1 >= 5
                self.connect_four_count+=1
#                 self.connect_four.append(left_pos + 4)
            end
            if left + right + 1 >= 6
                self.connect_four_count+=1
#                 self.connect_four.append(left_pos + 5)
            end
            if left + right + 1 >= 7
                self.connect_four_count+=1
#                 self.connect_four.append(left_pos + 6)
            end
        end

        if up + down + 1 >= 4
            down_pos = action + (7 * (action_row - down))
#             self.connect_four = []
#             self.connect_four.append(down_pos)
#             self.connect_four.append(down_pos + 7)
#             self.connect_four.append(down_pos + 14)
#             self.connect_four.append(down_pos + 21)
            self.connect_four_count+=1
        end

        if left_up + right_down + 1 >= 4
            right_down_pos = action + right_down + (7 * (action_row - right_down))
#             self.connect_four = []
#             self.connect_four.append(right_down_pos)
#             self.connect_four.append(right_down_pos + 6)
#             self.connect_four.append(right_down_pos + 12)
#             self.connect_four.append(right_down_pos + 18)
            self.connect_four_count+=1
            if left_up + right_down + 1 >= 5
#                 self.connect_four.append(right_down_pos + 24)
                self.connect_four_count+=1
            end
            if left_up + right_down + 1 >= 6
#                 self.connect_four.append(right_down_pos + 30)
                self.connect_four_count+=1
            end
        end

        if left_down + right_up + 1 >= 4
            left_down_pos = action - left_down + (7 * (action_row - left_down))
#             self.connect_four = []
#             self.connect_four.append(left_down_pos)
#             self.connect_four.append(left_down_pos + 8)
#             self.connect_four.append(left_down_pos + 16)
#             self.connect_four.append(left_down_pos + 24)
            self.connect_four_count+=1
            if left_down + right_up + 1 >= 5
#                 self.connect_four.append(left_down_pos + 32)
                self.connect_four_count+=1
            end
            if left_down + right_up + 1 >= 6
#                 self.connect_four.append(left_down_pos + 40)
                self.connect_four_count+=1
            end
        end

        return self.connect_four_count > 0
    end

    function move(self, action)
        self.last_action = action
        if self.state[action, 6] != 0
            return finish(self, ILLEGAL_MOVE_PENALTY, true, true)
        end

        # Did player win
        if is_winning_action(self, self.player, action)
            apply_move(self, action)
            return finish(self, WIN_REWARD, true)
        end

        self = apply_move(self, action)
        return finish(self, NOT_LOSS)
    end

end