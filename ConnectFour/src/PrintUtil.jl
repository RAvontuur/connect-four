"""
# module PrintUtil

- Julia version: 1.6.4
- Author: ravontuur
- Date: 2021-12-04

# Examples

```jldoctest
julia>
```
"""
module PrintUtil

    export display_board

    using ConnectFour.ConnectFourEnvironment


     function who_is_now(self)
        s = ""
        if self.player == 1
            s *= "X"
        else
            s *= "O"
        end

        if self.terminated
            if self.reward == 1
                s *= " WON"
            elseif self.reward == -1
                s *= " LOST"
            else
                s = "Game ended in a DRAW"
            end
            if self.illegal_action
                s *= " after illegal move"
            end
        else
            s *= " is playing now"
        end

        return s
    end

    function display_board(self::Environment)
        s = ""
        x = "X"
        o = "O"
        for row in 1:6
            for col in 1:7
                if self.state[col,7 - row] == 0
                    s *= "_"
                elseif self.state[col,7 - row] == 1
                    s *= x
                elseif self.state[col,7 - row] == -1
                    s *= o
                end
            end
            s *= "\n"
        end
        s *= who_is_now(self) * "\n"
        return s
    end
end