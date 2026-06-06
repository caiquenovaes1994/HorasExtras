
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_1c85b2d8f8d812e0503385d47304d010 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_49559500ef96840d7174dd3ad8d00a95 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.open_profile", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["color"] : "#fafafa", ["border"] : "1px solid #444", ["width"] : "50%", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "rgba(255,255,255,0.1)" }) }),onClick:on_click_49559500ef96840d7174dd3ad8d00a95,variant:"outline"},children)
    )
});
