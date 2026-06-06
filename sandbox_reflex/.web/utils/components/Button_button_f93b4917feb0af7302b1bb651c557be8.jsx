
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_f93b4917feb0af7302b1bb651c557be8 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_752d70b824497c8b135b6e260a433e6d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.save_profile", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#800000", ["color"] : "white", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "#A30000" }) }),onClick:on_click_752d70b824497c8b135b6e260a433e6d},children)
    )
});
