
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_b4a6c6f3e550742a606d00683f02b72f = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_7e390696e59addf55d30c60a5b55f1e3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.open_new_record", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#2ecc71", ["color"] : "white", ["&:hover"] : ({ ["backgroundColor"] : "#27ae60" }), ["marginBottom"] : "1em" }),onClick:on_click_7e390696e59addf55d30c60a5b55f1e3},children)
    )
});
