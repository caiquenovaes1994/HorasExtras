
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_bbbddf6b548d9d83f14e3183b955e112 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_8d7cdda7ee0058f38fa2d0dbc63044e1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "transparent", ["color"] : "#fafafa", ["border"] : "1px solid #444", ["width"] : "100%", ["&:hover"] : ({ ["backgroundColor"] : "rgba(255,255,255,0.1)" }) }),onClick:on_click_8d7cdda7ee0058f38fa2d0dbc63044e1},children)
    )
});
