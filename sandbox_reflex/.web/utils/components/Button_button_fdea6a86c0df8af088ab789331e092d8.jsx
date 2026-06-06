
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_fdea6a86c0df8af088ab789331e092d8 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_45a082be780b040f418aa3c51d0dda03 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.open_new_user", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#2ecc71", ["color"] : "white", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "#27ae60" }) }),onClick:on_click_45a082be780b040f418aa3c51d0dda03},children)
    )
});
