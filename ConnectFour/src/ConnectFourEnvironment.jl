"""
# module ConnectFourEnvironment

- Julia version: 
- Author: ravontuur
- Date: 2021-11-24

# Examples

```jldoctest
julia>
```
"""
module ConnectFourEnvironment

    export WIN_REWARD, ILLEGAL_MOVE_PENALTY, NOT_LOSS
    export Environment
    export create_env, create_copy, move, get_legal_actions, game_result

    const WIN_REWARD = 1
    const DRAW_REWARD = 0
    const ILLEGAL_MOVE_PENALTY = -1
    const NOT_LOSS = 0

    State = Matrix{Int8}

    mutable struct Environment
        player::Int8  # 1 = first player, -1 = second player
        state::State
        last_action::Int8
        reward::Int8
        terminated::Bool
        illegal_action::Bool
        move_count::Int8
        connect_four::Array{Int8}
        connect_four_count::Int8
    end

    #----------------------------------------------------------------
    # public, exported methods

    function create_env()
        return Environment(1, zeros(Int8, 7, 6), 0, 0, false, false, 0, zeros(Int8, 0), 0)
    end

    function create_copy(env::Environment)
        return Environment(env.player, copy(env.state), env.last_action, env.reward,
            env.terminated, env.illegal_action, env.move_count,
            copy(env.connect_four), env.connect_four_count)
    end

    function move(self::Environment, action)
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

        if all_occupied(self)
            return finish(self, DRAW_REWARD, true)
        end
        return finish(self, NOT_LOSS)
    end

    function get_legal_actions(self::Environment)
        free_columns = []
        for col in 1:7
            if self.state[col, 6] == 0
                push!(free_columns, col)
            end
        end
        return free_columns
    end

    function game_result(self, player)
        self.reward * self.player * player
    end

    #----------------------------------------------------------------
    # private, not-exported methods

    function finish(self, result, terminate = false, illegal = false)
        self.illegal_action = illegal
        self.terminated = terminate
        self.player = -self.player
        self.reward = -result
        self.move_count += 1
        return self
    end

    function apply_move(self, action)
        for row in 1:7
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

        left = 0
        right = 0
        down = 0
        left_up = 0
        left_down = 0
        right_up = 0
        right_down = 0

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

        self.connect_four_count = 0
        if left + right + 1 >= 4
            left_pos = action - left + (7 * (action_row - 1))
            push!(self.connect_four, left_pos, left_pos + 1, left_pos + 2, left_pos + 3)
            self.connect_four_count+=1
            if left + right + 1 >= 5
                self.connect_four_count+=1
                push!(self.connect_four, left_pos + 4)
            end
            if left + right + 1 >= 6
                self.connect_four_count+=1
                push!(self.connect_four, left_pos + 5)
            end
            if left + right + 1 >= 7
                self.connect_four_count+=1
                push!(self.connect_four, left_pos + 6)
            end
        end

        if down + 1 >= 4
            down_pos = action + (7 * (action_row - down - 1))
            push!(self.connect_four, down_pos, down_pos + 7, down_pos + 14, down_pos + 21)
            self.connect_four_count+=1
        end

        if left_up + right_down + 1 >= 4
            right_down_pos = action + right_down + (7 * (action_row - right_down - 1))
            push!(self.connect_four, right_down_pos, right_down_pos + 6, right_down_pos + 12, right_down_pos + 18)
            self.connect_four_count+=1
            if left_up + right_down + 1 >= 5
                push!(self.connect_four, right_down_pos + 24)
                self.connect_four_count+=1
            end
            if left_up + right_down + 1 >= 6
                push!(self.connect_four, right_down_pos + 30)
                self.connect_four_count+=1
            end
        end

        if left_down + right_up + 1 >= 4
            left_down_pos = action - left_down + (7 * (action_row - left_down - 1))
            push!(self.connect_four, left_down_pos, left_down_pos + 8, left_down_pos + 16, left_down_pos + 24)
            self.connect_four_count+=1
            if left_down + right_up + 1 >= 5
                push!(self.connect_four, left_down_pos + 32)
                self.connect_four_count+=1
            end
            if left_down + right_up + 1 >= 6
                push!(self.connect_four, left_down_pos + 40)
                self.connect_four_count+=1
            end
        end

        return self.connect_four_count > 0
    end

    function all_occupied(self)
        for col in 1:7
            if self.state[col, 6] == 0
                return false
            end
        end
        return true
    end
end